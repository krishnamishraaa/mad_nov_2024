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
    category: {
        type: String,
        required: false,
        default: "",
    },
    budget: {
        type: String,
        required: false,
        default: "",
    },
    ad_requests: {
        type: Array,
        required: false,
        default: () => [],
    },
});


// Compute the gradient based on the progress
const gradientStyle = computed(() => {
    return {
        backgroundImage: `linear-gradient(to right, #4caf50 ${props.progress}%, transparent ${props.progress}%)`,
    };
});
</script>

<template>
    <div class="card" :style="gradientStyle">

        <div class="card-content">
            <h3>{{ title }}</h3>

            <p v-if="budget">Budget: {{ budget }}</p>
        
            <small>{{ progress }}% </small>
        


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
    color: rgb(249, 134, 4);
    margin:auto
}
p{
    color: rgb(203, 6, 6);
    margin: 0px;
    padding: 0px;
}
</style>