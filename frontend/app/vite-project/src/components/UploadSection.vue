<template>
    <div class="relative space-y-4 max-w-[80%] mx-auto border p-4 rounded-md shadow">

        <!-- 遮罩 -->
        <div
            v-if="loading"
            class="absolute inset-0 bg-white/70 flex items-center justify-center z-10 rounded-md"
        >
            <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
            </svg>
        </div>

        <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-gray-700">上傳區塊</h2>

            <div class="flex space-x-2">
                <button
                    class="text-sm text-blue-600 hover:text-blue-800"
                    @click="collapsed = !collapsed"
                    :disabled="loading"
                >
                    {{ collapsed ? 'Expand' : 'Collapse'}}
                </button>
                <button
                    class="text-sm text-blue-600 hover:text-blue-800"
                    @click="$emit('remove-self')"
                    :disabled="loading"
                    title="Cancel upload"
                >
                    X
                </button>
            </div>
        </div>

        <div v-if="!collapsed">
            <div>
                <label for="file_name" class="block text-gray-600 mb-2">檔案名稱</label>
                <input
                    id="file_name"
                    type="text"
                    class="w-full border border-gray-300 rounded-md p-2"
                    v-model="localFileName"
                    readonly
                />
            </div>

            <div>
                <label for="ticket_code" class="block text-gray-600 mb-2">票卷號碼</label>
                <input
                    id="ticket_code"
                    type="text"
                    class="w-full border border-gray-300 rounded-md p-2"
                    v-model="localTicketCode"
                    :disabled="loading"
                />
            </div>

            <div>
                <label for="unzip_password" class="block text-gray-600 mb-2">解壓密碼</label>
                <input
                    id="unzip_password"
                    type="text"
                    class="w-full border border-gray-300 rounded-md p-2"
                    v-model="localUnzipPassword"
                    :disabled="loading"
                />
            </div>

            <div>
                <label for="description" class="block text-gray-600 mb-2">額外說明</label>
                <textarea
                    id="description"
                    class="w-full border border-gray-300 rounded-md p-2"
                    rows="3"
                    v-model="localDescription"
                    :disabled="loading"
                ></textarea>
            </div>

            <div class="text-center mt-4">
                <button
                    class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700"
                    @click="$emit('upload')"
                    :disabled="!localTicketCode || loading"
                >
                    上傳檔案
                </button>
            </div>

            <div v-if="progress > 0" class="mt-4">
                <p class="text-sm text-gray-600">上傳進度：{{ progress }}%</p>
                <div class="w-full bg-gray-200 rounded h-2 mt-1">
                    <div
                        class="bg-blue-500 h-2 rounded"
                        :style="{ width: progress + '%' }"
                    ></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import type { PropType } from 'vue';

export default defineComponent({
    name: 'UploadSection',
    props: {
        file_name: String,
        ticket_code: String,
        unzip_password: String,
        description: {
            type: String,
            default: ''
        },
        fileQueue: {
            type: Array as PropType<File[]>,
            required: true,
        },
        userId: {
            type: Number as PropType<number | null>,
            required: false,
        },
        progress: {
            type: Number,
            default: 0
        },
        loading: {
            type: Boolean,
            default: false
        }
    },
    emits: [
        'upload',
        'update:file_name',
        'update:ticket_code',
        'update:description',
        'remove-self',
        'update:unzip_password'
    ],
    setup(props, { emit }) {
        const localFileName = ref(props.file_name);
        const localTicketCode = ref(props.ticket_code);
        const localDescription = ref(props.description);
        const localUnzipPassword = ref(props.unzip_password);
        const collapsed = ref(false);

        watch(localFileName, val => emit('update:file_name', val));
        watch(localTicketCode, val => emit('update:ticket_code', val));
        watch(localDescription, val => emit('update:description', val));
        watch(localUnzipPassword, val => emit('update:unzip_password', val));

        return { localFileName, localTicketCode, localDescription, collapsed, localUnzipPassword };
    }
});
</script>
