<template>
    <div class="flex h-screen">
        <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />

        <main class="flex-1 bg-gray-100 p-6">
            <div class="relative">
                <div class="h-40 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg"></div>
                <div class="absolute top-24 left-6 flex items-center space-x-4">
                    <img :src="getAvatarUrl(form.avatar) || defaultAvatar" alt="User Avatar"
                        class="w-20 h-20 rounded-full border-4 border-white" />
                    <div>
                        <h1 class="text-2xl font-bold text-gray-800">Settings</h1>
                    </div>
                </div>
            </div>

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

            <UserSettingsForm v-if="activeTab === 'My details'" :form="form" :uploadFile="uploadFile"
                :onDragOver="onDragOver" :onDragLeave="onDragLeave" :onDrop="onDrop" :onBrowse="onBrowse"
                :onFileSelected="onFileSelected" :resetForm="resetForm" :saveForm="saveForm" />

            <WebSettingForm v-else-if="activeTab === 'Web Setting'" />
            <div v-else>
                <p>Library Setting content here…</p>
            </div>
        </main>
    </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import LeftMenu from "@/components/LeftMenu.vue";
import UserSettingsForm from "@/components/forms/UserSettingsForm.vue";
import WebSettingForm from "../components/forms/WebSettingForm.vue";
import axios from "axios";

export default defineComponent({
    name: "SettingsPage",
    components: {
        LeftMenu,
        UserSettingsForm,
        WebSettingForm,
    },
    setup() {
        const menuItems = ref([
            { label: "Dashboard", link: "/dashboard", icon: "fas fa-tachometer-alt", active: false },
            { label: "Automation Control", link: "/automation", icon: "fas fa-robot", active: false },
            { label: "Download History", link: "/downloads", icon: "fas fa-download", active: false },
            { label: "Submission", link: "/submissions", icon: "fas fa-upload", active: false },
            { label: "Setting", link: "/setting", icon: "fas fa-cog", active: true },
        ]);

        const tabs = ref(["My details", "Web Setting", "Library Setting"]);
        const activeTab = ref("My details");

        const authToken = ref(localStorage.getItem("token") || "");
        const userId = ref<number | null>(null);
        const defaultAvatar =
            "https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D";

        const form = ref({
            username: "",
            email: "",
            real_name: "",
            organization: "",
            address: "",
            mobile: "",
            avatar: "",
        });

        const userInfo = ref<{
            id: number;
            account: string;
            email: string;
            real_name?: string;
            avatar?: string;
        } | null>(null);

        const uploadFile = ref<File | null>(null);
        const isDragging = ref(false);

        const fetchUserData = async () => {
            try {
                const response = await axios.get("http://172.31.176.1:8000/api/auth/verify", {
                    headers: { Authorization: `Bearer ${authToken.value}` },
                });
                const userData = response.data.data;
                userId.value = userData.id;
                
                // 更新表單資料
                form.value = {
                    username: userData.account,
                    email: userData.email,
                    real_name: userData.real_name || "",
                    organization: userData.organization || "",
                    address: userData.address || "",
                    mobile: userData.mobile || "",
                    avatar: userData.avatar || "",
                };
                
                // 更新用戶資料給 LeftMenu 使用
                userInfo.value = {
                    id: userData.id,
                    account: userData.account,
                    email: userData.email,
                    real_name: userData.real_name,
                    avatar: userData.avatar,
                };
            } catch (error) {
                console.error("Failed to fetch user data:", error);
                localStorage.removeItem("token");
            }
        };

        const resetForm = () => {
            fetchUserData();
            uploadFile.value = null;
        };

        const saveForm = async () => {
            try {
                // 先處理avatar上傳 (如果有的話)
                if (uploadFile.value) {
                    const formData = new FormData();
                    formData.append("file", uploadFile.value);
                    const avatarResponse = await axios.post(`http://172.31.176.1:8000/api/users/${userId.value}/avatar`, formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                            Authorization: `Bearer ${authToken.value}`,
                        },
                    });
                    form.value.avatar = avatarResponse.data.avatar;
                }

                // 然後更新其他用戶資料 (不包含avatar，因為已經單獨處理)
                const updateData = {
                    account: form.value.username,
                    email: form.value.email,
                    real_name: form.value.real_name || null,
                    organization: form.value.organization || null,
                    address: form.value.address || null,
                    mobile: form.value.mobile || null,
                    status: "active",
                };
                await axios.put(`http://172.31.176.1:8000/api/users/${userId.value}`, updateData, {
                    headers: { Authorization: `Bearer ${authToken.value}` },
                });

                alert("Settings saved successfully!");
            } catch (error: any) {
                console.error("Failed to save settings:", error);
                if (error.response) {
                    console.error("Response data:", error.response.data);
                    console.error("Response status:", error.response.status);
                    alert(`Failed to save settings: ${error.response.data.detail?.message || error.response.data.detail || 'Unknown error'}`);
                } else {
                    alert("Failed to save settings. Please try again.");
                }
            }
        };

        const onDragOver = () => {
            isDragging.value = true;
        };
        const onDragLeave = () => {
            isDragging.value = false;
        };
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

        const getAvatarUrl = (avatarPath: string | null) => {
            if (!avatarPath) return null;
            // 如果已經是完整URL，直接返回
            if (avatarPath.startsWith('http')) return avatarPath;
            // 否則加上後端基礎URL
            return `http://172.31.176.1:8000/${avatarPath}`;
        };

        onMounted(() => {
            fetchUserData();
        });

        return {
            menuItems,
            tabs,
            activeTab,
            form,
            userInfo,
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
            getAvatarUrl,
        };
    },
});
</script>
