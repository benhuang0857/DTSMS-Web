<template>
    <div class="flex h-screen">
        <!-- 左側：表單 -->
        <div class="w-1/2 flex flex-col justify-center items-center bg-white">
            <div class="max-w-md w-full">
                <img src="../../public/images/logo.png" alt="Italian Trulli" />
                <h1 class="text-3xl font-bold text-black mb-4">DTSMS 數位傳輸安全管理系統</h1>
                <h3 class="text-2xl font-medium text-black mb-4">BAISHUO 佰碩科技</h3>
                <form @submit.prevent="handleLogin">
                    <div class="mb-4">
                        <label class="block text-xl mb-2" for="account">帳號</label>
                        <input
                            id="account"
                            type="text"
                            v-model="account"
                            placeholder="Enter your account"
                            class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-xl mb-2" for="password">密碼</label>
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
                        登入
                    </button>
                </form>
            </div>
        </div>

        <!-- 右側：圖片 -->
        <div
            class="w-1/2 bg-cover bg-center"
            style="background-image: url('../../public/images/dtsms-login-bg.jpg')"
        ></div>

        <!-- AlertDialog -->
        <AlertDialog
            :visible="dialogVisible"
            :title="dialogTitle"
            :message="dialogMessage"
            :loading="dialogLoading"
            @close="closeDialog"
        />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import AlertDialog from '@/components/AlertDialog.vue';

export default defineComponent({
    name: 'Login',
    components: {
        AlertDialog,
    },
    setup() {
        const account = ref('');
        const password = ref('');
        const token = ref('');
        const router = useRouter();

        const dialogVisible = ref(false);
        const dialogTitle = ref('');
        const dialogMessage = ref('');
        const dialogLoading = ref(false);

        const showDialog = (title: string, message: string, loading = false) => {
            dialogTitle.value = title;
            dialogMessage.value = message;
            dialogLoading.value = loading;
            dialogVisible.value = true;
        };

        const closeDialog = () => {
            dialogVisible.value = false;
        };

        const handleLogin = async () => {
            showDialog('登入中', '請稍候…', true);

            try {
                const response = await axios.post('http://172.31.176.1:8000/api/auth', {
                    email: account.value,
                    password: password.value,
                });
                token.value = response.data.access_token;
                localStorage.setItem('token', token.value);

                showDialog('登入成功', `歡迎您, ${account.value}!`);
                setTimeout(() => {
                    closeDialog();
                    router.push('/dashboard');
                }, 1500);
            } catch (error) {
                showDialog('登入失敗', '錯誤帳號或是密碼, 請重試!');
                console.error('Login failed:', error);
            }
        };

        return {
            account,
            password,
            token,
            handleLogin,
            dialogVisible,
            dialogTitle,
            dialogMessage,
            dialogLoading,
            closeDialog,
        };
    },
});
</script>

<style scoped>
/* 如果需要自定義樣式，可以在這裡添加 */
</style>
