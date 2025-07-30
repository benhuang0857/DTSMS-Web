<template>
  <div class="flex min-h-screen" v-if="isAuthenticated">
    <LeftMenu :menuItems="menuItems" :userInfo="userInfo" />
    
    <main class="flex-1 flex flex-col">
      <div class="automation-container">
        <!-- Page Header -->
        <div class="page-header">
          <h1 class="text-2xl font-bold text-gray-800">自動化流程設計</h1>
          <p class="text-gray-600">設計和管理 Recipe、Autoflow 和 Processing Steps</p>
        </div>

        <!-- Toolbar -->
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

        <!-- Main Content Area -->
        <div class="main-content">
          <div class="canvas-container">
            <!-- Tree Display Area -->
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
              
              <div class="canvas-tree-container">
                <div class="canvas-tree-list">
                  <!-- Recipe Level -->
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
                    
                    <!-- Autoflow Level -->
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
                        
                        <!-- Processing Steps Level -->
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
            
            <!-- Vue Flow Canvas -->
            <div class="vueflow-area">
              <VueFlow 
                v-model:nodes="nodes" 
                v-model:edges="edges"
                @dragover="onDragOver"
                @drop="onDrop"
                @connect="onConnect"
                @nodes-delete="onNodesDelete"
                @edges-delete="onEdgesDelete"
                :fit-view-on-init="true"
                :nodes-draggable="true"
                :nodes-connectable="true"
                :nodes-deletable="true"
                :edges-deletable="true"
                :edge-types="edgeTypes"
              >
                <template #node-recipe="recipeProps">
                  <RecipeNode v-bind="recipeProps" />
                </template>
                <template #node-autoflow="autoflowProps">
                  <AutoflowNode v-bind="autoflowProps" />
                </template>
                <template #node-step="stepProps">
                  <StepNode v-bind="stepProps" />
                </template>
              </VueFlow>
            </div>
          </div>
        </div>

        <!-- Recipe Modal -->
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

        <!-- Autoflow Modal -->
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

        <!-- Processing Step Modal -->
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { VueFlow, useVueFlow, type Node, type Edge, type Connection, BezierEdge } from '@vue-flow/core';
import axios from 'axios';
import LeftMenu from '@/components/LeftMenu.vue';
import RecipeNode from '@/components/RecipeNode.vue';
import AutoflowNode from '@/components/AutoflowNode.vue';
import StepNode from '@/components/StepNode.vue';

// Vue Flow setup
const { addNodes, addEdges, setNodes, setEdges, removeNodes, removeEdges, getSelectedNodes, getSelectedEdges } = useVueFlow();
const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);
const edgeTypes = { bezier: BezierEdge };

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
  { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: true },
  { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
  { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
  { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
]);

// Reactive data
const recipes = ref<any[]>([]);
const autoflows = ref<any[]>([]);
const processingSteps = ref<any[]>([]);
const selectedRecipeId = ref('');

// Component library state
const selectedRecipe = ref<any>(null);
const selectedAutoflow = ref<any>(null);
const currentAutoflows = ref<any[]>([]);
const currentProcessingSteps = ref<any[]>([]);

// Modal states
const showRecipeModal = ref(false);
const showAutoflowModal = ref(false);
const showProcessingStepModal = ref(false);

// Editing states
const editingRecipe = ref<any>(null);
const editingAutoflow = ref<any>(null);
const editingProcessingStep = ref<any>(null);

// Form data
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

// Drag and drop
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
    // Check drag restrictions
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

// Handle node connections
const onConnect = (connection: Connection) => {
  const newEdge: Edge = {
    id: `e-${connection.source}-${connection.target}`,
    source: connection.source!,
    target: connection.target!,
    type: 'bezier',
  };
  
  addEdges([newEdge]);
};

// Handle node deletion
const onNodesDelete = (deletedNodes: Node[]) => {
  console.log('Nodes deleted:', deletedNodes);
  // Optional: Add any cleanup logic here
};

// Handle edge deletion
const onEdgesDelete = (deletedEdges: Edge[]) => {
  console.log('Edges deleted:', deletedEdges);
  // Optional: Add any cleanup logic here
};

// Handle keyboard events for deletion
const onKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Delete' || event.key === 'Backspace') {
    event.preventDefault();
    
    const selectedNodes = getSelectedNodes.value;
    const selectedEdges = getSelectedEdges.value;
    
    if (selectedNodes.length > 0) {
      removeNodes(selectedNodes.map((node: { id: any; }) => node.id));
    }
    
    if (selectedEdges.length > 0) {
      removeEdges(selectedEdges.map((edge: { id: any; }) => edge.id));
    }
  }
};

const addNodeToCanvas = (type: string, item: any, x: number, y: number) => {
  const node: Node = {
    id: `${type}_${item.id}`,
    type,
    position: { x, y },
    data: { ...item },
    class: `${type}-node`,
  };
  
  addNodes([node]);
};

// Recipe operations
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

// Autoflow operations
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

// Processing Step operations
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

// Canvas operations
const saveFlow = () => {
  const flowData = { nodes: nodes.value, edges: edges.value };
  console.log('Flow data:', flowData);
  // Implement backend save logic here
};

