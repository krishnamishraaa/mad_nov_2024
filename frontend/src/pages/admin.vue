<script setup>
import { ref, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import approval from '/src/components/approval.vue'
import statistics from '/src/components/statistics.vue'
import flagged from '/src/components/flagged.vue'
import adrequests from '/src/components/ad-requests.vue'
import tabsLayout from '/src/components/tabsLayout.vue'
import datacards from '/src/components/data_cards.vue'
import datacircles from '/src/components/data_circles.vue'


const defaultTab = 'approval';
const unapprovedSponsorCount = ref(0);

const sponsorCountUpdated = (count) => {
    unapprovedSponsorCount.value = count; // Update the count
};
const tabs = [
    { key: 'approval', label: 'Approval', component: approval },
    { key: 'statistics', label: 'Statistics', component: statistics},
    { key: 'flagged', label: 'Flagged', component: flagged},
    { key: 'adrequests', label: 'Ad Requests', component: adrequests},
];

</script>

<template>
    <h2> Influencer Management and Sponsor Coordination</h2>
    <h3>ADMIN DASHBOARD</h3>
    <tabsLayout :tabs="tabs" :defaultTab="defaultTab">
        <template #right-section>
            <div class="section">
                <h2>Attention : </h2>

                <p> Pending Sponsor Approvals:{{ unapprovedSponsorCount }}</p>
                <p> Current Enrollment Growth Rate is: </p>
                <p> Current Campaign Growth Rate is: </p>
                <p> Current Revenue Growth Rate is: </p>
            </div>

            <div class="bottomCssStats">
                <!-- Make Circular Charts showing Currenyt Statistics -->
                <datacards />
                <datacircles />
                Current Categories:
                Categories with most Influencers:
                Categories with most Campaigns:
                Categories with most Revenue:

            </div>
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
 text-align: right;

}
h3{
    color: #c5494b;
    text-align: center;
}
</style>


