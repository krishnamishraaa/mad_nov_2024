<script setup>
import { ref, onMounted } from 'vue';
import datacircles from '/src/components/common/data_circles.vue';
import datacards from '/src/components/common/data_cards.vue';

const stats_data = ref({});
const summaryStats = ref({});
const budgetUsage = ref(0);

const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const fetchStatistics = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/stats', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        const data = await response.json();
        stats_data.value = data;
        console.log(data);

        if (data.remainingBudget && data.totalBudget) {
            budgetUsage.value = ((data.totalBudget - data.remainingBudget) / data.totalBudget) * 100;
        }

        emit('totalInfluencers', data.influencers);
        emit('totalCampaigns', data.campaigns);
    } catch (error) {
        console.error('Error:', error);
    }
};

onMounted(() => {
    fetchStatistics();
});
</script>

<template>
    <div class="dashboard">

        <!-- Admin Specific Stats -->
        <section v-if="userDetails.role === 'admin'" class="role-specific">

            <div class="admin-stats">
                <div class="admin-card">
                    <h3><small>Total</small> Reach</h3>
                    <p>{{ stats_data.totalReach }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Budget</h3>
                    <p>{{ stats_data.totalBudget }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Runnig Ads</h3>
                    <p>{{ stats_data.adRequests }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Campaigns</h3>
                    <p>{{ stats_data.campaigns }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Categories</h3>
                    <p>{{ stats_data.uniquecategories }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Influencers</h3>
                    <p>{{ stats_data.influencers }}</p>
                </div>
                <div class="admin-card">
                    <h3><small>Total</small> Sponsors</h3>
                    <p>{{ stats_data.sponsors }}</p>
                </div>


                <div class="admin-card">
                    <h3>Pending Ad Requests</h3>
                    <p>{{ stats_data.pendingAdRequests }}</p>
                </div>


            </div>
        </section>

        <!-- Sponsor Specific Stats -->
        <section v-if="userDetails.role === 'sponsor'" class="role-specific">
            <h2>Sponsor Insights</h2>
            <p>Remaining Budget: {{ stats_data.remainingBudget }}</p>
            <progress :value="budgetUsage" max="100"></progress>
            <p>Budget Used: {{ budgetUsage }}%</p>

            <div class="sponsor-stats">
                <div class="sponsor-card">
                    <h3><small>Total</small> Campaigns</h3>
                    <p>{{ stats_data.campaigns }}</p>
                </div>
                <div class="sponsor-card">
                    <h3><small>Total</small> Ad Requests</h3>
                    <p>{{ stats_data.adRequests_total }}</p>
                </div>
                <div class="sponsor-card">
                    <h3>Pending Ad Requests</h3>
                    <p>{{ stats_data.adRequests_pending }}</p>
                </div>
                <div class="sponsor-card">
                    <h3>Accepted Ad Requests</h3>
                    <p>{{ stats_data.adRequests_accepted }}</p>
                </div>
                <div class="sponsor-card">
                    <h3>Rejected Ad Requests</h3>
                    <p>{{ stats_data.adRequests_rejected }}</p>
                </div>
            </div>
        </section>

        <!-- Influencer Specific Stats -->
        <section v-if="userDetails.role === 'influencer'" class="role-specific">
            <h2>Influencer Insights</h2>
            <div class="influencer-stats">
                <div class="influencer-card">
                    <h3><small>Total</small> Ad Requests</h3>
                    <p>{{ stats_data.adRequests_total }}</p>
                </div>
                <div class="influencer-card">
                    <h3>Pending Ad Requests</h3>
                    <p>{{ stats_data.adRequests_pending }}</p>
                </div>
                <div class="influencer-card">
                    <h3>Accepted Ad Requests</h3>
                    <p>{{ stats_data.adRequests_accepted }}</p>
                </div>
                <div class="influencer-card">
                    <h3>Rejected Ad Requests</h3>
                    <p>{{ stats_data.adRequests_rejected }}</p>
                </div>
                <div class="influencer-card">
                    <h3><small>Total</small> Earnings</h3>
                    <p>{{ stats_data.totalEarnings }}</p>
                </div>
                <div class="influencer-card">
                    <h3>Earnings This Month</h3>
                    <p>{{ stats_data.EarningThisMonth }}</p>
                </div>
            </div>
        </section>

        <!-- Charts Section -->
        <section class="charts">
            <h2>Performance Overview</h2>
            <div class="chart">
                <datacards />
                <datacircles :stats="sponsorStats" @statUpdated="handleStatUpdate"/>
            </div>
        </section>

    </div>
</template>

<style scoped>
.dashboard {
    font-family: Arial, sans-serif;
    margin: 20px;
}

.dashboard-header {
    margin-bottom: 20px;
}

.metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.metric-card {
    flex: 1 1 20%;
    background: #f4f4f4;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.charts {
    margin-top: 20px;
}

.chart {
    height: 300px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
}

.role-specific {
    margin-top: 20px;
}

.admin-stats,
.sponsor-stats,
.influencer-stats {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

.admin-card,
.sponsor-card,
.influencer-card {
    background: #f4f4f4;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

progress {
    width: 100%;
    height: 20px;
}

strong {
    font-size: 1.5em;
    color: rgb(18, 215, 123);
}
h3{
    color: #06f0c9;
    text-align: center;
}
small {
    font-size: 0.5em;
    color: #00f1e5;
    text-align: center;
    text-overflow: ellipsis;
    display: block;
    white-space: nowrap;
    overflow: hidden;  
}
p{
    color: #000000;
    font-size:2em;
    text-align: center;
}
</style>
