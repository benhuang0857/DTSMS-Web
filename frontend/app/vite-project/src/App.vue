<template>
  <div id="app" class="h-screen flex flex-col">
    <header
      v-if="showTopBar"
      class="bg-gray-800 text-white py-4 px-6 flex justify-between items-center"
    >
      <h1 class="text-lg font-semibold">My Application</h1>
      <nav>
        <router-link to="/" class="mr-4 text-white hover:underline">Login</router-link>
        <router-link to="/dashboard" class="text-white hover:underline">Dashboard</router-link>
      </nav>
    </header>

    <!-- 路由出口 -->
    <main class="flex-1 bg-gray-100">
      <router-view />
    </main>

    <!-- 頁腳 -->
    <footer 
      v-if="showTopBar"
      class="bg-gray-800 text-white text-center py-4">
      &copy; 2025 My Application. All rights reserved.
    </footer>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router'; // 引入 useRoute

export default defineComponent({
  name: "App",
  setup() {
    const route = useRoute();

    // 根據路由判斷是否顯示導航欄
    const showTopBar = route.path !== '/';

    return { showTopBar };
  },
});
</script>

<style>
/* 全局樣式 */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
