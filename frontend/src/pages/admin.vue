<script setup>
import approval from '/src/components/admin/approval.vue'
import statistics from '/src/components/common/statistics.vue'
import flagged from '/src/components/admin/flagged.vue'
import adrequests from '/src/components/ad_request/ad-requests.vue'
import tabsLayout from '/src/components/common/tabsLayout.vue'
import datacards from '/src/components/common/data_cards.vue'
import datacircles from '/src/components/common/data_circles.vue'
import { ref, onMounted } from 'vue'


const defaultTab = 'approval';
const tabs = [
    { key: 'approval', label: 'Approval', component: approval },
    { key: 'statistics', label: 'Statistics', component: statistics},
    { key: 'flagged', label: 'Flagged', component: flagged},
    { key: 'adrequests', label: 'Ad Requests', component: adrequests},
];
const summaryStats = ref({});
const fetchStatistics = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/insights', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('auth-token'),
                'userDetails': localStorage.getItem('userDetails'),
            },
        });
        const data = await response.json();
        summaryStats.value = data;
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
};
onMounted(() => {
    fetchStatistics();
}); 

</script>

<template>
    <h2> Influencer Management and Sponsor Coordination</h2>
    <h3>ADMIN DASHBOARD</h3>
    <tabsLayout :tabs="tabs" :defaultTab="defaultTab">
        <template #right-section>
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
h1{
    color: #48b944;
}
h2{
    color: #ff9900;
 text-align: center;

}
h3{
    color: #c5494b;
    text-align: center;
}
</style>


