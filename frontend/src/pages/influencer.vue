<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import tabLayout from '/src/components/common/tabsLayout.vue'
import adrequests from '/src/components/ad_request/ad-requests.vue'
import currentengagement from '/src/components/common/statistics.vue'
import profileedit from '/src/components/influencer/edit_prof_influencer.vue'
import publiccampaignsearch from '/src/components/influencer/view_campaign.vue'
import datacards from '/src/components/common/data_cards.vue'

const defaultTab = 'adrequests';
const tabs = [
    { key: 'adrequests', label: 'Ad Requests', component: adrequests },
    { key: 'currentengagement', label: 'Current Engagement & Earnings', component: currentengagement },
    { key: 'profileedit', label: 'Profile Edit', component: profileedit },
    { key: 'publiccampaignsearch', label: 'Public Campaign Search', component: publiccampaignsearch },
];

const summaryStats = ref({});
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const fetchStatistics = async () => {
    try {
        const response = await fetch('http://127.0.01:5000/api/insights', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        const data = await response.json();
        summaryStats.value = data;
    } catch (error) {
        console.error('Error:', error);
    }
};
const handleStatUpdate = (updatedStat) => {
    summaryStats.value = { ...summaryStats.value, ...updatedStat };
};
onMounted(() => {
    fetchStatistics();

});
</script>

<template>
    <h2> Influencer Management and Sponsor Coordination</h2>
    <h3>INFLUENCER DASHBOARD</h3>
    <tabLayout :tabs="tabs" :defaultTab="defaultTab">
        <template v-slot:top-right-content>


        </template>
        <template v-slot:right-section>
            <datacards :stats="summaryStats" @statUpdated="handleStatUpdate" />

        </template>
    </tabLayout>
</template>

<style scoped>

h2{
    text-align: center;
    color: #090101;
    font-size: 1.5em;
    font-weight: bold;
    margin: 0;
    padding: 10px;

}
h3{
    text-align: center;
    color: #f49004;
    font-size: 1em;
   
    margin: 0;
    padding: 10px;

}

</style>