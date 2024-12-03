<script setup>
import { ref, watch } from 'vue';

// Define props to accept initial filter values
const props = defineProps({
    filters: {
        type: Object,
        required: true,
    },
});


const emit = defineEmits(['updateFilters']);


const filterFields = ref(
    Object.fromEntries(
        Object.keys(props.filters).map((key) => [key, props.filters[key] || ''])
    )
);


watch(
    () => filterFields.value,
    (newFilters) => {
        emit('updateFilters', { ...newFilters });
    },
    { deep: true }
);
</script>

<template>
    <div>
        <!-- Dynamically generate inputs based on filter fields -->
        <div v-for="(value, key) in filterFields" :key="key">
            <input v-model="filterFields[key]" :type="typeof value === 'number' ? 'number' : 'text'"
                :placeholder="'Filter by ' + key.charAt(0).toUpperCase() + key.slice(1)" />
        </div>
    </div>
</template>

<style scoped>
input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 5px;
    width: calc(100% - 22px);
}
</style>
