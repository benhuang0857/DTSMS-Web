<template>
  <div class="flex min-h-screen" v-if="isAuthenticated">
    <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />
    
    <main class="flex-1 flex flex-col">
      <div class="recipe-management-container">
        <!-- Page Header -->
        <div class="page-header">
          <h1 class="text-3xl font-bold text-gray-800">Recipe Management</h1>
          <p class="text-gray-600 mt-2">管理和配置你的自動化食譜</p>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
          <div class="toolbar-left">
            <div class="search-box">
              <i class="fas fa-search"></i>
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="搜索 Recipe..." 
                class="search-input"
              />
            </div>
            <select v-model="statusFilter" class="filter-select">
              <option value="">所有狀態</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
            <select v-model="libraryFilter" class="filter-select">
              <option value="">所有 Library</option>
              <option v-for="library in libraries" :key="library.id" :value="library.id">
                {{ library.name }}
              </option>
            </select>
          </div>
          <div class="toolbar-right">
            <button @click="loadRecipes" class="btn btn-secondary" :disabled="loading">
              <i class="fas fa-refresh" :class="{ 'fa-spin': loading }"></i>
              刷新
            </button>
            <button @click="showAddRecipeModal = true" class="btn btn-primary">
              <i class="fas fa-plus"></i>
              新增 Recipe
            </button>
          </div>
        </div>

        <!-- Recipe Cards Grid -->
        <div class="recipes-grid" v-if="!loading">
          <RecipeCard
            v-for="recipe in filteredRecipes"
            :key="recipe.id"
            :recipe="recipe"
            @edit="editRecipe"
            @delete="deleteRecipe"
            @view="viewRecipe"
          />
          
          <!-- Empty State -->
          <div v-if="filteredRecipes.length === 0" class="empty-state">
            <i class="fas fa-utensils text-6xl text-gray-300 mb-4"></i>
            <h3 class="text-xl text-gray-500 mb-2">沒有找到 Recipe</h3>
            <p class="text-gray-400">{{ searchQuery ? '嘗試調整搜索條件' : '開始創建你的第一個 Recipe' }}</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i>
          <p class="mt-4 text-gray-600">載入中...</p>
        </div>
      </div>
    </main>

    <!-- Add/Edit Recipe Modal -->
    <div v-if="showAddRecipeModal || editingRecipe" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingRecipe ? '編輯 Recipe' : '新增 Recipe' }}</h3>
          <button @click="closeModal" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitRecipe">
            <div class="form-group">
              <label>關聯的 Library</label>
              <select v-model="recipeForm.library_id" class="form-control">
                <option :value="null">選擇 Library（可選）</option>
                <option v-for="library in libraries" :key="library.id" :value="library.id">
                  {{ library.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>名稱 <span class="required">*</span></label>
              <input v-model="recipeForm.name" type="text" class="form-control" required>
            </div>
            <div class="form-group">
              <label>描述</label>
              <textarea v-model="recipeForm.description" class="form-control" rows="3" placeholder="輸入 Recipe 的詳細描述..."></textarea>
            </div>
            <div class="form-group">
              <label>狀態</label>
              <select v-model="recipeForm.status" class="form-control">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="form-group">
              <label class="flex items-center">
                <input v-model="recipeForm.allow_parallel_autoflows" type="checkbox" class="mr-2">
                允許平行執行 Autoflows
              </label>
            </div>
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                <i v-if="submitting" class="fas fa-spinner fa-spin mr-2"></i>
                {{ editingRecipe ? '更新' : '創建' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deletingRecipe" class="modal-overlay" @click="deletingRecipe = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>確認刪除</h3>
          <button @click="deletingRecipe = null" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <p>確定要刪除 Recipe "<strong>{{ deletingRecipe.name }}</strong>" 嗎？</p>
          <p class="text-sm text-red-600 mt-2">此操作將會刪除相關的 Autoflows 和 Processing Steps，且無法復原。</p>
          <div class="form-actions mt-6">
            <button @click="deletingRecipe = null" class="btn btn-secondary">取消</button>
            <button @click="confirmDelete" class="btn btn-danger" :disabled="submitting">
              <i v-if="submitting" class="fas fa-spinner fa-spin mr-2"></i>
              確認刪除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex h-screen justify-center items-center">
    <p>正在驗證身份或跳轉至登錄頁面...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import LeftMenu from '@/components/LeftMenu.vue';
import RecipeCard from '@/components/RecipeCard.vue';

// Authentication and routing
const router = useRouter();
const authToken = ref(localStorage.getItem('token') || '');
const isAuthenticated = ref(false);

// User data
const userInfo = ref<{
  id: number;
  account: string;
  email: string;
  real_name?: string;
  avatar?: string;
} | null>(null);

// Menu items
const menuItems = ref([
  { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: false },
  { label: 'Recipe Management', link: '/recipe-management', icon: 'fas fa-utensils', active: true },
  { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
  { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
  { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
  { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
]);

// Data
const recipes = ref<any[]>([]);
const libraries = ref<any[]>([]);
const loading = ref(false);
const submitting = ref(false);

// Filters
const searchQuery = ref('');
const statusFilter = ref('');
const libraryFilter = ref('');

// Modals
const showAddRecipeModal = ref(false);
const editingRecipe = ref<any>(null);
const deletingRecipe = ref<any>(null);

// Form
const recipeForm = ref({
  library_id: null,
  name: '',
  description: '',
  status: 'active',
  allow_parallel_autoflows: false,
  recipe_steps: []
});

// Computed
const filteredRecipes = computed(() => {
  return recipes.value.filter(recipe => {
    const matchesSearch = !searchQuery.value || 
      recipe.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      recipe.description?.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesStatus = !statusFilter.value || recipe.status === statusFilter.value;
    
    const matchesLibrary = !libraryFilter.value || recipe.library_id === parseInt(libraryFilter.value);
    
    return matchesSearch && matchesStatus && matchesLibrary;
  });
});

// Authentication check
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
      isAuthenticated.value = true;
      const userData = response.data.data;
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

// Load data
const loadRecipes = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://172.31.176.1:8000/api/recipes', {
      headers: { Authorization: `Bearer ${authToken.value}` }
    });
    recipes.value = response.data;
  } catch (error) {
    console.error('載入 Recipes 失敗:', error);
  } finally {
    loading.value = false;
  }
};

const loadLibraries = async () => {
  try {
    const response = await axios.get('http://172.31.176.1:8000/api/libraries', {
      headers: { Authorization: `Bearer ${authToken.value}` }
    });
    libraries.value = response.data;
  } catch (error) {
    console.error('載入 Libraries 失敗:', error);
  }
};

// CRUD operations
const editRecipe = (recipe: any) => {
  editingRecipe.value = recipe;
  recipeForm.value = { ...recipe };
  showAddRecipeModal.value = false;
};

const deleteRecipe = (recipe: any) => {
  deletingRecipe.value = recipe;
};

const viewRecipe = (recipe: any) => {
  // Navigate to automation page with recipe ID as query parameter
  router.push({
    path: '/automation',
    query: { recipeId: recipe.id }
  });
};

const submitRecipe = async () => {
  submitting.value = true;
  try {
    if (editingRecipe.value) {
      await axios.put(`http://172.31.176.1:8000/api/recipes/${editingRecipe.value.id}`, recipeForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    } else {
      await axios.post('http://172.31.176.1:8000/api/recipes', recipeForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    }
    
    closeModal();
    await loadRecipes();
  } catch (error) {
    console.error('Recipe 操作失敗:', error);
  } finally {
    submitting.value = false;
  }
};

const confirmDelete = async () => {
  if (!deletingRecipe.value) return;
  
  submitting.value = true;
  try {
    await axios.delete(`http://172.31.176.1:8000/api/recipes/${deletingRecipe.value.id}`, {
      headers: { Authorization: `Bearer ${authToken.value}` }
    });
    
    deletingRecipe.value = null;
    await loadRecipes();
  } catch (error) {
    console.error('刪除 Recipe 失敗:', error);
  } finally {
    submitting.value = false;
  }
};

const closeModal = () => {
  showAddRecipeModal.value = false;
  editingRecipe.value = null;
  recipeForm.value = {
    library_id: null,
    name: '',
    description: '',
    status: 'active',
    allow_parallel_autoflows: false,
    recipe_steps: []
  };
};

// Lifecycle
onMounted(async () => {
  await checkAuth();
  if (isAuthenticated.value) {
    await Promise.all([loadRecipes(), loadLibraries()]);
  }
});
</script>

<style scoped>
.recipe-management-container {
  @apply flex flex-col bg-gray-50 min-h-screen;
}

.page-header {
  @apply p-6 bg-white shadow-sm border-b;
}

.toolbar {
  @apply flex justify-between items-center p-4 bg-white shadow-sm border-b gap-4;
}

.toolbar-left {
  @apply flex items-center gap-3;
}

.toolbar-right {
  @apply flex items-center gap-2;
}

.search-box {
  @apply relative;
}

.search-box i {
  @apply absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400;
}

.search-input {
  @apply pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-w-64;
}

.filter-select {
  @apply px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white;
}

.recipes-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6;
}

.empty-state {
  @apply col-span-full flex flex-col items-center justify-center py-16;
}

.loading-state {
  @apply flex flex-col items-center justify-center py-16;
}

.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center gap-2;
}

.btn-primary {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.btn-secondary {
  @apply bg-gray-500 text-white hover:bg-gray-600;
}

.btn-danger {
  @apply bg-red-500 text-white hover:bg-red-600;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg shadow-xl max-w-lg w-full mx-4;
}

.modal-header {
  @apply flex justify-between items-center p-4 border-b;
}

.btn-close {
  @apply text-gray-500 hover:text-gray-700 text-xl;
}

.modal-body {
  @apply p-4;
}

.form-group {
  @apply mb-4;
}

.form-group label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-control {
  @apply w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

.required {
  @apply text-red-500;
}

.form-actions {
  @apply flex justify-end gap-2 mt-6;
}
</style>