<template>
    <div class="flex h-screen">
        <LeftMenu :menuItems="menuItems" />

        <main class="flex-1 flex">
            <div class="dashboard-container flex-1 p-10px">
                <TopSection :rows="tableRows" />
                <DragAndDrop />
                <UploadSection token="TWTWT1089TWT1089&xsrf" :uploadedFiles="['document-name.PDF']" />
            </div>
        </main>

    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import LeftMenu from '@/components/LeftMenu.vue';
import TopSection from '@/components/TopSection.vue';
import DragAndDrop from '../components/DragAndDrop.vue';
import UploadSection from '../components/UploadSection.vue';

export default defineComponent({
    name: 'Dashboard',
    components: {
        LeftMenu,
        TopSection,
        DragAndDrop,
        UploadSection
    },
    setup() {
        const menuItems = ref([
            { label: 'Dashboard', link: '/dashboard', icon: 'fas fa-tachometer-alt', active: true },
            { label: 'Automation Control', link: '/automation', icon: 'fas fa-robot', active: false },
            { label: 'Download History', link: '/downloads', icon: 'fas fa-download', active: false },
            { label: 'Submission', link: '/submissions', icon: 'fas fa-upload', active: false },
            { label: 'Setting', link: '/setting', icon: 'fas fa-cog', active: false },
        ]);

        const tableRows = ref([
            { label: 'Macro', value: 12, percentage: '28.6%' },
            { label: 'Boot Strap Sector', value: 22, percentage: '42.9%' },
            { label: 'File Infectors Virus', value: 12, percentage: '28.6%' },
            { label: 'Label 4', value: 12, percentage: '28.6%' },
            { label: 'Label 5', value: 7, percentage: '14.3%' },
            { label: 'Label 6', value: 7, percentage: '14.3%' },
        ]);

        return { menuItems, tableRows };
    },
});
</script>