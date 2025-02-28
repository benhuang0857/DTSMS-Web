<template>
    <div class="space-y-4 max-w-[80%] mx-auto">
        <div>
            <label for="token" class="block text-gray-600 mb-2">Token</label>
            <input id="token" type="text" class="w-full border border-gray-300 rounded-md p-2" :value="token" readonly />
        </div>
        <div>
            <label class="block text-gray-600 mb-2">Uploaded</label>
            <div class="space-y-2">
                <input
                    v-for="file in uploadedFiles"
                    :key="file"
                    type="text"
                    class="w-full border border-gray-300 rounded-md p-2"
                    :value="file"
                    readonly
                />
            </div>
        </div>
        <div class="text-center">
            <button
                class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700"
                @click="$emit('upload')"
                :disabled="fileQueue.length === 0"
            >
                UPLOAD FILES
            </button>
            <p v-if="fileQueue.length > 0" class="text-gray-600 mt-2">
                已選擇 {{ fileQueue.length }} 個文件等待上傳
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue'; // 使用 type-only 導入

export default defineComponent({
    name: 'UploadSection',
    props: {
        token: {
            type: String,
            required: true,
        },
        uploadedFiles: {
            type: Array as PropType<string[]>,
            required: true,
        },
        fileQueue: {
            type: Array as PropType<File[]>,
            required: true,
        },
        userId: {
            type: Number as PropType<number | null>,
            required: false,
        },
    },
    emits: ['upload'],
});
</script>