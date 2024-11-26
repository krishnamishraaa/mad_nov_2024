<script setup>
import { ref } from 'vue';

const influencerCount = ref(6);
const sponsorCount = ref(10);
const campaignCount = ref(4);
const revenueAmount = ref(100000);

// Function to simulate updating values
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
    <div class="circle-stats">
        <!-- Influencers Circle -->
        <div class="circle" @click="updateStat('influencers', influencerCount + 1)">
            <div class="circle-title">Influencers</div>
            <div class="circle-value">{{ influencerCount }}</div>
        </div>

        <!-- Sponsors Circle -->
        <div class="circle" @click="updateStat('sponsors', sponsorCount + 1)">
            <div class="circle-title">Sponsors</div>
            <div class="circle-value">{{ sponsorCount }}</div>
        </div>

        <!-- Campaigns Circle -->
        <div class="circle" @click="updateStat('campaigns', campaignCount + 1)">
            <div class="circle-title">Campaigns</div>
            <div class="circle-value">{{ campaignCount }}</div>
        </div>

        <!-- Revenue Circle -->
        <div class="circle" @click="updateStat('revenue', revenueAmount + 10000)">
            <div class="circle-title">Revenue</div>
            <div class="circle-value">${{ revenueAmount }}</div>
        </div>
    </div>
</template>

<style scoped>
.circle-stats {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    margin-top: 0px;
    margin-bottom: auto;
}

.circle {
    width: 100px;
    height: 100px;
    background-color: #4CAF50;
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
    background-color: #388E3C;
}

.circle-title {
    font-size: 1em;
    font-weight: bold;
    margin-bottom: 5px;
}

.circle-value {
    font-size: 2em;
    font-weight: bold;
}
</style>