const clearFlow = () => {
  setNodes([]);
  setEdges([]);
};

// Load Recipe flow
const loadRecipeFlow = (recipe: any) => {
  setNodes([]);
  setEdges([]);
  
  if (!recipe.autoflows || recipe.autoflows.length === 0) {
    console.log('此 Recipe 沒有 Autoflows');
    return;
  }
  
  selectRecipe(recipe);
  
  // Layout parameters
  const recipeX = 50;
  const recipeY = 50;
  const autoflowStartY = 250;
  const autoflowSpacing = 400;
  const stepStartY = 450;
  const stepSpacing = 200;
  
  // Create Recipe node
  const recipeNode: Node = {
    id: `recipe_${recipe.id}`,
    type: 'recipe',
    position: { x: recipeX, y: recipeY },
    data: { ...recipe },
    class: 'recipe-node',
  };
  
  const newNodes: Node[] = [recipeNode];
  const newEdges: Edge[] = [];
  
  // Create Autoflow nodes and edges
  recipe.autoflows.forEach((autoflow: any, autoflowIndex: number) => {
    const autoflowX = recipeX + (autoflowIndex * autoflowSpacing);
    const autoflowNode: Node = {
      id: `autoflow_${autoflow.id}`,
      type: 'autoflow',
      position: { x: autoflowX, y: autoflowStartY },
      data: { ...autoflow },
      class: 'autoflow-node',
    };
    
    newNodes.push(autoflowNode);
    newEdges.push({
      id: `e-recipe_${recipe.id}-autoflow_${autoflow.id}`,
      source: recipeNode.id,
      target: autoflowNode.id,
      type: 'bezier',
    });
    
    // Create Processing Step nodes and edges
    if (autoflow.processing_steps && autoflow.processing_steps.length > 0) {
      let previousNodeId = autoflowNode.id;
      
      autoflow.processing_steps.forEach((step: any, stepIndex: number) => {
        const stepX = autoflowX + (stepIndex * stepSpacing) - ((autoflow.processing_steps.length - 1) * stepSpacing / 2);
        const stepY = stepStartY + (stepIndex * 150);
        const stepNode: Node = {
          id: `step_${step.id}`,
          type: 'step',
          position: { x: stepX, y: stepY },
          data: { ...step },
          class: 'step-node',
        };
        
        newNodes.push(stepNode);
        
        newEdges.push({
          id: `e-${previousNodeId}-step_${step.id}`,
          source: previousNodeId,
          target: stepNode.id,
          type: 'bezier',
        });
        
        previousNodeId = stepNode.id;
      });
    }
  });
  
  addNodes(newNodes);
  addEdges(newEdges);
  selectedRecipeId.value = '';
};

// Load selected recipe flow from dropdown
const loadSelectedRecipeFlow = () => {
  if (!selectedRecipeId.value) return;
  
  const recipe = recipes.value.find((r: { id: number }) => r.id === parseInt(selectedRecipeId.value));
  if (recipe) {
    loadRecipeFlow(recipe);
  }
};

// Component library navigation
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

// Tree expand/collapse
const toggleRecipe = (recipe: any) => {
  recipe.expanded = !recipe.expanded;
};

const toggleAutoflow = (autoflow: any) => {
  autoflow.expanded = !autoflow.expanded;
};

const expandAll = () => {
  recipes.value.forEach((recipe: { expanded: boolean; autoflows: any[] }) => {
    recipe.expanded = true;
    if (recipe.autoflows) {
      recipe.autoflows.forEach((autoflow: any) => {
        autoflow.expanded = true;
      });
    }
  });
};

const collapseAll = () => {
  recipes.value.forEach((recipe: { expanded: boolean; autoflows: any[] }) => {
    recipe.expanded = false;
    if (recipe.autoflows) {
      recipe.autoflows.forEach((autoflow: any) => {
        autoflow.expanded = false;
      });
    }
  });
};

// Lifecycle
onMounted(async () => {
  await checkAuth();
  if (isAuthenticated.value) {
    await loadData();
    await nextTick();
  }
  
  // Add keyboard event listener
  document.addEventListener('keydown', onKeyDown);
});

onUnmounted(() => {
  // Remove keyboard event listener
  document.removeEventListener('keydown', onKeyDown);
});
</script>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
</style>

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

.vueflow-area {
  @apply flex-1 relative;
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

/* Vue Flow node styles */
:deep(.recipe-node) {
  @apply bg-blue-50 border-blue-300 rounded-lg shadow-md min-w-48 p-3;
}

:deep(.autoflow-node) {
  @apply bg-green-50 border-green-300 rounded-lg shadow-md min-w-48 p-3;
}

:deep(.step-node) {
  @apply bg-purple-50 border-purple-300 rounded-lg shadow-md min-w-48 p-3;
}

:deep(.vue-flow__node.selected) {
  @apply border-blue-500;
}

:deep(.vue-flow__edge) {
  @apply stroke-2;
}

:deep(.vue-flow__edge-path) {
  @apply stroke-blue-500;
}
</style>