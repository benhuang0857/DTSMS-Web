<template>
    <div
        class="border-dashed border-2 border-gray-300 rounded-lg p-6 text-center max-w-[80%] mx-auto"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        :class="{ 'bg-gray-100': isDragging }"
    >
        <input
            type="file"
            ref="fileInput"
            class="hidden"
            @change="onFileSelected"
            multiple
        />
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
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'DragAndDrop',
    setup(_, { emit }) {
        const isDragging = ref(false);
        const fileInput = ref<HTMLInputElement | null>(null);

        const onDragOver = () => {
            isDragging.value = true;
        };

        const onDragLeave = () => {
            isDragging.value = false;
        };

        const onDrop = (event: DragEvent) => {
            isDragging.value = false;
            const files = event.dataTransfer?.files;
            if (files && files.length > 0) {
                emit('file-dropped', files[0]); // 發送單個文件，可改為多文件
            }
        };

        const onBrowse = () => {
            if (fileInput.value) {
                fileInput.value.click();
            }
        };

        const onFileSelected = (event: Event) => {
            const target = event.target as HTMLInputElement;
            const files = target.files;
            if (files && files.length > 0) {
                emit('file-dropped', files[0]); // 發送單個文件，可改為多文件
            }
        };

        return {
            isDragging,
            fileInput,
            onDragOver,
            onDragLeave,
            onDrop,
            onBrowse,
            onFileSelected,
        };
    },
});
</script>

<style scoped>
.bg-gray-100 {
    background-color: #f7fafc;
}
</style>