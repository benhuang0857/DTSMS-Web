<template>
    <div class="flex h-screen">
        <!-- LeftMenu -->
        <LeftMenu :menuItems="menuItems" />

        <!-- 功能區 -->
        <div class="function-panel w-48 bg-gray-100 p-4 border-r border-gray-200">
            <h3 class="text-lg font-semibold mb-4">動作</h3>
            <div
                v-for="action in actions"
                :key="action.id"
                class="action-item mb-2 p-2 bg-white border border-gray-300 rounded cursor-move"
                draggable="true"
                @dragstart="onDragStart($event, action)"
            >
                <svg width="150" height="40">
                    <rect x="0" y="0" width="150" height="40" rx="5" fill="#e0f7fa" stroke="#0288d1" stroke-width="2" />
                    <text x="50" y="25" text-anchor="middle" fill="#000" font-size="14">{{ action.label }}</text>
                </svg>
            </div>
        </div>

        <!-- 流程圖區域 -->
        <main class="flex-1 flex p-6">
            <div class="dashboard-container flex-1 p-10px" @drop="onDrop($event)" @dragover.prevent>
                <div class="flowchart">
                    <svg ref="svg" :width="width" :height="height">
                        <!-- 連線 -->
                        <line
                            v-for="link in links"
                            :key="link.id"
                            :x1="nodes.find((n) => n.id === link.source)?.x || 0"
                            :y1="nodes.find((n) => n.id === link.source)?.y || 0"
                            :x2="nodes.find((n) => n.id === link.target)?.x || 0"
                            :y2="nodes.find((n) => n.id === link.target)?.y || 0"
                            stroke="#000"
                            stroke-width="2"
                        />
                        <!-- 節點（動作長方形） -->
                        <g v-for="node in nodes" :key="node.id" @click="onNodeClick(node)">
                            <rect
                                :x="node.x - 50"
                                :y="node.y - 20"
                                width="150"
                                height="40"
                                rx="5"
                                fill="#e0f7fa"
                                stroke="#0288d1"
                                stroke-width="2"
                                class="cursor-move"
                                @dragstart="onNodeDragStart($event, node)"
                                draggable="true"
                            />
                            <text
                                :x="node.x"
                                :y="node.y + 5"
                                text-anchor="middle"
                                fill="#000"
                                font-size="14"
                            >{{ node.label }}</text>
                        </g>
                    </svg>
                </div>
            </div>
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import LeftMenu from '@/components/LeftMenu.vue';
import * as d3 from "d3";

// 定義節點和連結的型別
interface Node {
    id: number;
    x: number;
    y: number;
    label: string;
}

interface Link {
    id: number;
    source: number;
    target: number;
}

