<template>
    <div class="flex min-h-screen" v-if="isAuthenticated">
        <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />

        <main class="flex-1 flex flex-col">
            <div class="dashboard-container flex-1 p-10px">
                <DragAndDrop @file-dropped="addFileToQueue" />
                <div v-for="(item, index) in fileQueue" :key="item.id" class="mt-4">
                    <UploadSection
                        v-model:file_name="item.file.name"
                        v-model:ticket_code="item.ticketCode"
                        v-model:unzip_password="item.unzipPassword"
                        v-model:description="item.description"
                        :uploadedFiles="uploadedFiles"
                        :fileQueue="[item.file]"
                        :userId="userId"
                        :progress="item.progress"
                        :loading="item.loading"
                        @remove-self="removeUpload(index)"
                        @upload="() => uploadFile(index)"
                    />
                </div>
            </div>
        </main>

        <!-- AlertDialog -->
        <AlertDialog
            :visible="dialogVisible"
            :title="dialogTitle"
            :message="dialogMessage"
            :loading="dialogLoading"
            @close="closeDialog"
        />

    </div>
    <div v-else class="flex h-screen justify-center items-center">
        <p>正在驗證身份或跳轉至登錄頁面...</p>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import LeftMenu from '@/components/LeftMenu.vue';
import DragAndDrop from '@/components/DragAndDrop.vue';
import UploadSection from '@/components/UploadSection.vue';
import AlertDialog from '@/components/AlertDialog.vue';

export default defineComponent({
    name: 'Dashboard',
    components: {
        LeftMenu,
        DragAndDrop,
        UploadSection,
        AlertDialog,
    },
    setup() {
        const router = useRouter();
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const dialogVisible = ref(false);
        const dialogTitle = ref('');
        const dialogMessage = ref('');
        const dialogLoading = ref(false);

        const showDialog = (title: string, message: string, loading = false) => {
            dialogTitle.value = title;
            dialogMessage.value = message;
            dialogLoading.value = loading;
            dialogVisible.value = true;
        };
        
        const closeDialog = () => {
            dialogVisible.value = false;
        };

        const authToken = ref(localStorage.getItem('token') || '');
        const isAuthenticated = ref(false);
        const uploadedFiles = ref<string[]>([]);
        const userId = ref<number | null>(null);
        
        const userInfo = ref<{
            id: number;
            account: string;
            email: string;
            real_name?: string;
            avatar?: string;
        } | null>(null);
        const fileQueue = ref<{ 
            id: string; 
            file: File; 
            unzipPassword: string; 
            ticketCode: string; 
            description: string;
            progress: number;
            loading: boolean;
        }[]>([]);

        const checkAuth = async () => {
            if (!authToken.value) {
                router.push('/');
                return;
            }
            try {
                const response = await axios.get('http://172.31.176.1:8000/api/auth/verify', {
                    headers: { Authorization: `Bearer ${authToken.value}` }
                });
                if (response.status === 200) {
                    isAuthenticated.value = true;
                    const userData = response.data.data;
                    userId.value = userData.id || null;
                    
                    // 更新用戶資料給 LeftMenu 使用
                    userInfo.value = {
                        id: userData.id,
                        account: userData.account,
                        email: userData.email,
                        real_name: userData.real_name,
                        avatar: userData.avatar,
                    };
                }
            } catch (error) {
                console.error('Token verification failed:', error);
                localStorage.removeItem('token');
                router.push('/');
            }
        };

        const addFileToQueue = (files: File[]) => {
            files.forEach(file => {
                const alreadyExists = fileQueue.value.some(
                    (item: { file: { name: string; }; }) => item.file.name === file.name
                );

                if (alreadyExists) {
                    alert(`文件 ${file.name} 已存在於上傳隊列中！`);
                    return;
                }

                fileQueue.value.push({
                    id: `${Date.now()}-${Math.random()}`,
                    file,
                    ticketCode: '',
                    unzipPassword: '',
                    description: '',
                    progress: 0,
                    loading: false,
                });
            });
        };

        const uploadFile = async (index: number) => {
            const item = fileQueue.value[index];
            if (!item.ticketCode) {
                alert('請輸入 Ticket Code');
                return;
            }

            item.loading = true;

            try {

                const ticketResp = await axios.get(`http://172.31.176.1:8000/api/tickets/${item.ticketCode}`, {
                    headers: { Authorization: `Bearer ${authToken.value}` }
                });
                if (ticketResp.status !== 200) {
                    alert('Ticket Code 錯誤！');
                    return;
                }

                const formData = new FormData();
                formData.append('uploaded_file', item.file);
                formData.append('user_id', String(userId.value || ''));
                formData.append('unzip_password', item.unzipPassword);
                formData.append('ticket_id', ticketResp.data.id);
                formData.append('description', item.description);

                const response = await axios.post(
                    'http://172.31.176.1:8000/api/uploaded-files/', 
                    formData, 
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            'Authorization': `Bearer ${authToken.value}`
                        },
                        onUploadProgress: progressEvent => {
                            if (progressEvent.total) {
                                item.progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
                            }
                        }
                });
                const uploadedFile = response.data;
                uploadedFiles.value.push(uploadedFile.name);
                showDialog('文件上傳成功！', `Tracking ID: ${uploadedFile.id}`);

                fileQueue.value.splice(index, 1);

            } catch (error) {
                console.error('File upload failed:', error);
                alert(`文件 ${item.file.name} 上傳失敗，請重試！`);
            }
        };

        onMounted(() => {
            checkAuth();
        });

        const removeUpload = (index: number) => {
            fileQueue.value.splice(index, 1);
        };

        return {
            menuItems,
            authToken,
            isAuthenticated,
            uploadedFiles,
            fileQueue,
            userId,
            userInfo,
            dialogVisible,
            dialogTitle,
            dialogMessage,
            dialogLoading,
            addFileToQueue,
            uploadFile,
            removeUpload,
            closeDialog,
        };
    },
});
</script>

<style scoped>
.dashboard-container {
    padding: 10px;
}
</style>
