<template>
  <div class="recipe-card">
    <div class="card-header">
      <div class="recipe-icon">
        <i class="fas fa-utensils"></i>
      </div>
      <div class="status-badge" :class="statusClass">
        {{ recipe.status === 'active' ? 'Active' : 'Inactive' }}
      </div>
    </div>
    
    <div class="card-body">
      <h3 class="recipe-title" :title="recipe.name">
        {{ recipe.name }}
      </h3>
      
      <p class="recipe-description" v-if="recipe.description" :title="recipe.description">
        {{ truncatedDescription }}
      </p>
      <p class="recipe-description text-gray-400 italic" v-else>
        沒有描述
      </p>
      
      <div class="recipe-info">
        <div class="info-item" v-if="recipe.library_name">
          <i class="fas fa-cube text-blue-500"></i>
          <span class="info-text">{{ recipe.library_name }}</span>
        </div>
        <div class="info-item" v-else>
          <i class="fas fa-cube text-gray-400"></i>
          <span class="info-text text-gray-400">No Library</span>
        </div>
        
        <div class="info-item">
          <i class="fas fa-project-diagram text-green-500"></i>
          <span class="info-text">{{ recipe.autoflows_count || 0 }} Autoflows</span>
        </div>
        
        <div class="info-item">
          <i class="fas fa-list-ol text-purple-500"></i>
          <span class="info-text">{{ recipe.recipe_steps_count || 0 }} Steps</span>
        </div>
        
        <div class="info-item">
          <i class="fas fa-clock text-gray-500"></i>
          <span class="info-text">{{ formatDate(recipe.updated_time) }}</span>
        </div>
        
        <div class="info-item" v-if="recipe.allow_parallel_autoflows">
          <i class="fas fa-code-branch text-orange-500"></i>
          <span class="info-text">Parallel</span>
        </div>
      </div>
    </div>
    
    <div class="card-actions">
      <button @click="$emit('view', recipe)" class="action-btn view-btn" title="在自動化畫布中查看此 Recipe">
        <i class="fas fa-project-diagram"></i>
        View in Canvas
      </button>
      <button @click="$emit('edit', recipe)" class="action-btn edit-btn" title="編輯">
        <i class="fas fa-edit"></i>
        Edit
      </button>
      <button @click="$emit('delete', recipe)" class="action-btn delete-btn" title="刪除">
        <i class="fas fa-trash"></i>
        Delete
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  recipe: {
    id: number;
    library_id?: number;
    library_name?: string;
    name: string;
    description?: string;
    status: 'active' | 'inactive';
    allow_parallel_autoflows: boolean;
    autoflows_count?: number;
    recipe_steps_count?: number;
    created_time: string;
    updated_time: string;
  }
}>();

const emit = defineEmits<{
  view: [recipe: any];
  edit: [recipe: any];
  delete: [recipe: any];
}>();

const statusClass = computed(() => ({
  'status-active': props.recipe.status === 'active',
  'status-inactive': props.recipe.status === 'inactive'
}));

const truncatedDescription = computed(() => {
  if (!props.recipe.description) return '';
  return props.recipe.description.length > 100 
    ? props.recipe.description.substring(0, 100) + '...'
    : props.recipe.description;
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};
</script>

<style scoped>
.recipe-card {
  @apply bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-all duration-300 relative overflow-hidden;
  @apply hover:border-blue-300 hover:transform hover:scale-105;
}

.card-header {
  @apply flex justify-between items-center p-4 border-b border-gray-100;
}

.recipe-icon {
  @apply w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600;
}

.status-badge {
  @apply px-2 py-1 rounded-full text-xs font-semibold;
}

.status-active {
  @apply bg-green-100 text-green-800;
}

.status-inactive {
  @apply bg-gray-100 text-gray-600;
}

.card-body {
  @apply p-4;
}

.recipe-title {
  @apply text-lg font-semibold text-gray-800 mb-2 truncate;
}

.recipe-description {
  @apply text-sm text-gray-600 mb-4 leading-relaxed;
  min-height: 2.5rem;
}

.recipe-info {
  @apply space-y-2;
}

.info-item {
  @apply flex items-center gap-2;
}

.info-text {
  @apply text-sm text-gray-700;
}

.card-actions {
  @apply flex justify-center gap-2 p-4 border-t border-gray-100 bg-gray-50;
}

.action-btn {
  @apply flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors duration-200;
}

.view-btn {
  @apply bg-blue-100 text-blue-700 hover:bg-blue-200;
}

.edit-btn {
  @apply bg-yellow-100 text-yellow-700 hover:bg-yellow-200;
}

.delete-btn {
  @apply bg-red-100 text-red-700 hover:bg-red-200;
}


/* Enhanced hover effects */
.recipe-card:hover .recipe-icon {
  @apply transform scale-110 bg-blue-200;
}

.recipe-card:hover .recipe-title {
  @apply text-blue-600;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .recipe-card {
    @apply hover:transform-none hover:scale-100;
  }
  
  .action-btn {
    @apply px-2 py-1 text-xs;
  }
  
}

/* Animation for card entrance */
.recipe-card {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>