<script setup>
import { ref, onMounted } from 'vue';

const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const authToken = localStorage.getItem('auth-token');

const filters = ref({
    category: "",
    niche: "",
    budget: "",
    requirement: "",
});

const props = defineProps({
    campaign_id: { type: Number, required: false, default: null },
});
const campaign_id = props.campaign_id ?? null;


const sendRequest = async (id) => {
    try {
        
        const response = await fetch(`http://127.0.0.1:5000/api/request_campaign/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
            body: JSON.stringify({"interested_influencers":{ "influencer_id": userDetails.id }}),
        });
        if (response.ok) {
            alert('Interest sent successfully');
        } else {
            alert('Failed to send request');
        }
    } catch (error) {
        console.error('Failed to send request:', error);
    }
};

// Reactive variable to store campaigns
const campaigns = ref({});

// Fetch campaigns with filters applied
const fetchFilteredCampaigns = async () => {
    try {
        // Build query parameters from filters
        const params = new URLSearchParams({
            category: filters.value.category || "",
            niche: filters.value.niche || "",
            budget: filters.value.budget || "",
            requirement: filters.value.requirement || "",
        });

        const response = await fetch(`http://127.0.0.1:5000/api/campaign_filter?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch campaigns.");

        const data = await response.json();
        campaigns.value = data.campaigns;
    } catch (error) {
        console.error(error.message);
    }
};
onMounted(async () => {

fetchFilteredCampaigns();
});

</script>
<template>
    <div class="searchBar">
        <h6>Filter based on: </h6>
        <input v-model="filters.category" type="text" placeholder="Category" @input="fetchFilteredCampaigns" />
        <input v-model="filters.budget" type="number" placeholder="Minimum Budget" @input="fetchFilteredCampaigns" />
        <input v-model="filters.niche" type="text" placeholder="Niche" @input="fetchFilteredCampaigns" />
        <select v-model="filters.requirement" @input="fetchFilteredCampaigns">
            <option disabled selected value="">Requirements</option>
            <option value="photo">Photo</option>
            <option value="video">Video</option>
            <option value="short">Short</option>
            <option value="post">POST</option>
        </select>
        <!-- <button @click="fetchFilteredCampaigns"><i class="bi bi-search"></i></button> -->
        <!-- <button ><i class="bi bi-search"></i></button> -->
    </div>
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th colspan="2">Description</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Budget</th>
                <th>Category</th>
                <th>Niche</th>
                <th>Requirements</th>
                <th>Interested?</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="campaign in campaigns" :key="campaign.campaign_id">
                <td>{{ campaign.name }}</td>
                <td colspan="2">{{ campaign.description }}</td>
                <td>{{ new Date(campaign.start_date).toLocaleDateString() }}</td>
                <td>{{ new Date(campaign.end_date).toLocaleDateString() }}</td>
                <td>{{ campaign.budget }}</td>
                <td>{{ campaign.category }}</td>
                <td>{{ campaign.niche }}</td>
                <td>{{ campaign.requirements }}</td>
                <td>
                    <button @click="sendRequest(campaign.campaign_id)" class="btn btn-success"><i
                            class="bi bi-hand-thumbs-up"></i></button>
                    <button class="btn btn-warning"><i class="bi bi-flag"></i></button>
                </td>
            </tr>
        </tbody>
    </table>

</template>

<style scoped>
.longMsg {
    text-align: center;
    text-wrap: ellipsis;
}
.searchBar {
    display: flex;
    gap: 10px;
    margin: 10px;
    background-color: rgb(232, 238, 244);
    margin-right:10px;
    padding: 10px;
}
h6{
    text-align: center;
    font-size: 1em;
    margin-top: 5px;

}
input{
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #ddd;
    flex-wrap: nowrap;
    height: 0%;
}
select{
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #ddd;
    height: 32px;
}
</style>
