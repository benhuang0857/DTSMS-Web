<template>
    <div class="flex h-screen">
        <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />
        <main class="flex-1 p-6">
            <!-- 控制區域 -->
            <div class="flex justify-between items-center mb-4">
                <!-- Show entries -->
                <div class="flex items-center">
                    <label for="entries" class="text-gray-600 mr-2">Show</label>
                    <select id="entries" class="border border-gray-300 rounded-md p-2" v-model="entries">
                        <option value="10">10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                    </select>
                    <span class="ml-2 text-gray-600">entries</span>
                    <button @click="fetchData" class="ml-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
                        重新整理
                    </button>
                </div>

                <!-- Search -->
                <div>
                    <input type="text" placeholder="Search..." v-model="search"
                        class="border border-gray-300 rounded-md p-2 w-64" />
                </div>
            </div>

            <!-- 數據表格 -->
            <div class="overflow-x-auto border border-gray-200 rounded-lg">
                <table class="table-auto w-full text-left">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="p-2">Tracking ID</th>
                            <th class="p-2">Step Name</th>
                            <th class="p-2">Start Time</th>
                            <th class="p-2">File Name</th>
                            <th class="p-2">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="row in paginatedData" :key="row.id" class="hover:bg-gray-50 border-b">
                            <td class="p-2">{{ row.tracking_id || 'N/A' }}</td>
                            <td class="p-2">{{ row.step_name || 'N/A' }}</td>
                            <td class="p-2">{{ formatDate(row.start_time) }}</td>
                            <td class="p-2">{{ row.uploaded_file_name }}</td>
                            <td class="p-2">
                                <span :class="statusClass(row.status)" class="px-2 py-1 rounded-md text-white">
                                    {{ row.status }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 分頁器 -->
            <div class="flex justify-between items-center mt-4">
                <button @click="prevPage" class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md hover:bg-gray-300"
                    :disabled="currentPage === 1">
                    Previous
                </button>
                <div class="space-x-2">
                    <button v-for="page in totalPages" :key="page" @click="goToPage(page)" class="px-3 py-1 rounded-md"
                        :class="{
                            'bg-purple-500 text-white': page === currentPage,
                            'bg-gray-200 text-gray-600 hover:bg-gray-300': page !== currentPage,
                        }">
                        {{ page }}
                    </button>
                </div>
                <button @click="nextPage" class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md hover:bg-gray-300"
                    :disabled="currentPage === totalPages">
                    Next
                </button>
            </div>
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import LeftMenu from '@/components/LeftMenu.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: "TablePage",
    components: {
        LeftMenu,
    },
    setup() {
        const router = useRouter();
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: false },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: true },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const entries = ref(10);
        const search = ref("");
        const currentPage = ref(1);
        const data = ref<any[]>([]); // 儲存從 API 獲取的數據
        
        const userInfo = ref<{
            id: number;
            account: string;
            email: string;
            real_name?: string;
            avatar?: string;
        } | null>(null);

        // 驗證身份並獲取用戶資料
        const checkAuth = async () => {
            const authToken = localStorage.getItem('token');
            if (!authToken) {
                router.push('/');
                return;
            }
            try {
                const response = await axios.get('http://172.31.176.1:8000/api/auth/verify', {
                    headers: { Authorization: `Bearer ${authToken}` }
                });
                if (response.status === 200) {
                    const userData = response.data.data;
                    
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

        // 從後端獲取數據
        const fetchData = async () => {
            try {
                const response = await axios.get('http://172.31.176.1:8000/api/file-trackings/', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token') || ''}`
                    }
                });
                data.value = response.data;
            } catch (error) {
                console.error('Failed to fetch file uploads:', error);
            }
        };

        // 在組件掛載時獲取數據和驗證身份
        onMounted(() => {
            checkAuth();
            fetchData();
        });

        // 計算總頁數
        const totalPages = computed(() => Math.ceil(filteredData.value.length / entries.value));

        // 過濾數據（基於搜索）
        const filteredData = computed(() =>
            data.value.filter((item) =>
                item.uploaded_file_name?.toLowerCase().includes(search.value.toLowerCase()) ||
                item.step_name?.toLowerCase().includes(search.value.toLowerCase()) ||
                item.tracking_id?.toString().toLowerCase().includes(search.value.toLowerCase())
            )
        );

        // 分頁數據
        const paginatedData = computed(() => {
            const start = (currentPage.value - 1) * entries.value;
            const end = start + entries.value;
            return filteredData.value.slice(start, end);
        });

        // 分頁控制
        const goToPage = (page: number) => (currentPage.value = page);
        const prevPage = () => {
            if (currentPage.value > 1) currentPage.value--;
        };
        const nextPage = () => {
            if (currentPage.value < totalPages.value) currentPage.value++;
        };

        // 狀態顏色
        const statusClass = (status: string) => {
            switch (status) {
                case "success":
                    return "bg-green-500";
                case "error":
                    return "bg-red-500";
                case "dangerous":
                    return "bg-red-700";
                case "in_progress":
                    return "bg-yellow-500";
                case "pending":
                    return "bg-blue-500";
                default:
                    return "bg-gray-500";
            }
        };

        // 格式化日期
        const formatDate = (dateString: string | null) => {
            if (!dateString) return 'N/A';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
        };

        return {
            menuItems,
            userInfo,
            entries,
            search,
            currentPage,
            totalPages,
            filteredData,
            paginatedData,
            goToPage,
            prevPage,
            nextPage,
            statusClass,
            formatDate,
            fetchData,
        };
    },
});
</script>