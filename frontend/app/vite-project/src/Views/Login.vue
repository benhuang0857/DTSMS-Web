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
            <input id="account" type="text" v-model="account" placeholder="Enter your account"
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500" />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2" for="password">
              Password
            </label>
            <input id="password" type="password" v-model="password" placeholder="Enter your password"
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500" />
          </div>
          <button type="submit" class="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition">
            Login
          </button>
        </form>
      </div>
    </div>

    <!-- 右側：圖片 -->
    <div class="w-1/2 bg-cover bg-center"
      style="background-image: url('https://mediaproxy.salon.com/width/1200/https://media2.salon.com/2021/02/romanesco-broccoli-0209212.jpg')">
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'App',
  setup() {
    const account = ref('');
    const password = ref('');
    const token = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      try {
        const response = await axios.post('http://172.31.176.1:8000/auth', {
          email: account.value,
          password: password.value,
        });
        token.value = response.data.access_token;
        localStorage.setItem('token', token.value);
        alert(`歡迎您, ${account.value}!`);
        router.push('/dashboard');
      } catch (error) {
        alert('錯誤帳號或是密碼, 請重試!');
        console.error('Login failed:', error);
      }
    };

    return {
      account,
      password,
      token,
      handleLogin,
    };
  },
});
</script>

<style scoped>
/* 如果需要自定義樣式，可以在這裡添加 */
</style>