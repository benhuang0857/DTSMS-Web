<template>
    <div class="mt-8 bg-white p-6 rounded-lg shadow-md max-w-[90%] mx-auto">
        <h2 class="text-xl font-bold mb-4">系統設定</h2>

        <div v-if="loading" class="text-gray-500">Loading settings...</div>
        <div v-else-if="error" class="text-red-500">Failed to load settings</div>
        <div v-else>
            <div v-for="setting in settings" :key="setting.id" class="mb-6 flex items-center space-x-2">
                <label class="flex-1">
                    <span class="block text-gray-600 mb-1">{{ setting.name }}</span>
                    <input v-model="setting.value" type="text"
                        class="w-full max-w-5xl border border-gray-300 rounded-md p-2" />
                    <p v-if="setting.description" class="text-sm text-gray-500 mt-1">
                        {{ setting.description }}
                    </p>
                </label>

                <label class="inline-flex items-center space-x-1 mt-6 whitespace-nowrap">
                    <input type="checkbox" v-model="setting.status" :true-value="'on'" :false-value="'off'"
                        class="form-checkbox h-5 w-5 text-blue-600" />
                    <span class="text-gray-700">Enabled</span>
                </label>
            </div>

            <div class="mt-6 flex justify-end space-x-4">
                <button class="px-4 py-2 text-gray-600 bg-gray-200 rounded-md hover:bg-gray-300" @click="fetchSettings">
                    Reset
                </button>
                <button class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700" @click="saveSettings">
                    Save
                </button>
            </div>
        </div>

    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import axios from "axios";

type WebSetting = {
    id: number;
    key: string;
    name: string;
    description: string | null;
    value: string;
    status: "on" | "off";
    created_time: string;
    updated_time: string;
};

export default defineComponent({
    name: "WebSettingForm",
    setup() {
        const settings = ref<WebSetting[]>([]);
        const loading = ref(false);
        const error = ref(false);

        const authToken = localStorage.getItem("token") || "";
        const domain = "http://172.31.176.1:8000";

        const fetchSettings = async () => {
            loading.value = true;
            error.value = false;
            try {
                const res = await axios.get(`${domain}/api/web-settings`, {
                    headers: { Authorization: `Bearer ${authToken}` },
                });
                settings.value = res.data;
            } catch (err) {
                console.error(err);
                error.value = true;
            } finally {
                loading.value = false;
            }
        };

        const saveSettings = async () => {
            try {
                for (const setting of settings.value) {
                    await axios.put(
                        `${domain}/api/web-settings/${setting.id}`,
                        { value: setting.value, status: setting.status },
                        {
                            headers: { Authorization: `Bearer ${authToken}` },
                        }
                    );
                }
                alert("Settings saved successfully!");
            } catch (err) {
                console.error(err);
                alert("Failed to save settings.");
            }
        };

        onMounted(() => {
            fetchSettings();
        });

        return {
            settings,
            loading,
            error,
            fetchSettings,
            saveSettings,
        };
    },
});
</script>
