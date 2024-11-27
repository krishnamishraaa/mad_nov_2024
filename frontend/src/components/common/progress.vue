<script setup>
import { computed, defineProps } from "vue";

// Props for the reusable component
const props = defineProps({
    title: {
        type: String,
        required: true,
    },
    progress: {
        type: Number,
        required: true,
        validator: (value) => value >= 0 && value <= 100,
    },
    description: {
        type: String,
        required: false,
        default: "",
    },
});

const editCampaign = () => {
    console.log('Editing campaign:', props.title);
    
};
const deleteCampaign = () => {
    console.log('Deleting campaign:', props.title);
};

// Compute the gradient based on the progress
const gradientStyle = computed(() => {
    return {
        backgroundImage: `linear-gradient(to right, #4caf50 ${props.progress}%, transparent ${props.progress}%)`,
    };
});
</script>

<template>
    <div class="card" :style="gradientStyle">
        <button id="one" @click="editCampaign">
            <i class="bi bi-pen"><small>Edit</small></i>
        </button>
        <button id="two" @click="deleteCampaign">
            <i class="bi bi-trash-fill"></i><small>Delete</small>
        </button>
        <div class="card-content">
            <h3>{{ title }}</h3>
            <p v-if="description">{{ description }}</p>
            <p v-if="budget">Budget: {{ budget }}</p>
            <p v-if="category">Category: {{ category }}</p>
        </div>
    </div>

</template>
<style scoped>
.card {
    position: relative;
    width: 200px;
    height: 150px;
    border: 2px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    color: #fff;
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    transition: background-image 0.3s ease-in-out;
}

.card-content {
    position: relative;
    z-index: 2;
    text-align: center;
}
#one {
    position: absolute;
    bottom: 0;
    left: 0;
    background-color: #4caf50;
    border: none;
    border-radius: 0 4px 0 0;
    padding: 5px;
    cursor: pointer;
}
#two {
    position: absolute;
    bottom: 0;
    right: 0;
    background-color: #ffffff;
    border: none;
    border-radius: 4px 0 0 0;
    padding: 5px;
    cursor: pointer;
}
</style>