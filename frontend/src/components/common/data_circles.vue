<script setup>
import { computed } from 'vue';


const props = defineProps({
    stats: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});

const topStats = computed(() => {
    return Object.entries(props.stats).slice(0, 6).map(([title, value]) => ({
        title: title,
        value: value,
        type: title.toLowerCase().replace(/\s+/g, '_') 
    }));
});

</script>

<template>
    <div class="circle-stats">
        <div class="circle" v-for="stat in topStats" :key="stat.type" @click="updateStat(stat)">

            <div class="circle-value">
                {{stat.value}}
            </div>
            <div class="circle-title">{{ stat.title }}</div>
        </div>
    </div>
</template>

<style scoped>
.circle-stats {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
    margin-bottom: auto;
}

/* Style for individual circles */
.circle {
    width: 100px;
    height: 100px;
    background-color: #4caf50;
    border-radius: 50%;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    cursor: pointer;
    transition: transform 0.2s, background-color 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.circle:hover {
    transform: scale(1.1);
    background-color: #388e3c;
}

/* Circle title style */
.circle-title {
    font-size: 1em;
    margin-bottom: 5px;
}

/* Circle value style */
.circle-value {
    font-size: 1em;
    font-weight: bold;
}
</style>
