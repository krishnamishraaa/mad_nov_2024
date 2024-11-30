<script setup>
import { ref } from 'vue';

// Props to accept dynamic data (now expecting an object instead of separate values)
const props = defineProps({
    stats: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});

// Store updated stats
const stats = ref(props.stats);

const handleStatUpdate = (title, value) => {
    // Update the value of the selected stat
    stats.value[title] = value;
};

</script>

<template>
    <div class="stats-cards">
        <!-- Loop through the stats dictionary and display each card dynamically -->
        <div v-for="(value, title) in stats" :key="title" class="card" @click="handleStatUpdate(title, value)">
            <div class="card-title">{{ title.toUpperCase() }}</div>

            <!-- Check if value is an array and display accordingly -->
            <div class="card-value" v-if="Array.isArray(value)">
                <div v-for="(val, index) in value" :key="index">
                    <!-- Assuming val is an object with properties 'name', 'reach', 'budget' -->
                    <p> {{ val.name }}:<small> {{ val.reach || val.budget }}</small></p>
                </div>
            </div>

            <!-- Default display for non-array value -->
            <div class="card-value" v-else>
                {{ value }}
            </div>
        </div>
    </div>
</template>


<style scoped>
.stats-cards {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 30px;
    flex-wrap: wrap;
}

/* Style for individual cards */
.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
    text-wrap: wrap;
    width: 150px;
    cursor: pointer;
    transition: transform 0.2s;
}

.card:hover {
    transform: scale(1.05);
}

/* Card title style */
.card-title {
    font-size: 0.8em;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

/* Card value style */
.card-value {
    font-size: 0.8em;
    color: #4caf50;
}

.card-value span {
    color: #ff5722;
}
</style>
