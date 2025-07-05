<template>
    <aside class="bg-gray-800 text-gray-300 w-60 min-h-screen flex flex-col">
        <!-- 用戶信息 -->
        <div class="flex items-center px-4 py-6">
            <img src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1hbiUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D"
                alt="User Image" class="w-12 h-12 rounded-full mr-4" />
            <div>
                <p class="text-lg font-semibold">Alexander Pierce</p>
            </div>
        </div>

        <!-- 菜單列表 -->
        <nav class="flex-1 px-2 space-y-2">
            <ul>
                <li v-for="(item, index) in menuItems" :key="index" class="group">
                    <router-link :to="item.link"
                        class="flex items-center px-4 py-2 text-sm rounded-lg hover:bg-gray-700 hover:text-white transition"
                        :class="{ 'bg-gray-700 text-white font-bold': item.active }">
                        <i :class="item.icon" class="mr-3"></i>
                        {{ item.label }}
                    </router-link>
                </li>
            </ul>
        </nav>
    </aside>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

// 定義菜單項目類型
interface MenuItem {
    label: string;
    link: string;
    icon: string;
    active: boolean;
}

export default defineComponent({
    name: 'LeftMenu',
    props: {
        menuItems: {
            type: Array as PropType<MenuItem[]>,
            required: true,
        },
    },
});
</script>

<style scoped>
/* 你可以根據需要添加更多自定義樣式 */
</style>
