<script setup>

import { ref, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import tabsLayout from '/src/components/common/tabsLayout.vue'
import datacards from '/src/components/common/data_cards.vue'
import datacircles from '/src/components/common/data_circles.vue'
import campaignForm from '/src/components/sponsor/campaignForm.vue'
import influencers from '/src/components/sponsor/explore_INfluencier.vue'
import status from '/src/components/sponsor/campaign_status.vue'
import adrequest from '/src/components/ad_request/ad-requests.vue'
import statistics from '../components/common/statistics.vue';
import { on } from 'events';

const summaryStats = ref({});

const handleStatUpdate = (updatedStat) => {
    sponsorStats.value = { ...summaryStats.value, ...updatedStat };
};

const defaultTab = 'create';

const tabs = [
    { key: 'create', label: 'Create Campaign', component: campaignForm },
    { key: 'search', label: 'Search Influencers', component: influencers },
    { key: 'status', label: 'Campaign Status', component: status },
    { key:'adrequest', label: 'AD Requests', component: adrequest},
];

const userDetails = localStorage.getItem('userDetails');
const authToken = localStorage.getItem('auth-token');

// ASYNCHRONUS Celery running is must for this function to work
const download_campaign = async () => {
    
    try {
        const response = await fetch('http://127.0.0.1:5000/download_csv', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json, text/csv',
                'Authentication-Token': localStorage.getItem('auth-token'),
            },
        })
        const data = await response.json()
        if (response.ok) {
            console.log(data)
            const taskId = data['task_id']
            console.log(taskId)
            const in_ter_val = setInterval(async () => {
                const csv_res = await fetch(`http://127.0.0.1:5000/getcsv/${taskId}`)
                if (csv_res.ok) {
                    clearInterval(in_ter_val)
                    window.location.href = `http://127.0.0.1:5000/getcsv/${taskId}`
                    alert('Downloaded Successfully')
                }
            },1000)
        }


        console.log(data)
    } catch (error) {
        console.error('Error fetching data:', error);
    }

}

const getInsights = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/insights', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': localStorage.getItem('userDetails'),
            },
        });
        const data = await response.json();
        summaryStats.value = data;
    } catch (error) {
        console.error('Error fetching insights:', error);
    }
};


onMounted(() => {
    getInsights();
});

</script>

<template>
    <h2> Influencer Management and Sponsor Coordination</h2>
    <h3>SPONSOR DASHBOARD</h3>

    <tabsLayout :tabs="tabs" :defaultTab="defaultTab">
        <template v-slot:top-right-content>
            <button class="btn btn-success" @click="download_campaign">DOWNLOAD CAMPAIGN DATA</button>
        </template>
        
        <template v-slot:right-section>
            <datacards :stats="summaryStats" @statUpdated="handleStatUpdate" />

        </template>

    </tabsLayout>
</template>

<style scoped>
/* Style for container */
.container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    /* Two columns */
    grid-template-rows: 1fr 1fr;
    /* Two rows */
    gap: 20px;
    /* Gap between grid items */
    height: 100vh;
    /* Full viewport height */
    margin: 0;
    /* No margin */
    padding: 20px;
    /* Padding for container */
    box-sizing: border-box;
}

/* Style for individual sections */
.section {

    padding: 20px;
    /* Padding inside each section */
    background-color: #fdfdfa;
    /* Light background color */
    display: flex;
    /* Flexbox layout */
    flex-direction: column;
    /* Stack content vertically */
    justify-content: center;
    /* Center content vertically */
    align-items: right;
    /* Center content horizontally */
    text-align: right;
    /* Align text to center */
}

h1 {
    color: #48b944;
}

h2 {
    color: #ff9900;
    text-align: center;
    margin-bottom: 0px;
    margin-top: 0px;

}

h3 {
    color: #c5494b;
    text-align: center;
}

</style>
