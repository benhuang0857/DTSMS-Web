<template>
    <div class="flex h-screen">
        <LeftMenu :menuItems="menuItems" />
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
                            <th class="p-2">Token</th>
                            <th class="p-2">File Name</th>
                            <th class="p-2">Date</th>
                            <th class="p-2">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="row in filteredData" :key="row.id" class="hover:bg-gray-50 border-b">
                            <td class="p-2">#{{ row.trackingId }}</td>
                            <td class="p-2">{{ row.token }}</td>
                            <td class="p-2">{{ row.fileName }}</td>
                            <td class="p-2">{{ row.date }}</td>
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
import { defineComponent, ref, computed } from "vue";
import LeftMenu from '@/components/LeftMenu.vue';

export default defineComponent({
    name: "TablePage",
    components: {
        LeftMenu,
    },
    setup() {
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const entries = ref(10);
        const search = ref("");
        const currentPage = ref(1);

        const data = ref([
            {
                id: 1,
                trackingId: 20462,
                fileName: "Vendor01",
                token: "TWTWT1089TWT1089",
                date: "13/05/2022",
                status: "Completed",
            }
        ]);

        const totalPages = computed(() => Math.ceil(data.value.length / entries.value));
        const filteredData = computed(() =>
            data.value.filter((item) =>
                item.fileName.toLowerCase().includes(search.value.toLowerCase())
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

        return {
            menuItems,
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