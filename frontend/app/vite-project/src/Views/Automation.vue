<template>
  <div class="flex min-h-screen" v-if="isAuthenticated">
    <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />
    
    <main class="flex-1 flex flex-col">
      <div class="automation-container">
        <!-- 頁面標題 -->
        <div class="page-header">
          <h1 class="text-2xl font-bold text-gray-800">自動化流程設計</h1>
          <p class="text-gray-600">設計和管理 Recipe、Autoflow 和 Processing Steps</p>
        </div>

    <!-- 工具欄 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <button @click="showRecipeModal = true" class="btn btn-primary">
          <i class="fas fa-plus"></i> 新增 Recipe
        </button>
        <button @click="showAutoflowModal = true" class="btn btn-secondary">
          <i class="fas fa-plus"></i> 新增 Autoflow
        </button>
        <button @click="showProcessingStepModal = true" class="btn btn-success">
          <i class="fas fa-plus"></i> 新增 Processing Step
        </button>
      </div>
      <div class="toolbar-right">
        <select @change="loadSelectedRecipeFlow" v-model="selectedRecipeId" class="form-select">
          <option value="">選擇 Recipe 載入流程圖</option>
          <option v-for="recipe in recipes" :key="recipe.id" :value="recipe.id">
            {{ recipe.name }}
          </option>
        </select>
        <button @click="saveFlow" class="btn btn-info">
          <i class="fas fa-save"></i> 保存流程
        </button>
        <button @click="clearFlow" class="btn btn-danger">
          <i class="fas fa-trash"></i> 清空畫布
        </button>
      </div>
    </div>

    <!-- 主要內容區域 -->
    <div class="main-content">
      <!-- 畫布容器 - 包含樹狀結構和 Drawflow -->
      <div class="canvas-container">
        <!-- 樹狀結構展示區域 -->
        <div class="tree-display-area">
          <div class="tree-header">
            <h3 class="tree-title">結構樹</h3>
            <div class="tree-controls">
              <button @click="expandAll" class="btn-expand">
                <i class="fas fa-expand-alt"></i> 展開全部
              </button>
              <button @click="collapseAll" class="btn-collapse">
                <i class="fas fa-compress-alt"></i> 收起全部
              </button>
            </div>
          </div>
          
          <!-- 畫布上的樹狀結構 -->
          <div class="canvas-tree-container">
            <div class="canvas-tree-list">
              <!-- Recipe 層級 -->
              <div v-for="recipe in recipes" :key="recipe.id" class="canvas-tree-item recipe-level">
                <div class="canvas-tree-node" @click="toggleRecipe(recipe)">
                  <div class="canvas-tree-line-container">
                    <div class="canvas-tree-expand-icon">
                      <i :class="recipe.expanded ? 'fas fa-minus-square' : 'fas fa-plus-square'"></i>
                    </div>
                    <div class="canvas-tree-content">
                      <div 
                        class="canvas-component-item recipe-item"
                        draggable="true"
                        @dragstart="onDragStart($event, 'recipe', recipe)"
                      >
                        <div class="canvas-item-header">
                          <span class="canvas-item-name">
                            <i class="fas fa-book"></i> {{ recipe.name }}
                          </span>
                          <div class="canvas-item-actions">
                            <button @click.stop="loadRecipeFlow(recipe)" class="canvas-btn-flow" title="載入流程圖">
                              <i class="fas fa-project-diagram"></i>
                            </button>
                            <button @click.stop="editRecipe(recipe)" class="canvas-btn-edit" title="編輯">
                              <i class="fas fa-edit"></i>
                            </button>
                          </div>
                        </div>
                        <div class="canvas-item-description">{{ recipe.description }}</div>
                        <div class="canvas-item-meta">
                          <span class="canvas-badge">{{ recipe.autoflows_count }} autoflows</span>
                          <span class="canvas-badge">{{ recipe.recipe_steps_count }} steps</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Autoflow 層級 -->
                <div v-if="recipe.expanded" class="canvas-tree-children">
                  <div 
                    v-for="(autoflow, autoflowIndex) in recipe.autoflows || []" 
                    :key="autoflow.id" 
                    class="canvas-tree-item autoflow-level"
                  >
                    <div class="canvas-tree-node" @click="toggleAutoflow(autoflow)">
                      <div class="canvas-tree-line-container">
                        <div class="canvas-tree-connector">
                          <div class="canvas-vertical-line" v-if="autoflowIndex < (recipe.autoflows?.length || 0) - 1"></div>
                          <div class="canvas-horizontal-line"></div>
                        </div>
                        <div class="canvas-tree-expand-icon">
                          <i :class="autoflow.expanded ? 'fas fa-minus-square' : 'fas fa-plus-square'"></i>
                        </div>
                        <div class="canvas-tree-content">
                          <div 
                            class="canvas-component-item autoflow-item"
                            draggable="true"
                            @dragstart="onDragStart($event, 'autoflow', autoflow)"
                          >
                            <div class="canvas-item-header">
                              <span class="canvas-item-name">
                                <i class="fas fa-project-diagram"></i> {{ autoflow.name }}
                              </span>
                              <div class="canvas-item-actions">
                                <button @click.stop="editAutoflow(autoflow)" class="canvas-btn-edit" title="編輯">
                                  <i class="fas fa-edit"></i>
                                </button>
                              </div>
                            </div>
                            <div class="canvas-item-description">{{ autoflow.description }}</div>
                            <div class="canvas-item-meta">
                              <span class="canvas-badge">{{ autoflow.processing_steps_count }} steps</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Processing Steps 層級 -->
                    <div v-if="autoflow.expanded" class="canvas-tree-children">
                      <div 
                        v-for="(step, stepIndex) in autoflow.processing_steps || []" 
                        :key="step.id" 
                        class="canvas-tree-item step-level"
                      >
                        <div class="canvas-tree-node">
                          <div class="canvas-tree-line-container">
                            <div class="canvas-tree-connector">
                              <div class="canvas-vertical-line" v-if="stepIndex < (autoflow.processing_steps?.length || 0) - 1"></div>
                              <div class="canvas-horizontal-line"></div>
                            </div>
                            <div class="canvas-tree-leaf-icon">
                              <i class="fas fa-circle"></i>
                            </div>
                            <div class="canvas-tree-content">
                              <div 
                                class="canvas-component-item step-item"
                                draggable="true"
                                @dragstart="onDragStart($event, 'step', step)"
                              >
                                <div class="canvas-item-header">
                                  <span class="canvas-item-name">
                                    <i class="fas fa-cogs"></i> {{ step.name }}
                                  </span>
                                  <button @click.stop="editProcessingStep(step)" class="canvas-btn-edit">
                                    <i class="fas fa-edit"></i>
                                  </button>
                                </div>
                                <div class="canvas-item-description">{{ step.description }}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Drawflow 畫布 -->
        <div class="drawflow-area">
          <div id="drawflow" class="drawflow-canvas" @drop="onDrop" @dragover="onDragOver"></div>
        </div>
      </div>
    </div>

    <!-- Recipe 新增/編輯模態框 -->
    <div v-if="showRecipeModal" class="modal-overlay" @click="showRecipeModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingRecipe ? '編輯 Recipe' : '新增 Recipe' }}</h3>
          <button @click="showRecipeModal = false" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitRecipe">
            <div class="form-group">
              <label>名稱</label>
              <input v-model="recipeForm.name" type="text" class="form-control" required>
            </div>
            <div class="form-group">
              <label>描述</label>
              <textarea v-model="recipeForm.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group">
              <label>狀態</label>
              <select v-model="recipeForm.status" class="form-control">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" @click="showRecipeModal = false" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary">{{ editingRecipe ? '更新' : '創建' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Autoflow 新增/編輯模態框 -->
    <div v-if="showAutoflowModal" class="modal-overlay" @click="showAutoflowModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingAutoflow ? '編輯 Autoflow' : '新增 Autoflow' }}</h3>
          <button @click="showAutoflowModal = false" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitAutoflow">
            <div class="form-group">
              <label>關聯的 Recipe</label>
              <select v-model="autoflowForm.recipe_id" class="form-control">
                <option value="">選擇 Recipe</option>
                <option v-for="recipe in recipes" :key="recipe.id" :value="recipe.id">
                  {{ recipe.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>名稱</label>
              <input v-model="autoflowForm.name" type="text" class="form-control" required>
            </div>
            <div class="form-group">
              <label>描述</label>
              <textarea v-model="autoflowForm.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group">
              <label>狀態</label>
              <select v-model="autoflowForm.status" class="form-control">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" @click="showAutoflowModal = false" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary">{{ editingAutoflow ? '更新' : '創建' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Processing Step 新增/編輯模態框 -->
    <div v-if="showProcessingStepModal" class="modal-overlay" @click="showProcessingStepModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingProcessingStep ? '編輯 Processing Step' : '新增 Processing Step' }}</h3>
          <button @click="showProcessingStepModal = false" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitProcessingStep">
            <div class="form-group">
              <label>關聯的 Autoflow</label>
              <select v-model="processingStepForm.autoflow_id" class="form-control">
                <option value="">選擇 Autoflow</option>
                <option v-for="autoflow in autoflows" :key="autoflow.id" :value="autoflow.id">
                  {{ autoflow.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>名稱</label>
              <input v-model="processingStepForm.name" type="text" class="form-control" required>
            </div>
            <div class="form-group">
              <label>描述</label>
              <textarea v-model="processingStepForm.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" @click="showProcessingStepModal = false" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary">{{ editingProcessingStep ? '更新' : '創建' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
      </div>
    </main>
  </div>
  <div v-else class="flex h-screen justify-center items-center">
    <p>正在驗證身份或跳轉至登錄頁面...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import Drawflow from 'drawflow';
import axios from 'axios';
import LeftMenu from '@/components/LeftMenu.vue';

// 路由和認證
const router = useRouter();
const authToken = ref(localStorage.getItem('token') || '');
const isAuthenticated = ref(false);

// 用戶資料
const userInfo = ref<{
  id: number;
  account: string;
  email: string;
  real_name?: string;
  avatar?: string;
} | null>(null);

// 菜單項
const menuItems = ref([
  { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: false },
  { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: true },
  { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
  { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
  { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
]);

// 響應式數據
const recipes = ref<any[]>([]);
const autoflows = ref<any[]>([]);
const processingSteps = ref<any[]>([]);
const selectedRecipeId = ref('');

// 組件庫狀態管理
const selectedRecipe = ref<any>(null);
const selectedAutoflow = ref<any>(null);
const currentAutoflows = ref<any[]>([]);
const currentProcessingSteps = ref<any[]>([]);

// 模態框狀態
const showRecipeModal = ref(false);
const showAutoflowModal = ref(false);
const showProcessingStepModal = ref(false);

// 編輯狀態
const editingRecipe = ref<any>(null);
const editingAutoflow = ref<any>(null);
const editingProcessingStep = ref<any>(null);

// 表單數據
const recipeForm = ref({
  name: '',
  description: '',
  status: 'active',
  recipe_steps: []
});

const autoflowForm = ref({
  recipe_id: '',
  name: '',
  description: '',
  status: 'active',
  processing_steps: []
});

const processingStepForm = ref({
  autoflow_id: '',
  name: '',
  description: ''
});

// Drawflow 實例
let editor: any = null;

// 認證檢查
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
      
      // 更新用戶資料給 LeftMenu 使用
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

// 載入資料
const loadData = async () => {
  try {
    const [recipesRes, autoflowsRes, stepsRes] = await Promise.all([
      axios.get('http://172.31.176.1:8000/api/recipes', {
        headers: { Authorization: `Bearer ${authToken.value}` }
      }),
      axios.get('http://172.31.176.1:8000/api/autoflows', {
        headers: { Authorization: `Bearer ${authToken.value}` }
      }),
      axios.get('http://172.31.176.1:8000/api/processing-steps', {
        headers: { Authorization: `Bearer ${authToken.value}` }
      })
    ]);
    
    recipes.value = recipesRes.data;
    autoflows.value = autoflowsRes.data;
    processingSteps.value = stepsRes.data;
  } catch (error) {
    console.error('載入資料失敗:', error);
  }
};

// 初始化 Drawflow
const initDrawflow = () => {
  const container = document.getElementById('drawflow');
  if (container) {
    editor = new Drawflow(container);
    editor.reroute = true;
    editor.reroute_fix_curvature = true;
    editor.force_first_input = false;
    editor.start();
  }
};

// 拖拽相關
const onDragStart = (event: DragEvent, type: string, item: any) => {
  event.dataTransfer?.setData('text/plain', JSON.stringify({ type, item }));
};

const onDragOver = (event: DragEvent) => {
  event.preventDefault();
};

const onDrop = (event: DragEvent) => {
  event.preventDefault();
  const data = JSON.parse(event.dataTransfer?.getData('text/plain') || '{}');
  
  if (data.type && data.item) {
    // 檢查拖拽限制
    if (data.type === 'autoflow' && selectedRecipe.value && data.item.recipe_id !== selectedRecipe.value.id) {
      alert('只能添加屬於當前選擇的 Recipe 的 Autoflows');
      return;
    }
    
    if (data.type === 'step' && selectedAutoflow.value && data.item.autoflow_id !== selectedAutoflow.value.id) {
      alert('只能添加屬於當前選擇的 Autoflow 的 Processing Steps');
      return;
    }
    
    addNodeToCanvas(data.type, data.item, event.offsetX, event.offsetY);
  }
};

const addNodeToCanvas = (type: string, item: any, x: number, y: number) => {
  let nodeContent = '';
  let nodeClass = '';
  
  switch (type) {
    case 'recipe':
      nodeContent = `
        <div class="node-header recipe-node">
          <i class="fas fa-book"></i>
          <span class="node-title">${item.name}</span>
        </div>
        <div class="node-content">
          <p>${item.description || ''}</p>
          <div class="node-meta">
            <span class="badge">${item.autoflows_count} autoflows</span>
            <span class="badge">${item.recipe_steps_count} steps</span>
          </div>
        </div>
      `;
      nodeClass = 'recipe-node';
      break;
    case 'autoflow':
      nodeContent = `
        <div class="node-header autoflow-node">
          <i class="fas fa-project-diagram"></i>
          <span class="node-title">${item.name}</span>
        </div>
        <div class="node-content">
          <p>${item.description || ''}</p>
          <div class="node-meta">
            <span class="badge">${item.processing_steps_count} steps</span>
          </div>
        </div>
      `;
      nodeClass = 'autoflow-node';
      break;
    case 'step':
      nodeContent = `
        <div class="node-header step-node">
          <i class="fas fa-cogs"></i>
          <span class="node-title">${item.name}</span>
        </div>
        <div class="node-content">
          <p>${item.description || ''}</p>
        </div>
      `;
      nodeClass = 'step-node';
      break;
  }
  
  editor.addNode(type, 1, 1, x, y, nodeClass, { item_id: item.id }, nodeContent);
};

// Recipe 相關操作
const editRecipe = (recipe: any) => {
  editingRecipe.value = recipe;
  recipeForm.value = { ...recipe };
  showRecipeModal.value = true;
};

const submitRecipe = async () => {
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
    
    showRecipeModal.value = false;
    editingRecipe.value = null;
    recipeForm.value = { name: '', description: '', status: 'active', recipe_steps: [] };
    await loadData();
  } catch (error) {
    console.error('Recipe 操作失敗:', error);
  }
};

// Autoflow 相關操作
const editAutoflow = (autoflow: any) => {
  editingAutoflow.value = autoflow;
  autoflowForm.value = { ...autoflow };
  showAutoflowModal.value = true;
};

const submitAutoflow = async () => {
  try {
    if (editingAutoflow.value) {
      await axios.put(`http://172.31.176.1:8000/api/autoflows/${editingAutoflow.value.id}`, autoflowForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    } else {
      await axios.post('http://172.31.176.1:8000/api/autoflows', autoflowForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    }
    
    showAutoflowModal.value = false;
    editingAutoflow.value = null;
    autoflowForm.value = { recipe_id: '', name: '', description: '', status: 'active', processing_steps: [] };
    await loadData();
  } catch (error) {
    console.error('Autoflow 操作失敗:', error);
  }
};

// Processing Step 相關操作
const editProcessingStep = (step: any) => {
  editingProcessingStep.value = step;
  processingStepForm.value = { ...step };
  showProcessingStepModal.value = true;
};

const submitProcessingStep = async () => {
  try {
    if (editingProcessingStep.value) {
      await axios.put(`http://172.31.176.1:8000/api/processing-steps/${editingProcessingStep.value.id}`, processingStepForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    } else {
      await axios.post('http://172.31.176.1:8000/api/processing-steps', processingStepForm.value, {
        headers: { Authorization: `Bearer ${authToken.value}` }
      });
    }
    
    showProcessingStepModal.value = false;
    editingProcessingStep.value = null;
    processingStepForm.value = { autoflow_id: '', name: '', description: '' };
    await loadData();
  } catch (error) {
    console.error('Processing Step 操作失敗:', error);
  }
};

// 畫布操作
const saveFlow = () => {
  const flowData = editor.export();
  console.log('Flow data:', flowData);
  // 這裡可以實現保存到後端的邏輯
};

const clearFlow = () => {
  editor.clear();
};

// 載入 Recipe 流程圖
const loadRecipeFlow = (recipe: any) => {
  // 清空畫布
  editor.clear();
  
  if (!recipe.autoflows || recipe.autoflows.length === 0) {
    console.log('此 Recipe 沒有 Autoflows');
    return;
  }
  
  // 更新組件庫狀態
  selectRecipe(recipe);
  
  // 計算布局參數
  const recipeX = 50;
  const recipeY = 50;
  const autoflowStartY = 250;
  const autoflowSpacing = 400;
  const stepStartY = 450;
  const stepSpacing = 200;
  
  // 創建 Recipe 節點
  const recipeNodeId = addRecipeNode(recipe, recipeX, recipeY);
  
  // 為每個 Autoflow 創建節點並連接
  recipe.autoflows.forEach((autoflow: any, autoflowIndex: number) => {
    const autoflowX = recipeX + (autoflowIndex * autoflowSpacing);
    const autoflowNodeId = addAutoflowNode(autoflow, autoflowX, autoflowStartY);
    
    // 連接 Recipe 到 Autoflow
    editor.addConnection(recipeNodeId, autoflowNodeId, 'output_1', 'input_1');
    
    // 為每個 Processing Step 創建節點並連接
    if (autoflow.processing_steps && autoflow.processing_steps.length > 0) {
      let previousStepNodeId = autoflowNodeId;
      
      autoflow.processing_steps.forEach((step: any, stepIndex: number) => {
        const stepX = autoflowX + (stepIndex * stepSpacing) - ((autoflow.processing_steps.length - 1) * stepSpacing / 2);
        const stepY = stepStartY + (stepIndex * 150);
        const stepNodeId = addProcessingStepNode(step, stepX, stepY);
        
        // 連接到上一個節點（可能是 autoflow 或前一個 step）
        if (stepIndex === 0) {
          // 第一個 step 連接到 autoflow
          editor.addConnection(autoflowNodeId, stepNodeId, 'output_1', 'input_1');
        } else {
          // 其他 steps 連接到前一個 step
          const prevStepNodeId = `step_${autoflow.processing_steps[stepIndex - 1].id}`;
          editor.addConnection(prevStepNodeId, stepNodeId, 'output_1', 'input_1');
        }
      });
    }
  });
  
  // 重置下拉選單
  selectedRecipeId.value = '';
};

// 添加 Recipe 節點到畫布
const addRecipeNode = (recipe: any, x: number, y: number) => {
  const nodeId = `recipe_${recipe.id}`;
  const nodeContent = `
    <div class="node-header recipe-node">
      <i class="fas fa-book"></i>
      <span class="node-title">${recipe.name}</span>
    </div>
    <div class="node-content">
      <p class="node-description">${recipe.description || ''}</p>
      <div class="node-meta">
        <span class="badge">${recipe.autoflows_count || recipe.autoflows?.length || 0} autoflows</span>
        <span class="badge">${recipe.recipe_steps_count || recipe.recipe_steps?.length || 0} steps</span>
      </div>
    </div>
  `;
  
  editor.addNode(nodeId, 0, 1, x, y, 'recipe-node', { item_id: recipe.id, type: 'recipe' }, nodeContent);
  return nodeId;
};

// 添加 Autoflow 節點到畫布
const addAutoflowNode = (autoflow: any, x: number, y: number) => {
  const nodeId = `autoflow_${autoflow.id}`;
  const nodeContent = `
    <div class="node-header autoflow-node">
      <i class="fas fa-project-diagram"></i>
      <span class="node-title">${autoflow.name}</span>
    </div>
    <div class="node-content">
      <p class="node-description">${autoflow.description || ''}</p>
      <div class="node-meta">
        <span class="badge">${autoflow.processing_steps_count || autoflow.processing_steps?.length || 0} steps</span>
      </div>
    </div>
  `;
  
  editor.addNode(nodeId, 1, 1, x, y, 'autoflow-node', { item_id: autoflow.id, type: 'autoflow' }, nodeContent);
  return nodeId;
};

// 添加 Processing Step 節點到畫布
const addProcessingStepNode = (step: any, x: number, y: number) => {
  const nodeId = `step_${step.id}`;
  const nodeContent = `
    <div class="node-header step-node">
      <i class="fas fa-cogs"></i>
      <span class="node-title">${step.name}</span>
    </div>
    <div class="node-content">
      <p class="node-description">${step.description || ''}</p>
    </div>
  `;
  
  editor.addNode(nodeId, 1, 1, x, y, 'step-node', { item_id: step.id, type: 'step' }, nodeContent);
  return nodeId;
};

// 從下拉選單載入 Recipe 流程圖
const loadSelectedRecipeFlow = () => {
  if (!selectedRecipeId.value) return;
  
  const recipe = recipes.value.find((r: { id: number; }) => r.id === parseInt(selectedRecipeId.value));
  if (recipe) {
    loadRecipeFlow(recipe);
  }
};

// 組件庫導航函數
const selectRecipe = (recipe: any) => {
  selectedRecipe.value = recipe;
  selectedAutoflow.value = null;
  currentAutoflows.value = recipe.autoflows || [];
  currentProcessingSteps.value = [];
};

const selectAutoflow = (autoflow: any) => {
  selectedAutoflow.value = autoflow;
  currentProcessingSteps.value = autoflow.processing_steps || [];
};

const resetToRecipes = () => {
  selectedRecipe.value = null;
  selectedAutoflow.value = null;
  currentAutoflows.value = [];
  currentProcessingSteps.value = [];
};

const resetToAutoflows = () => {
  selectedAutoflow.value = null;
  currentProcessingSteps.value = [];
};

// 樹狀結構展開/收起功能
const toggleRecipe = (recipe: any) => {
  recipe.expanded = !recipe.expanded;
};

const toggleAutoflow = (autoflow: any) => {
  autoflow.expanded = !autoflow.expanded;
};

const expandAll = () => {
  recipes.value.forEach((recipe: { expanded: boolean; autoflows: any[]; }) => {
    recipe.expanded = true;
    if (recipe.autoflows) {
      recipe.autoflows.forEach((autoflow: any) => {
        autoflow.expanded = true;
      });
    }
  });
};

const collapseAll = () => {
  recipes.value.forEach((recipe: { expanded: boolean; autoflows: any[]; }) => {
    recipe.expanded = false;
    if (recipe.autoflows) {
      recipe.autoflows.forEach((autoflow: any) => {
        autoflow.expanded = false;
      });
    }
  });
};

// 生命週期
onMounted(async () => {
  await checkAuth();
  if (isAuthenticated.value) {
    await loadData();
    await nextTick();
    initDrawflow();
  }
});
</script>

<style scoped>
.automation-container {
  @apply flex flex-col bg-gray-50 h-full;
}

.page-header {
  @apply p-6 bg-white shadow-sm border-b;
}

.toolbar {
  @apply flex justify-between items-center p-4 bg-white shadow-sm border-b;
}

.toolbar-left, .toolbar-right {
  @apply flex space-x-2;
}

.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.btn-secondary {
  @apply bg-gray-500 text-white hover:bg-gray-600;
}

.btn-success {
  @apply bg-green-500 text-white hover:bg-green-600;
}

.btn-info {
  @apply bg-cyan-500 text-white hover:bg-cyan-600;
}

.btn-danger {
  @apply bg-red-500 text-white hover:bg-red-600;
}

.main-content {
  @apply flex-1 flex;
}

.canvas-container {
  @apply flex-1 relative flex;
}

.tree-display-area {
  @apply w-80 bg-white shadow-lg border-r overflow-y-auto flex-shrink-0;
}

.tree-header {
  @apply border-b bg-gray-50 p-4 flex justify-between items-center;
}

.tree-title {
  @apply text-lg font-semibold;
}

.tree-controls {
  @apply flex space-x-2;
}

.btn-expand, .btn-collapse {
  @apply text-xs px-2 py-1 rounded bg-blue-500 text-white hover:bg-blue-600;
}

.canvas-tree-container {
  @apply p-4 overflow-y-auto;
}

.canvas-tree-list {
  @apply space-y-2;
}

.canvas-tree-item {
  @apply relative;
}

.canvas-tree-node {
  @apply cursor-pointer;
}

.canvas-tree-line-container {
  @apply flex items-start;
}

.canvas-tree-connector {
  @apply relative flex-shrink-0 w-6 h-6 flex items-center justify-center;
}

.canvas-tree-connector .canvas-vertical-line {
  @apply absolute left-3 top-6 w-px h-full bg-gray-300;
}

.canvas-tree-connector .canvas-horizontal-line {
  @apply absolute left-3 top-3 w-3 h-px bg-gray-300;
}

.canvas-tree-expand-icon {
  @apply flex-shrink-0 w-6 h-6 flex items-center justify-center text-gray-500 hover:text-gray-700;
}

.canvas-tree-leaf-icon {
  @apply flex-shrink-0 w-6 h-6 flex items-center justify-center text-gray-400;
}

.canvas-tree-leaf-icon i {
  @apply text-xs;
}

.canvas-tree-content {
  @apply flex-1 ml-2;
}

.canvas-tree-children {
  @apply ml-6 border-l border-gray-200;
}

.canvas-component-item {
  @apply p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-white hover:shadow-md cursor-move transition-all duration-200;
}

.canvas-component-item:hover {
  @apply transform scale-105;
}

.canvas-component-item.dragging {
  @apply opacity-50;
}

.recipe-item {
  @apply border-blue-200 hover:border-blue-300;
}

.autoflow-item {
  @apply border-green-200 hover:border-green-300;
}

.step-item {
  @apply border-purple-200 hover:border-purple-300;
}

.canvas-item-header {
  @apply flex justify-between items-center mb-2;
}

.canvas-item-name {
  @apply font-medium text-gray-800;
}

.canvas-item-actions {
  @apply flex space-x-1;
}

.canvas-btn-edit {
  @apply p-1 text-gray-500 hover:text-gray-700;
}

.canvas-btn-flow {
  @apply p-1 text-blue-500 hover:text-blue-700;
}

.canvas-item-description {
  @apply text-sm text-gray-600 mb-2;
}

.canvas-item-meta {
  @apply flex space-x-2;
}

.canvas-badge {
  @apply px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700;
}

.recipe-level {
  @apply mb-4;
}

.autoflow-level {
  @apply mb-2;
}

.step-level {
  @apply mb-1;
}

.drawflow-area {
  @apply flex-1 relative;
}

.drawflow-canvas {
  @apply w-full h-full;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg shadow-xl max-w-md w-full mx-4;
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

.form-select {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white;
}

.form-actions {
  @apply flex justify-end space-x-2 mt-6;
}

/* Drawflow 節點樣式 */
:deep(.recipe-node) {
  @apply bg-blue-50 border-blue-300;
}

:deep(.autoflow-node) {
  @apply bg-green-50 border-green-300;
}

:deep(.step-node) {
  @apply bg-purple-50 border-purple-300;
}

:deep(.node-header) {
  @apply flex items-center space-x-2 p-2 border-b;
}

:deep(.node-title) {
  @apply font-medium text-gray-800;
}

:deep(.node-content) {
  @apply p-3;
}

:deep(.node-description) {
  @apply text-sm text-gray-600 mb-2;
}

:deep(.node-meta) {
  @apply flex space-x-2 mt-2;
}

:deep(.node-meta .badge) {
  @apply px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700;
}

/* Drawflow 基本樣式 */
:deep(.drawflow) {
  @apply bg-gray-100;
}

:deep(.drawflow .drawflow-node) {
  @apply bg-white rounded-lg shadow-md border-2 min-w-48;
}

:deep(.drawflow .drawflow-node.selected) {
  @apply border-blue-500;
}

:deep(.drawflow .connection) {
  @apply stroke-2;
}

:deep(.drawflow .connection .main-path) {
  @apply stroke-blue-500;
}

:deep(.drawflow .connection .point) {
  @apply fill-blue-500;
}

:deep(.drawflow .connection .point.selected) {
  @apply fill-red-500;
}
</style>