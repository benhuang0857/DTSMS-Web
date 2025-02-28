<template>
    <div class="flex h-screen">
        <!-- 左側菜單 -->
        <LeftMenu :menuItems="menuItems" />

        <!-- 主內容 -->
        <main class="flex-1 bg-gray-100 p-6">
            <!-- 頂部區域 -->
            <div class="relative">
                <div class="h-40 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg"></div>
                <div class="absolute top-24 left-6 flex items-center space-x-4">
                    <img :src="form.avatar || defaultAvatar" alt="User Avatar"
                        class="w-20 h-20 rounded-full border-4 border-white" />
                    <div>
                        <h1 class="text-2xl font-bold text-gray-800">Settings</h1>
                    </div>
                </div>
            </div>

            <!-- 子選單 -->
            <div class="mt-20 border-b border-gray-200">
                <nav class="flex space-x-6">
                    <button v-for="tab in tabs" :key="tab" @click="activeTab = tab" :class="{
                        'text-blue-600 border-b-2 border-blue-600': activeTab === tab,
                        'text-gray-600': activeTab !== tab
                    }" class="pb-2">
                        {{ tab }}
                    </button>
                </nav>
            </div>

            <!-- 表單內容 -->
            <div class="mt-8 bg-white p-6 rounded-lg shadow-md max-w-[90%] mx-auto">
                <div class="grid grid-cols-2 gap-6 mb-4">
                    <!-- Username -->
                    <div>
                        <label for="username" class="block text-gray-600 mb-2">Username</label>
                        <input id="username" v-model="form.username" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Real Name -->
                    <div>
                        <label for="real-name" class="block text-gray-600 mb-2">Real Name</label>
                        <input id="real-name" v-model="form.real_name" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Email -->
                    <div>
                        <label for="email" class="block text-gray-600 mb-2">Email</label>
                        <input id="email" v-model="form.email" type="email"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Organization -->
                    <div>
                        <label for="organization" class="block text-gray-600 mb-2">Organization</label>
                        <input id="organization" v-model="form.organization" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Address -->
                    <div>
                        <label for="address" class="block text-gray-600 mb-2">Address</label>
                        <input id="address" v-model="form.address" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Mobile -->
                    <div>
                        <label for="mobile" class="block text-gray-600 mb-2">Mobile</label>
                        <input id="mobile" v-model="form.mobile" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>
                </div>

                <!-- 文件上傳 -->
                <div class="border-dashed border-2 border-gray-300 rounded-md p-6 text-center"
                    @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop">
                    <input type="file" ref="fileInput" class="hidden" @change="onFileSelected"
                        accept=".svg,.png,.jpg,.gif" />
                    <p class="text-gray-600">
                        Click to upload or drag and drop
                        <span class="text-blue-500 cursor-pointer" @click="onBrowse">Browse</span>
                    </p>
                    <p class="text-sm text-gray-400 mt-2">
                        SVG, PNG, JPG or GIF (max, 800x400px)
                    </p>
                    <p v-if="uploadFile" class="text-gray-600 mt-2">{{ uploadFile.name }}</p>
                </div>

                <!-- 動作按鈕 -->
                <div class="mt-6 flex justify-end space-x-4">
                    <button class="px-4 py-2 text-gray-600 bg-gray-200 rounded-md hover:bg-gray-300" @click="resetForm">
                        Cancel
                    </button>
                    <button class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700" @click="saveForm">
                        Save
                    </button>
                </div>
            </div>
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import LeftMenu from "@/components/LeftMenu.vue";
import axios from 'axios';

export default defineComponent({
    name: "SettingsPage",
    components: {
        LeftMenu,
    },
    setup() {
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: false },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: true },
        ]);

        const tabs = ref(["My details", "Profile", "Password", "Team", "Plan", "Billing", "Email", "Notifications"]);
        const activeTab = ref("My details");

        const authToken = ref(localStorage.getItem('token') || '');
        const userId = ref<number | null>(null);
        const defaultAvatar = "https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D";

        const form = ref({
            username: "",
            email: "",
            real_name: "",
            organization: "",
            address: "",
            mobile: "",
            avatar: ""
        });

        const uploadFile = ref<File | null>(null);
        const isDragging = ref(false);

        // 從後端獲取當前用戶資料
        const fetchUserData = async () => {
            try {
                const response = await axios.get('http://172.31.176.1:8000/auth/verify', {
                    headers: { Authorization: `Bearer ${authToken.value}` }
                });
                const userData = response.data.data; // 提取嵌套的 data 字段
                userId.value = userData.id;
                console.log(userId.value);
                form.value = {
                    username: userData.username,
                    email: userData.email,
                    real_name: userData.real_name || "",
                    organization: userData.organization || "",
                    address: userData.address || "",
                    mobile: userData.mobile || "",
                    avatar: userData.avatar || ""
                };
            } catch (error) {
                console.error('Failed to fetch user data:', error);
                localStorage.removeItem('token');
                // 可跳轉至登錄頁
            }
        };

        // 重置表單
        const resetForm = () => {
            fetchUserData(); // 重置為後端數據
            uploadFile.value = null;
        };

        // 保存表單
        const saveForm = async () => {
            try {
                const updateData = {
                    username: form.value.username,
                    email: form.value.email,
                    real_name: form.value.real_name || null,
                    organization: form.value.organization || null,
                    address: form.value.address || null,
                    mobile: form.value.mobile || null
                };
                await axios.put(`http://172.31.176.1:8000/users/${userId.value}`, updateData, {
                    headers: { Authorization: `Bearer ${authToken.value}` }
                });

                if (uploadFile.value) {
                    const formData = new FormData();
                    formData.append('file', uploadFile.value);
                    const uploadResponse = await axios.post('http://172.31.176.1:8000/file_uploads/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            'Authorization': `Bearer ${authToken.value}`
                        }
                    });
                    form.value.avatar = uploadResponse.data.file_path;
                    await axios.put(`http://172.31.176.1:8000/users/${userId.value}`, { avatar: form.value.avatar }, {
                        headers: { Authorization: `Bearer ${authToken.value}` }
                    });
                }

                alert("Settings saved successfully!");
            } catch (error) {
                console.error('Failed to save settings:', error);
                alert("Failed to save settings. Please try again.");
            }
        };

        // 文件拖曳與選擇
        const onDragOver = () => { isDragging.value = true; };
        const onDragLeave = () => { isDragging.value = false; };
        const onDrop = (event: DragEvent) => {
            isDragging.value = false;
            const file = event.dataTransfer?.files[0];
            if (file) uploadFile.value = file;
        };
        const onBrowse = () => {
            const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
            fileInput?.click();
        };
        const onFileSelected = (event: Event) => {
            const target = event.target as HTMLInputElement;
            const file = target.files?.[0];
            if (file) uploadFile.value = file;
        };

        // 在組件掛載時獲取用戶數據
        onMounted(() => {
            fetchUserData();
        });

        return {
            menuItems,
            tabs,
            activeTab,
            form,
            uploadFile,
            isDragging,
            defaultAvatar,
            resetForm,
            saveForm,
            onDragOver,
            onDragLeave,
            onDrop,
            onBrowse,
            onFileSelected,
        };
    },
});
</script>

<style scoped>
.bg-gray-100.active-drag {
    background-color: #f7fafc;
}
</style>