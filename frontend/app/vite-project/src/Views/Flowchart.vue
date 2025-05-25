<template>
    <div class="flex h-screen">
        <LeftMenu :menuItems="menuItems" />

        <div class="function-panel w-48 bg-gray-100 p-4 border-r border-gray-200">
            <h3 class="text-lg font-semibold mb-4">動作</h3>
            <div
                v-for="action in actions"
                :key="action.id"
                class="action-item mb-2 p-2 bg-white border border-gray-300 rounded cursor-move"
                draggable="true"
                @dragstart="onDragStart($event, action)"
            >
                <div class="drawflow-node-preview p-2 text-center" :style="{ backgroundColor: '#e0f7fa', border: '2px solid #0288d1', borderRadius: '5px'}">
                    {{ action.label }}
                </div>
            </div>
        </div>

        <main class="flex-1 flex p-6">
            <div id="drawflow" class="dashboard-container flex-1 p-10px border border-gray-300" @drop="onDrop($event)" @dragover.prevent>
                </div>
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick } from "vue";
import LeftMenu from '@/components/LeftMenu.vue'; // 假設路徑正確
import Drawflow from 'drawflow';
import 'drawflow/dist/drawflow.min.css'; // 引入 Drawflow 樣式
// 如果您想自定義 Drawflow 節點樣式，可以在這裡或全局 CSS 中添加

// 注意：您原有的 actions 中 id:3 有重複，我將其修改為 3 和 4
interface Action {
    id: number;
    label: string;
    nodeName?: string; // 用於 Drawflow 節點類型
    inputs?: number;
    outputs?: number;
}

export default defineComponent({
    name: "FlowchartPageWithDrawflow",
    components: {
        LeftMenu,
    },
    setup() {
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
            { label: 'Automation Control', link: '/flowchart', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const editor = ref<Drawflow | null>(null);

        // 功能區的動作
        const actions = ref<Action[]>([
            { id: 1, label: '開啟檔案', nodeName: 'openFile', inputs: 0, outputs: 1 },
            { id: 2, label: '關閉檔案', nodeName: 'closeFile', inputs: 1, outputs: 0 },
            { id: 3, label: '掃描檔案', nodeName: 'scanFile', inputs: 1, outputs: 1 },
            { id: 4, label: 'Sandbox分析', nodeName: 'sandboxAnalysis', inputs: 1, outputs: 1 }, // 修正了重複的 ID
        ]);

        const onDragStart = (event: DragEvent, action: Action) => {
            if (event.dataTransfer) {
                // 傳遞 action 的相關資訊，特別是 nodeName，以便在 onDrop 中使用
                event.dataTransfer.setData('application/drawflow', JSON.stringify(action));
            }
        };

        const onDrop = (event: DragEvent) => {
            event.preventDefault();
            if (editor.value && event.dataTransfer) {
                const actionString = event.dataTransfer.getData('application/drawflow');
                if (!actionString) return;

                const action: Action = JSON.parse(actionString);

                // 計算放置位置
                // Drawflow addNode 的 x, y 是相對於 Drawflow 容器的
                const container = (event.target as HTMLElement).closest('#drawflow');
                if (!container) return;

                const rect = container.getBoundingClientRect();
                const x = event.clientX - rect.left - (event.offsetX || 0); //offsetX可能不准, drawflow內部會再處理
                const y = event.clientY - rect.top - (event.offsetY || 0);  //offsetY可能不准

                // 定義節點的 HTML 內容
                // 您可以創建更複雜的 HTML 結構，甚至使用 Vue 組件來渲染節點內容
                const nodeHtml = `
                    <div style="padding: 10px; background-color: #e0f7fa; border: 2px solid #0288d1; border-radius: 5px; text-align: center;">
                        ${action.label}
                    </div>
                `;

                editor.value.addNode(
                    action.nodeName || action.label.toLowerCase().replace(/\s/g, ''), // 節點名稱/類型
                    action.inputs !== undefined ? action.inputs : 1,         // 輸入點數量
                    action.outputs !== undefined ? action.outputs : 1,       // 輸出點數量
                    x,                                            // X 座標
                    y,                                            // Y 座標
                    action.nodeName || action.label.replace(/\s/g, ''), // class name for the node
                    { label: action.label, id: action.id },      // 節點的內部數據
                    nodeHtml,                                     // 節點的 HTML 內容
                    false                                         // 'vue' 模式 (如果使用 Vue 渲染節點則為 true)
                );
            }
        };

        onMounted(() => {
            const container = document.getElementById('drawflow');
            if (container) {
                editor.value = new Drawflow(container, { registerNode: undefined }, {
                    // Drawflow options (if any)
                    // 例如: reroute: true, reroute_fix_curvature: true
                });
                editor.value.start();

                // (可選) 註冊自定義節點類型，如果需要更複雜的節點渲染或行為
                // actions.value.forEach(action => {
                //     if (action.nodeName && editor.value) {
                //         // 這裡的 HTML 也可以是一個 Vue 組件的實例
                //         const nodeHtmlTemplate = `
                //             <div class="custom-node" style="background-color: #e0f7fa; border: 1px solid #0288d1; padding: 15px; border-radius: 5px;">
                //                 <div><strong>${action.label}</strong></div>
                //             </div>
                //         `;
                //         editor.value.registerNode(action.nodeName, nodeHtmlTemplate, {}, {}); // 後兩個參數是 props 和 options
                //     }
                // });

                // (可選) 監聽 Drawflow 事件
                editor.value.on('nodeCreated', (id: number) => {
                    console.log("Node Created: " + id);
                    // 您可以在此處獲取 editor.value.getNodeFromId(id) 來訪問節點數據
                });

                editor.value.on('connectionCreated', (connection: any) => {
                    console.log("Connection Created", connection);
                });

                editor.value.on('nodeRemoved', (id: number) => {
                    console.log("Node Removed: " + id);
                });

                // 可以使用 editor.value.import(data) 來載入現有流程圖
                // editor.value.import({ "drawflow": { "Home": { "data": { /* ... some data ... */ } } } });
            }
        });

        // 如果需要導出數據
        // const exportData = () => {
        //     if (editor.value) {
        //         const data = editor.value.export();
        //         console.log(JSON.stringify(data));
        //         // 在此處處理導出的數據，例如保存到後端
        //     }
        // };

        return {
            menuItems,
            actions,
            onDragStart,
            onDrop, // onDrop 現在是 Drawflow 容器的事件
            // exportData, // 如果需要導出功能，可以解除註釋
        };
    },
});
</script>

<style scoped>
/* 確保 Drawflow 容器有明確的尺寸 */
#drawflow {
    width: 100%;
    height: calc(100vh - 100px); /* 根據您的佈局調整 */
    background: #f7f7f7; /* 給一個背景色，方便看清邊界 */
    border: 1px solid #ccc;
}

.function-panel {
    width: 200px; /* 與模板中一致 */
}

.action-item {
    user-select: none; /* 防止拖曳時選中文本 */
}

.drawflow-node-preview { /* 預覽項目的樣式，可以自定義 */
    font-size: 14px;
}

/* 您可以添加更多自定義樣式來美化 Drawflow 節點和連接線 */
/* 例如： */
/* ::v-deep .drawflow-node { ... } */
/* ::v-deep .drawflow-connection .main-path { stroke: blue; stroke-width: 3; } */

</style>