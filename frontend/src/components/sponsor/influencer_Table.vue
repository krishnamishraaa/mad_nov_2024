<script setup>
import { defineProps, ref, computed } from 'vue';

const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const props = defineProps({
    inf_data: {
        type: Array,
        required: true,
    },
    camp_data: {
        type: Array,
        required: true,
    }
});

const category_search = ref('');
const niche_search = ref('');
const reach_search = ref(''); 
const selectedCampaign = ref({});


// Filter the data from props based on user input
const filteredData = computed(() =>
    props.inf_data.filter((item) => {
        const matchesCategory =
            !category_search.value ||
            item.category.toLowerCase().includes(category_search.value.toLowerCase());
        const matchesNiche =
            !niche_search.value ||
            item.niche.toLowerCase().includes(niche_search.value.toLowerCase());
        const matchesReach = parseInt(item.reach, 10) >= reach_search.value;

        return matchesCategory && matchesNiche && matchesReach;
    })
);

const ad_Request = async (influencer_id, campaign_id) => {
    const message = prompt('Enter a message for the influencer');
    const payment = prompt('Enter the payment amount');

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/ad_request/${campaign_id}/${influencer_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':`Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
            body: JSON.stringify({
                "message": message,
                "requirements": {
                    "post": post,
                    "story": story,
                    "video": video,
                    "image": image,
                },
                "payment": payment,
                "status": "Pending",

            })
        });
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
};
           
</script>

<template>
    <form>
        <label for="category_search">Category</label>
        <input type="text" id="category_search" v-model="category_search" placeholder="Search by Category" />

        <label for="niche_search">Niche</label>
        <input type="text" id="niche_search" v-model="niche_search" placeholder="Search by Niche" />

        <label for="reach_search">Reach</label>
        <input type="range" id="reach_search" v-model="reach_search" min="50000" max="1000000" />


    </form>

    <div>
        <h3>Filtered Results</h3>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Niche</th>
                    <th>Reach <small>(Minimum:{{ reach_search }})</small></th>
                    <th>Add to Campaign</th>
                    <th>Flag</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in filteredData" :key="index">
                    <a :href="'/influencer/' + item.influencer_id">
                        <td>{{ item.name }}</td>
                    </a>
                    <td>{{ item.category }}</td>
                    <td>{{ item.niche }}</td>
                    <td>{{ item.reach }}</td>
                    <td>
                        <select v-model="selectedCampaign[item.influencer_id]">
                            <option value="" disabled>Select a Campaign</option>
                            <option v-for="campaign in props.camp_data" :key="campaign.campaign_id"
                                :value="campaign.campaign_id">
                                {{ campaign.name }}
                            </option>
                        </select>
    
                        <button :disabled="!selectedCampaign[item.influencer_id]"
                            @click="ad_Request(item.influencer_id, selectedCampaign[item.influencer_id])">
                            Add
                        </button>
                    </td>
                    <td>
                        <button @click="flagInfluencer(item.influencer_id)">Flag</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background-color: #f2f2f2;
    padding: 10px;
    text-align: left;
}

td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #f2f2f2;
}

tr:hover {
    background-color: #f9f9f9;
}
input{
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 5px;
}
</style>
