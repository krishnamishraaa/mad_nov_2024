<script setup>
import { ref } from 'vue';

// State for each stat
const influencerCount = ref(6);
const sponsorCount = ref(10);
const campaignCount = ref(4);
const revenueAmount = ref(100000);

// Function to simulate updating values (can be replaced with API calls)
const updateStat = (type, value) => {
    if (type === 'influencers') {
        influencerCount.value = value;
    } else if (type === 'sponsors') {
        sponsorCount.value = value;
    } else if (type === 'campaigns') {
        campaignCount.value = value;
    } else if (type === 'revenue') {
        revenueAmount.value = value;
    }
};
</script>

<template>
    <div class="stats-cards">
        <!-- Influencers Card -->
        <div class="card" @click="updateStat('influencers', influencerCount + 1)">
            <div class="card-title">Influencers</div>
            <div class="card-value">{{ influencerCount }}</div>
        </div>

        <!-- Sponsors Card -->
        <div class="card" @click="updateStat('sponsors', sponsorCount + 1)">
            <div class="card-title">Sponsors</div>
            <div class="card-value">{{ sponsorCount }}</div>
        </div>

        <!-- Campaigns Card -->
        <div class="card" @click="updateStat('campaigns', campaignCount + 1)">
            <div class="card-title">Campaigns</div>
            <div class="card-value">{{ campaignCount }}</div>
        </div>

        <!-- Revenue Card -->
        <div class="card" @click="updateStat('revenue', revenueAmount + 10000)">
            <div class="card-title">Revenue</div>
            <div class="card-value">${{ revenueAmount }}</div>
        </div>
    </div>
</template>

<style scoped>
.stats-cards {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 30px;
}

.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
    width: 200px;
    cursor: pointer;
    transition: transform 0.2s;
}

.card:hover {
    transform: scale(1.05);
}

.card-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}

.card-value {
    font-size: 2em;
    font-weight: bold;
    color: #4CAF50;
}

.card-value span {
    color: #FF5722;
}
</style>
