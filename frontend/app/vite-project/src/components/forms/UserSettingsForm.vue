<template>
    <div class="mt-8 bg-white p-6 rounded-lg shadow-md max-w-[90%] mx-auto">
        <h2 class="text-xl font-bold mb-4">用戶基本資料設定</h2>
        <div class="grid grid-cols-2 gap-6 mb-4">
            <div>
                <label for="username" class="block text-gray-600 mb-2">Username</label>
                <input id="username" v-model="form.username" type="text"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>

            <div>
                <label for="real-name" class="block text-gray-600 mb-2">Real Name</label>
                <input id="real-name" v-model="form.real_name" type="text"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>

            <div>
                <label for="email" class="block text-gray-600 mb-2">Email</label>
                <input id="email" v-model="form.email" type="email"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>

            <div>
                <label for="organization" class="block text-gray-600 mb-2">Organization</label>
                <input id="organization" v-model="form.organization" type="text"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>

            <div>
                <label for="address" class="block text-gray-600 mb-2">Address</label>
                <input id="address" v-model="form.address" type="text"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>

            <div>
                <label for="mobile" class="block text-gray-600 mb-2">Mobile</label>
                <input id="mobile" v-model="form.mobile" type="text"
                    class="w-full border border-gray-300 rounded-md p-2" />
            </div>
        </div>

        <div class="border-dashed border-2 border-gray-300 rounded-md p-6 text-center" @dragover.prevent="onDragOver"
            @dragleave.prevent="onDragLeave" @drop.prevent="onDrop">
            <input type="file" ref="fileInput" class="hidden" @change="onFileSelected" accept=".svg,.png,.jpg,.gif" />
            <p class="text-gray-600">
                Click to upload or drag and drop
                <span class="text-blue-500 cursor-pointer" @click="onBrowse">Browse</span>
            </p>
            <p class="text-sm text-gray-400 mt-2">
                SVG, PNG, JPG or GIF (max, 800x400px)
            </p>
            <p v-if="uploadFile" class="text-gray-600 mt-2">{{ uploadFile.name }}</p>
        </div>

        <div class="mt-6 flex justify-end space-x-4">
            <button class="px-4 py-2 text-gray-600 bg-gray-200 rounded-md hover:bg-gray-300" @click="resetForm">
                Reset
            </button>
            <button class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700" @click="saveForm">
                Save
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import type { PropType } from "vue";

type UserForm = {
    username: string;
    email: string;
    real_name: string;
    organization: string;
    address: string;
    mobile: string;
    avatar: string;
};

export default defineComponent({
    name: "UserSettingsForm",
    props: {
        form: {
            type: Object as PropType<UserForm>,
            required: true as true,
        },
        uploadFile: {
            type: Object as PropType<File | null>,
            required: true as true,
        },
        onDragOver: {
            type: Function as PropType<() => void>,
            required: true as true,
        },
        onDragLeave: {
            type: Function as PropType<() => void>,
            required: true as true,
        },
        onDrop: {
            type: Function as PropType<(e: DragEvent) => void>,
            required: true as true,
        },
        onBrowse: {
            type: Function as PropType<() => void>,
            required: true as true,
        },
        onFileSelected: {
            type: Function as PropType<(e: Event) => void>,
            required: true as true,
        },
        resetForm: {
            type: Function as PropType<() => void>,
            required: true as true,
        },
        saveForm: {
            type: Function as PropType<() => void>,
            required: true as true,
        },
    },
});

</script>
