<script setup>
import { ref, onMounted} from 'vue';
import datacircles from '/src/components/common/data_circles.vue';

const emit = defineEmits(['totalInfluencers', 'totalCampaigns']);

const stats_data = ref({});

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
        emit('totalInfluencers', stats_data.value.totalInfluencers);
        emit('totalCampaigns', stats_data.value.totalCampaigns);
    }
    catch (error) {
        console.error('Error:', error);
    }
};
onMounted(() => {
    fetchStatistics();
});



</script>

<template>

    <!-- stats_data: {{ stats_data }} -->

    <h2> Total Reach : {{ stats_data.totalReach }}</h2>
    <p>
        Active Users: {{ stats_data.users }}

    </p>
    <p>
        datacircles: <datacircles />
        <datacircles />
    </p>
    <p>
        Active Influencers: {{ stats_data.influencers }}
    </p>
    <p>
        Active Sponsors: {{ stats_data.sponsors }}
    </p>
    <p>
        Active Campaigns: {{ stats_data.campaigns }}
    </p>

    <p>
        Total Ad Requests: {{ stats_data.ad_requests }}

    </p>

    <p>
        Pending Ad Requests: {{ stats_data.pendingAdRequests }}
    </p>
    <p>
        Total Budget: {{ stats_data.totalBudget }}
    </p>


</template>

<style scoped>

</style>