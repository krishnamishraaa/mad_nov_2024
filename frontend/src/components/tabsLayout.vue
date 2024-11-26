<script setup>
import { ref, computed } from 'vue';
import { defineProps, defineEmits } from 'vue';


const emit = defineEmits(['tab-change']);

const props = defineProps({
    tabs: {
        type: Array,
        required: true,
    },
    defaultTab: {
        type: String,
        required: false,
        default: '',
    },
});

// Compute the default tab
const defaultTab = computed(() => props.defaultTab || props.tabs[0]?.key);

// Reactive active tab state
const activeTab = ref(defaultTab.value);

// Change tab and emit event
const changeTab = (tab) => {
    activeTab.value = tab;
    emit('tab-change', tab);
};
</script>

<template>
    <div class="tabs-layout">
        <!-- Top Section -->
        <div class="top-section">
            <!-- Tab Navigation -->
            <div class="tab-container">
                <div class="tabs">
                    <button v-for="tab in props.tabs" :key="tab.key" @click="changeTab(tab.key)"
                        :class="{ active: activeTab === tab.key }">
                        {{ tab.label }}
                    </button>
                </div>
            </div>
            <!-- Right Div -->
            <div class="right-box">
                <slot name="top-right-content">
                    
                </slot>
            </div>
        </div>

        <!-- Split Screen Layout -->
        <div class="split-screen">
            <!-- Left Panel -->
            <div class="left-panel">
                <!-- Render the active tab's content -->
                <component :is="props.tabs.find(tab => tab.key === activeTab)?.component" />
            </div>

            <!-- Right Panel -->
            <div class="right-panel">
                <slot name="right-section"></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>
.tabs-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.top-section {
    display: flex;
    justify-content: space-between;
    /* Distribute tabs and right box */
    align-items: center;
    /* Vertically align items */
    margin-bottom: 20px;
}

.tab-container {
    flex-grow: 1;
    /* Tabs take as much space as available */
}

.tabs {
    display: flex;
    gap: 10px;
}

.tabs button {
    padding: 10px 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    background-color: white;
    text-align: center;
}

.tabs button.active {
    background-color: #007bff;
    color: white;
    font-weight: bold;
}

.right-box {
    flex-shrink: 0;
    /* Prevent the box from shrinking */
    margin-left: 0px;
    background-color: #fff;
    padding: 20px;
    border-radius: 5px;
}

.split-screen {
    display: flex;
    height: 100%;
    gap: 20px;
}

.left-panel {
    flex: 2;
    /* Left panel takes 2/3 of space */
}

.right-panel {
    flex: 1;
    /* Right panel takes 1/3 of space */
    overflow-y: auto;
}
</style>
