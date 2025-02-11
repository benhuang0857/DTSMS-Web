<template>
    <div class="flex h-screen">
        <!-- 左側菜單 -->
        <LeftMenu :menuItems="menuItems" />

        <!-- 主內容 -->
        <main class="flex-1 bg-gray-100 p-6">
            <!-- 頂部區域 -->
            <div class="relative">
                <!-- 背景圖 -->
                <div class="h-40 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg"></div>

                <!-- 頭像與標題 -->
                <div class="absolute top-24 left-6 flex items-center space-x-4">
                    <img src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D" alt="User Avatar"
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
                    <!-- First name -->
                    <div>
                        <label for="first-name" class="block text-gray-600 mb-2">First name</label>
                        <input id="first-name" v-model="form.firstName" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>

                    <!-- Last name -->
                    <div>
                        <label for="last-name" class="block text-gray-600 mb-2">Last name</label>
                        <input id="last-name" v-model="form.lastName" type="text"
                            class="w-full border border-gray-300 rounded-md p-2" />
                    </div>
                </div>

                <!-- Email -->
                <div class="mb-4">
                    <label for="email" class="block text-gray-600 mb-2">Email</label>
                    <input id="email" v-model="form.email" type="email"
                        class="w-full border border-gray-300 rounded-md p-2" />
                </div>

                <!-- 文件上傳 -->
                <div class="border-dashed border-2 border-gray-300 rounded-md p-6 text-center">
                    <p class="text-gray-600">
                        Click to upload or drag and drop
                    </p>
                    <p class="text-sm text-gray-400 mt-2">
                        SVG, PNG, JPG or GIF (max, 800x400px)
                    </p>
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
import { defineComponent, ref } from "vue";
import LeftMenu from "@/components/LeftMenu.vue";

export default defineComponent({
    name: "SettingsPage",
    components: {
        LeftMenu,
    },
    setup() {
        // 側邊欄數據
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        // 子選單
        const tabs = ref(["My details", "Profile", "Password", "Team", "Plan", "Billing", "Email", "Notifications"]);
        const activeTab = ref("My details");

        // 表單數據
        const form = ref({
            firstName: "Killan",
            lastName: "James",
            email: "killanjames@gmail.com",
        });

        // 重置表單
        const resetForm = () => {
            form.value = {
                firstName: "",
                lastName: "",
                email: "",
            };
        };

        // 保存表單
        const saveForm = () => {
            alert("Form saved!");
        };

        return {
            menuItems,
            tabs,
            activeTab,
            form,
            resetForm,
            saveForm,
        };
    },
});
</script>