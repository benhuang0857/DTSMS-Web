<template>
    <div class="flex h-screen" v-if="isAuthenticated">
        <LeftMenu :menuItems="menuItems" />

        <main class="flex-1 flex">
            <div class="dashboard-container flex-1 p-10px">
                <TopSection :rows="tableRows" />
                <DragAndDrop @file-dropped="addFileToQueue" />
                <UploadSection
                    :token="authToken"
                    :uploadedFiles="uploadedFiles"
                    :fileQueue="fileQueue"
                    :userId="userId"
                    @upload="uploadFiles"
                />
            </div>
        </main>
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
import TopSection from '@/components/TopSection.vue';
import DragAndDrop from '../components/DragAndDrop.vue';
import UploadSection from '../components/UploadSection.vue';

export default defineComponent({
    name: 'Dashboard',
    components: {
        LeftMenu,
        TopSection,
        DragAndDrop,
        UploadSection
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

        const tableRows = ref([
            { label: 'Macro', value: 12, percentage: '28.6%' },
            { label: 'Boot Strap Sector', value: 22, percentage: '42.9%' },
            { label: 'File Infectors Virus', value: 12, percentage: '28.6%' },
            { label: 'Label 4', value: 12, percentage: '28.6%' },
            { label: 'Label 5', value: 7, percentage: '14.3%' },
            { label: 'Label 6', value: 7, percentage: '14.3%' },
        ]);

        const authToken = ref(localStorage.getItem('token') || '');
        const isAuthenticated = ref(false);
        const uploadedFiles = ref<string[]>([]);
        const userId = ref<number | null>(null);
        const fileQueue = ref<File[]>([]); // 儲存待上傳的文件

        // 檢查用戶身份並獲取 user_id
        const checkAuth = async () => {
            if (!authToken.value) {
                router.push('/');
                return;
            }
            try {
                const response = await axios.get('http://172.31.176.1:8000/auth/verify', {
                    headers: { Authorization: `Bearer ${authToken.value}` }
                });
                if (response.status === 200) {
                    isAuthenticated.value = true;
                    userId.value = response.data.user_id || null;
                }
            } catch (error) {
                console.error('Token verification failed:', error);
                localStorage.removeItem('token');
                router.push('/');
            }
        };

        // 添加文件到佇列
        const addFileToQueue = (file: File) => {
            fileQueue.value.push(file);
        };

        // 上傳文件
        const uploadFiles = async () => {
            if (fileQueue.value.length === 0) {
                alert('請先選擇文件！');
                return;
            }

            for (const file of fileQueue.value) {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('user_id', String(userId.value || ''));
                formData.append('token', authToken.value);

                try {
                    const response = await axios.post('http://172.31.176.1:8000/file_uploads/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            'Authorization': `Bearer ${authToken.value}`
                        }
                    });
                    const uploadedFile = response.data;
                    uploadedFiles.value.push(uploadedFile.filename);
                    alert(`文件上傳成功！Tracking Number: ${uploadedFile.tracking_num}`);
                } catch (error) {
                    console.error('File upload failed:', error);
                    alert(`文件 ${file.name} 上傳失敗，請重試！`);
                }
            }
            fileQueue.value = []; // 清空佇列
        };

        // 在組件掛載時檢查身份
        onMounted(() => {
            checkAuth();
        });

        return {
            menuItems,
            tableRows,
            authToken,
            isAuthenticated,
            uploadedFiles,
            fileQueue,
            userId,
            addFileToQueue,
            uploadFiles
        };
    },
});
</script>

<style scoped>
.dashboard-container {
    padding: 10px;
}
</style>