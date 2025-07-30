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
                            <th class="p-2">User</th>
                            <th class="p-2">Token</th>
                            <th class="p-2">Date</th>
                            <th class="p-2">From</th>
                            <th class="p-2">Status</th>
                            <th class="p-2">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="row in filteredData" :key="row.id" class="hover:bg-gray-50 border-b">
                            <td class="p-2">#{{ row.trackingId }}</td>
                            <td class="p-2 flex items-center">
                                <img :src="row.userAvatar" alt="User Avatar" class="w-8 h-8 rounded-full mr-2" />
                                {{ row.userName }}
                            </td>
                            <td class="p-2">{{ row.token }}</td>
                            <td class="p-2">{{ row.date }}</td>
                            <td class="p-2">{{ row.from }}</td>
                            <td class="p-2">
                                <span :class="statusClass(row.status)" class="px-2 py-1 rounded-md text-white">
                                    {{ row.status }}
                                </span>
                            </td>
                            <td class="p-2 flex space-x-2">
                                <button class="text-gray-500 hover:text-gray-700">
                                    <i class="fas fa-file-alt"></i>
                                </button>
                                <button class="text-yellow-500 hover:text-yellow-700">
                                    <i class="fas fa-exclamation-triangle"></i>
                                </button>
                                <button class="text-green-500 hover:text-green-700">
                                    <i class="fas fa-download"></i>
                                </button>
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
import { useRouter } from 'vue-router';
import axios from 'axios';
import LeftMenu from '@/components/LeftMenu.vue';

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
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: true },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const authToken = ref(localStorage.getItem('token') || '');
        const userInfo = ref<{
            id: number;
            account: string;
            email: string;
            real_name?: string;
            avatar?: string;
        } | null>(null);

        const entries = ref(10);
        const search = ref("");
        const currentPage = ref(1);

        const data = ref([
            {
                id: 1,
                trackingId: 20462,
                userName: "User01",
                userAvatar: "https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D",
                token: "TWTWT1089TWT1089",
                date: "13/05/2022",
                from: "Vendor01",
                status: "Completed",
            },
            {
                id: 2,
                trackingId: 18933,
                userName: "User02",
                userAvatar: "https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D",
                token: "FGSW1SDf9T",
                date: "22/05/2022",
                from: "Vendor02",
                status: "Failed",
            },
            {
                id: 3,
                trackingId: 45169,
                userName: "User03",
                userAvatar: "https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D",
                token: "FGSsdF1sd9F",
                date: "15/06/2022",
                from: "Vendor02",
                status: "Process",
            },
        ]);

        const totalPages = computed(() => Math.ceil(data.value.length / entries.value));
        const filteredData = computed(() =>
            data.value.filter((item) =>
                item.userName.toLowerCase().includes(search.value.toLowerCase())
            )
        );

        const goToPage = (page: number) => (currentPage.value = page);
        const prevPage = () => {
            if (currentPage.value > 1) currentPage.value--;
        };
        const nextPage = () => {
            if (currentPage.value < totalPages.value) currentPage.value++;
        };

        const statusClass = (status: string) => {
            switch (status) {
                case "Completed":
                    return "bg-green-500";
                case "Failed":
                    return "bg-red-500";
                case "Process":
                    return "bg-yellow-500";
                default:
                    return "bg-gray-500";
            }
        };

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

        onMounted(() => {
            checkAuth();
        });

        return {
            menuItems,
            userInfo,
            entries,
            search,
            currentPage,
            totalPages,
            filteredData,
            goToPage,
            prevPage,
            nextPage,
            statusClass,
        };
    },
});
</script>