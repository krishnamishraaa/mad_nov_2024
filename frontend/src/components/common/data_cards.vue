<script setup>
import { defineProps, defineEmits } from 'vue';


const props = defineProps({
    stats: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});


const emit = defineEmits(['updateStats']);


const handleStatUpdate = (title, value) => {
    props.stats[title] = value; 
    emit('updateStats', props.stats);
};
</script>

<template>
    <div class="stats-cards">
       
        <div v-for="(value, title) in props.stats" :key="title" class="card" @click="handleStatUpdate(title, value)">
            <div class="card-title">{{ title.toUpperCase() }}</div>

            
            <div class="card-value" v-if="Array.isArray(value)">
                <div v-for="(val, index) in value" :key="index">
                    <p> {{ val.name }}:<small> {{ val.reach || val.budget || val.sponsor }}</small></p>
                </div>
            </div>

           
            <div class="card-value" v-else>
                {{ value }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.stats-cards {
    display: flex;
    justify-content:flex-start;
    margin-top: 30px;
    flex-wrap: wrap;
}


.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
    text-wrap: wrap;
    width: 150px;
    cursor: pointer;
    margin:auto;
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
    font-size: 0.75em;
    color: #4caf50;
}

.card-value span {
    color: #ff5722;
}
p{
    text-overflow: ellipsis;
        display: block;
        white-space: nowrap;
        overflow: hidden;

}
</style>
