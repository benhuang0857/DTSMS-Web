<template>
    <div class="flex h-screen">
      <!-- 左側：表單 -->
      <div class="w-1/2 flex flex-col justify-center items-center bg-white">
        <div class="max-w-md w-full">
          <h1 class="text-3xl font-bold text-black mb-4">DTSMS</h1>
          <p class="text-gray-500 mb-8">
            Enter your Credentials to access your account
          </p>
          <form @submit.prevent="handleLogin">
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2" for="account">
                Account
              </label>
              <input
                id="account"
                type="text"
                v-model="account"
                placeholder="Enter your account"
                class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2" for="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                v-model="password"
                placeholder="Enter your password"
                class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <button
              type="submit"
              class="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
            >
              Login
            </button>
          </form>
        </div>
      </div>
  
      <!-- 右側：圖片 -->
      <div
        class="w-1/2 bg-cover bg-center"
        style="background-image: url('https://mediaproxy.salon.com/width/1200/https://media2.salon.com/2021/02/romanesco-broccoli-0209212.jpg')"
      ></div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    name: 'App',
    setup() {
      const account = ref('');
      const password = ref('');
  
      const handleLogin = () => {
        console.log('Account:', account.value);
        console.log('Password:', password.value);
      };
  
      return {
        account,
        password,
        handleLogin,
      };
    },
  });
  </script>
  
  <style scoped>
  /* 如果需要自定義樣式，可以在這裡添加 */
  </style>
  