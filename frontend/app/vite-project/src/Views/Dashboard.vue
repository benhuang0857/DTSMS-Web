<template>
  <div class="flex h-screen">
    <!-- 左側菜單 -->
    <LeftMenu :menuItems="menuItems" />

    <!-- 主內容 -->
    <main class="flex-1 bg-gray-100 p-6">
      <header class="mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
      </header>
      <!-- 這裡可以添加其他內容 -->
      <p class="text-gray-600">Welcome to the Dashboard. Customize this section as needed.</p>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import LeftMenu from '@/components/LeftMenu.vue';

export default defineComponent({
  name: 'Dashboard',
  components: { LeftMenu },
  setup() {
    const menuItems = ref([
      { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
      { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
      { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
      { label: 'Submission', link: '/submission', icon: 'fas fa-upload', active: false },
      { label: 'Setting', link: '/settings', icon: 'fas fa-cog', active: false },
    ]);

    return { menuItems };
  },
});
</script>