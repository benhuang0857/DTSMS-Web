import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue'; // 確保這裡是正確的路徑
import Dashboard from '@/views/Dashboard.vue';
import Download from '@/views/Download.vue';
import Submission from '@/views/Submission.vue';
import Setting from '@/views/Setting.vue';

const routes = [
  {
    path: '/', // 根路徑顯示 Login 頁面
    name: 'Login',
    component: Login,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/downloads',
    name: 'Download',
    component: Download,
  },
  {
    path: '/submissions',
    name: 'Submission',
    component: Submission,
  },
  {
    path: '/setting',
    name: 'Setting',
    component: Setting,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
