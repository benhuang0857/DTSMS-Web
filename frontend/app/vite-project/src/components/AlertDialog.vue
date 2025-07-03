<template>
    <div
        v-if="visible"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
        <div class="bg-white rounded-lg shadow-lg p-6 max-w-sm w-full text-center">
            <h2 class="text-xl font-bold mb-2">{{ title }}</h2>
            <p class="mb-4">{{ message }}</p>

            <div
                v-if="loading"
                class="animate-spin w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full mx-auto"
            ></div>

            <button
                v-else
                class="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                @click="$emit('close')"
            >
                關閉
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'AlertDialog',
    props: {
        visible: { type: Boolean, required: true },
        title: { type: String, default: '' },
        message: { type: String, default: '' },
        loading: { type: Boolean, default: false },
    },
    emits: ['close'],
});
</script>

<style scoped>
</style>
