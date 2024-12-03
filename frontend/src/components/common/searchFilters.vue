<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
    filters: {
        type: Object,
        required: true,
    },
});
const emit = defineEmits(['updateFilters']);

const category = ref(props.filters.category || '');
const niche = ref(props.filters.niche || '');
const reach = ref(props.filters.reach || 0);

// Watch for input changes and immediately emit updated filters
watch([category, niche, reach], ([newCategory, newNiche, newReach]) => {
    emit('updateFilters', {
        category: newCategory,
        niche: newNiche,
        reach: newReach,
    });
});
</script>


<template>
    <div class="searchBox">
        <h6>Filter Results: </h6>
        <input v-model="category" type="text" placeholder="Filter by Category" />
        <input v-model="niche" type="text" placeholder="Filter by Niche" />
        <input v-model.number="reach" type="number" placeholder="Minimum Reach" />
    </div>
</template>

<style scoped>
input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 5px;
}

button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.searchBox {
    display: flex;
    gap: 10px;
    margin: 10px;
    background-color: rgb(232, 238, 244);
}

h6{
    text-align: center;
    font-size: 1em;
    margin-top: 10px;
    margin-left: 15px;

}
</style>
