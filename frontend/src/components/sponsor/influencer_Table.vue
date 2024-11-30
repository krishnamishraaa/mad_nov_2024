<script setup>
import { ref, computed } from 'vue';

// Retrieve auth token and user details
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

// Props for influencers, campaigns, and filters
const props = defineProps({
    inflData: {
        type: Array,
        required: true,
        default: () => [],
    },
    campData: {
        type: Array,
        required: true,
    },
    filters: {
        type: Object,
        required: true,
        default: () => ({}),
    },
});

// State to track selected campaign for each influencer
const selectedCampaign = ref({});

// Filtered influencers based on the provided filters
const filteredData = computed(() => {
    return props.inflData.filter((item) => {
        const matchesCategory = !props.filters.category ||
            item.category?.toLowerCase().includes(props.filters.category.toLowerCase());
        const matchesNiche = !props.filters.niche ||
            item.niche?.toLowerCase().includes(props.filters.niche.toLowerCase());
        const matchesReach = !props.filters.reach || parseInt(item.reach, 10) >= props.filters.reach;

        return matchesCategory && matchesNiche && matchesReach;
    });
});

// Send ad request to a campaign
const ad_Request = async (influencer_id, campaign_id) => {
    try {
        const message = prompt("Enter your message to the influencer:");
        if (!message) return; // Exit if no message

        const payment = prompt("Enter the payment amount:");
        if (!payment || isNaN(payment)) return; // Validate payment input

        const response = await fetch(`http://127.0.0.1:5000/api/ad_request/${campaign_id}/${influencer_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
            body: JSON.stringify({
                campaign_id,
                influencer_id,
                messages: message,
                payment_amount: payment,
            }),
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        alert("Ad request sent successfully!");
        console.log(data);
    } catch (error) {
        console.error("Error sending ad request:", error);
        alert("Error sending the ad request.");
    }
};

// Flag an influencer with a reason
const flagInfluencer = async (influencer_id) => {
    try {
        const reason = prompt("Enter the reason for flagging the influencer:");
        if (!reason) return; // Exit if no reason

        const response = await fetch("http://127.0.0.1:5000/flag/post", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': authToken,
            },
            body: JSON.stringify({
                influencer_id,
                reason,
            }),
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        alert("Influencer flagged successfully!");
        console.log(await response.json());
    } catch (error) {
        console.error("Error flagging influencer:", error);
        alert("Error flagging the influencer.");
    }
};
</script>

<template>
    <div>
        <h3>Filtered Results</h3>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Niche</th>
                    <th>Reach <small>(Minimum: {{ filters.reach }})</small></th>
                    <th>Add to Campaign</th>
                    <th>Flag</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in filteredData" :key="item.influencer_id">
                    <td>
                        <a :href="'/influencer/' + item.influencer_id">{{ item.name }}</a>
                    </td>
                    <td>{{ item.category }}</td>
                    <td>{{ item.niche }}</td>
                    <td>{{ item.reach }}</td>
                    <td>
                        <select v-model="selectedCampaign[item.influencer_id]">
                            <option value="" disabled>Select a Campaign</option>
                            <option v-for="campaign in campData" :key="campaign.campaign_id"
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
</style>
