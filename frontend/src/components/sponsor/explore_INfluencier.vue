<script setup>
import influencer_Tables from '/src/components/sponsor/influencer_Table.vue'
import { ref, onMounted } from 'vue'

const influencers = ref([]);
const campaigns = ref([]);
const loading = ref(true); 
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const fetchInfluencers= async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/influencer', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        const data = await response.json();
        influencers.value = data;
    }
    catch (error) {
        console.error('Error:', error);
    } finally {
        loading.value = false; 
    }
};

const fetchCampaign = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/campaign', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        const data = await response.json();
        campaigns.value = data;
    }
    catch (error) {
        console.error('Error:', error);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchInfluencers();
    fetchCampaign();
   
});

</script>

<template>
    <div class="campaign-cards">
    <div v-if="loading" class="loading">Loading influencerss...</div>
    <div v-else-if="influencers.length === 0" class="no-influencers">No influencers found.</div>
    <div v-else>
        <influencer_Tables :inf_data="influencers" , :camp_data="campaigns">
        </influencer_Tables>
    </div>
    </div>

</template>

<style>
.info-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
}

.loading,
.no-influencers {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-top: 20px;
}
</style>