export default defineComponent({
    name: "FlowchartPage",
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

        const svg = ref<SVGSVGElement | null>(null); // SVG 容器的引用
        const width = 800;
        const height = 600;

        // 功能區的動作
        const actions = ref([
            { id: 1, label: '開啟檔案' },
            { id: 2, label: '關閉檔案' },
            { id: 3, label: '掃描檔案' },
            { id: 3, label: 'Sandbox分析' },
        ]);

        // 流程圖節點和連結
        const nodes = ref<Node[]>([]);
        const links = ref<Link[]>([]);
        let nextNodeId = 1;
        let nextLinkId = 1;

        // 拖曳動作到流程圖區域
        const onDragStart = (event: DragEvent, action: { id: number; label: string }) => {
            event.dataTransfer?.setData('action', JSON.stringify(action));
        };

        const onDrop = (event: DragEvent) => {
            event.preventDefault();
            const actionData = event.dataTransfer?.getData('action');
            if (actionData) {
                const action = JSON.parse(actionData);
                const rect = (event.target as HTMLElement).getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                nodes.value.push({
                    id: nextNodeId++,
                    x,
                    y,
                    label: action.label,
                });
            }
        };

        // 節點拖曳
        const onNodeDragStart = (event: DragEvent, node: Node) => {
            event.dataTransfer?.setData('nodeId', node.id.toString());
        };

        // D3 拖曳行為
        const initDrag = () => {
            if (!svg.value) return;

            const svgElement = d3.select(svg.value);

            const drag = d3
                .drag<SVGRectElement, Node>()
                .on("start", (event, d) => {
                    d3.select(event.sourceEvent.target).attr("stroke", "red");
                })
                .on("drag", (event, d) => {
                    d.x = event.x;
                    d.y = event.y;
                    updateFlowchart();
                })
                .on("end", (event) => {
                    d3.select(event.sourceEvent.target).attr("stroke", "#0288d1");
                });

            svgElement.selectAll("rect").call(drag);
        };

        // 更新流程圖
        const updateFlowchart = () => {
            if (!svg.value) return;

            const svgElement = d3.select(svg.value);

            // 更新連線
            svgElement
                .selectAll("line")
                .data(links.value)
                .join("line")
                .attr("x1", (d) => nodes.value.find((n) => n.id === d.source)?.x || 0)
                .attr("y1", (d) => nodes.value.find((n) => n.id === d.source)?.y || 0)
                .attr("x2", (d) => nodes.value.find((n) => n.id === d.target)?.x || 0)
                .attr("y2", (d) => nodes.value.find((n) => n.id === d.target)?.y || 0)
                .attr("stroke", "#000")
                .attr("stroke-width", "2");

            // 更新節點
            svgElement
                .selectAll("rect")
                .data(nodes.value)
                .join("rect")
                .attr("x", (d) => d.x - 50)
                .attr("y", (d) => d.y - 20)
                .attr("width", 150)
                .attr("height", 40)
                .attr("rx", 5)
                .attr("fill", "#e0f7fa")
                .attr("stroke", "#0288d1")
                .attr("stroke-width", "2")
                .call(initDrag);

            svgElement
                .selectAll("text")
                .data(nodes.value)
                .join("text")
                .attr("x", (d) => d.x)
                .attr("y", (d) => d.y + 5)
                .attr("text-anchor", "middle")
                .attr("fill", "#000")
                .attr("font-size", "14")
                .text((d) => d.label);
        };

        // 點擊節點以創建或移除連線
        let selectedNode: Node | null = null;

        const onNodeClick = (node: Node) => {
            if (!selectedNode) {
                selectedNode = node;
                d3.select(`rect[x="${node.x - 50}"][y="${node.y - 20}"]`).attr("stroke", "red");
            } else if (selectedNode === node) {
                // 取消選擇
                selectedNode = null;
                d3.select(`rect[x="${node.x - 50}"][y="${node.y - 20}"]`).attr("stroke", "#0288d1");
            } else {
                // 檢查是否已存在連線
                const existingLink = links.value.find(
                    (link) =>
                        (link.source === selectedNode.id && link.target === node.id) ||
                        (link.source === node.id && link.target === selectedNode.id)
                );

                if (existingLink) {
                    // 移除連線
                    links.value = links.value.filter((link) => link !== existingLink);
                } else {
                    // 添加新連線
                    links.value.push({
                        id: nextLinkId++,
                        source: selectedNode.id,
                        target: node.id,
                    });
                }

                // 重置選擇
                d3.select(`rect[x="${selectedNode.x - 50}"][y="${selectedNode.y - 20}"]`).attr("stroke", "#0288d1");
                selectedNode = null;
                updateFlowchart();
            }
        };

        // 初始化
        onMounted(() => {
            updateFlowchart();
        });

        return {
            menuItems,
            actions,
            svg,
            width,
            height,
            nodes,
            links,
            onDragStart,
            onDrop,
            onNodeClick,
        };
    },
});
</script>

<style scoped>
.flowchart {
    border: 1px solid #ccc;
}
.function-panel {
    width: 200px;
}
.action-item {
    user-select: none;
}
</style>