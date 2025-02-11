<template>
    <div class="border-dashed border-2 border-gray-300 rounded-lg p-6 text-center max-w-[80%] mx-auto">
        <p class="text-gray-600">
            Drag & drop files or
            <span class="text-blue-500 cursor-pointer" @click="onBrowse">Browse</span>
        </p>
        <p class="text-sm text-gray-400 mt-2">
            Supported formats: JPEG, PNG, GIF, MP4, PDF, etc.
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'DragAndDrop',
    methods: {
        onBrowse() {
            // 添加 "Browse" 點擊行為
            console.log('Browse clicked');
        },
    },
});
</script>