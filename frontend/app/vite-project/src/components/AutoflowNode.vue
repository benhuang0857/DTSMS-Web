<template>
  <div class="autoflow-node-wrapper">
    <div class="node-header autoflow-node">
      <i class="fas fa-project-diagram"></i>
      <span class="node-title">{{ data.name }}</span>
    </div>
    <div class="node-content">
      <p class="node-description">{{ data.description || '' }}</p>
      <div class="node-meta">
        <span class="badge">{{ data.processing_steps_count || data.processing_steps?.length || 0 }} steps</span>
      </div>
      <Handle id="autoflow-target" type="target" position="top" />
      <Handle id="autoflow-source" type="source" position="bottom" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Handle } from '@vue-flow/core';

interface Props {
  id: string;
  type: string;
  data: any;
  events?: any;
  selected?: boolean;
  resizing?: boolean;
  dragging?: boolean;
  connectable?: boolean;
  position?: { x: number; y: number };
  dimensions?: { width: number; height: number };
  isValidTargetPos?: boolean;
  isValidSourcePos?: boolean;
  parent?: string;
  parentNodeId?: string;
  zIndex?: number;
  targetPosition?: string;
  sourcePosition?: string;
  label?: string;
  dragHandle?: string;
}

defineProps<Props>();
</script>

<style scoped>
.node-header {
  @apply flex items-center space-x-2 p-2 border-b;
}

.node-title {
  @apply font-medium text-gray-800;
}

.node-content {
  @apply p-3;
}

.node-description {
  @apply text-sm text-gray-600 mb-2;
}

.node-meta {
  @apply flex space-x-2 mt-2;
}

.badge {
  @apply px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700;
}
</style>