<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import tabLayout from '/src/components/common/tabsLayout.vue'
import adrequests from '/src/components/ad_request/ad-requests.vue'
import currentengagement from '/src/components/common/statistics.vue'
import profileedit from '/src/pages/register.vue'
import publiccampaignsearch from '/src/components/influencer/view_campaign.vue'

const defaultTab = 'adrequests';
const tabs = [
    { key: 'adrequests', label: 'Ad Requests', component: adrequests },
    { key: 'currentengagement', label: 'Current Engagement & Earnings', component: currentengagement },
    { key: 'profileedit', label: 'Profile Edit', component: profileedit },
    { key: 'publiccampaignsearch', label: 'Public Campaign Search', component: publiccampaignsearch },
];
</script>

<template>
    <h1> Welcome to the Influencer Dashboard</h1>
    <tabLayout :tabs="tabs" :defaultTab="defaultTab">
        <template v-slot:top-right-content>

        </template>
    </tabLayout>
</template>

<style scoped>

.sections {
    border: 1px solid #f15b5b;
    padding: 20px;
    background-color: #e8eed5;
    display: grid;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.container{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 20px;
    height: 100vh;
    margin: 0;
    padding: 20px;
    box-sizing: border-box;
}
h1{
    text-align: center;
    color: #f15b5b;
    font-size: 2em;
    font-weight: bold;
    margin: 0;
    padding: 20px;
    background-color: #e8eed5;
}

</style>