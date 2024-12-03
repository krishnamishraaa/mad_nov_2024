<script setup>
import { ref, computed, onMounted } from 'vue';
import filtered_table from '/src/components/sponsor/influencer_Table.vue';
import search_Filter from '/src/components/common/searchFilters.vue';


const allinfluencers = ref([]); // Full influencer list
const campaigns = ref([]); // Full campaign list
const filters = ref({
    category: '',
    niche: '',
    reach: 50000, // Default minimum reach
});

const updateFilters = (newFilters) => {
    filters.value = newFilters;
};

const loading = ref(true);

const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));


const filteredInfluencers = computed(() => {
    return allinfluencers.value.filter((influencer) => {
        return(
        influencer.category.toLowerCase().includes(filters.value.category.toLowerCase()) &&
        influencer.niche.toLowerCase().includes(filters.value.niche.toLowerCase()) &&
        influencer.reach >= filters.value.reach
        );
    });
});

// Fetch influencers
const fetchInfluencers = async () => {
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
        allinfluencers.value = data;
    } catch (error) {
        console.error('Error fetching influencers:', error);
    } finally {
        loading.value = false;
    }
};

// Fetch campaigns
const fetchCampaigns = async () => {
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
    } catch (error) {
        console.error('Error fetching campaigns:', error);
    }
};

// Fetch data on mount
onMounted(async () => {
    await fetchInfluencers();
    await fetchCampaigns();
});


</script>

<template>
    <div class="campaign-cards">
        <div v-if="loading" class="loading">Loading influencers...</div>
        <div v-else-if="!allinfluencers || allinfluencers.length === 0" class="no-influencers">No influencers found.
        </div>
        <div v-else>

            <!-- Influencer Table Component -->
            <influencer_Tables v-if=" allinfluencers && campaigns" :inflData="filteredInfluencers"
            :campData="campaigns" :filters="filters" />
            <search_Filter :filters="filters" @updateFilters="updateFilters" />
            <filtered_table :inflData="filteredInfluencers" :filters="filters" :campData="campaigns" />

        </div>
    </div>
</template>

<style scoped>
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
