<template>
    <div class="top-section flex justify-between items-center mb-6 max-w-[80%] mx-auto">
        <!-- 圓餅圖 -->
        <div class="w-1/2 flex justify-center">
            <DTSMSPieChart class="w-[350px] h-[350px]" />
        </div>
        <!-- 表格 -->
        <div class="w-1/2">
            <table class="table-auto w-full border-collapse">
                <thead>
                    <tr class="text-left text-gray-600 border-b">
                        <th class="pb-2">Label</th>
                        <th class="pb-2">Value</th>
                        <th class="pb-2">%</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in rows" :key="row.label" class="border-b">
                        <td>{{ row.label }}</td>
                        <td>{{ row.value }}</td>
                        <td>{{ row.percentage }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import DTSMSPieChart from '@/components/PieChart.vue';

export default defineComponent({
    name: 'TopSection',
    components: {
        DTSMSPieChart, // 引入圓餅圖組件
    },
    props: {
        rows: {
            type: Array as PropType<Array<{ label: string; value: number; percentage: string }>>,
            required: true,
        },
    },
});
</script>