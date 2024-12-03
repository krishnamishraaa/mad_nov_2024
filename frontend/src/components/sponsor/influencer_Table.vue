<script setup>
import { ref, computed } from 'vue';


const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const sentRequests = ref({}); 
const flaggedInfluencers = ref({});



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


const selectedCampaign = ref({});


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


const ad_Request = async (influencer_id, campaign_id) => {
    try {
        const message_input = prompt("Enter your message to the influencer:");
        if (!message_input) return; 

        const message = userDetails.name.split(' ')[0] + ": " + message_input;



        const payment = prompt("Enter the payment amount:");
        if (!payment || isNaN(payment)) return; 

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
    } catch (error) {
        console.error("Error sending ad request:", error);
        alert("Error sending the ad request.");
    }
};

const fetchSentRequests = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/ad_request', {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch existing ad requests: ${response.status}`);
        }

        const adRequests = await response.json();

        // Populate sentRequests object
        adRequests.forEach((request) => {
            const { influencer_id, campaign_id } = request;
            if (!sentRequests.value[influencer_id]) {
                sentRequests.value[influencer_id] = new Set();
            }
            sentRequests.value[influencer_id].add(campaign_id);
        });
    } catch (error) {
        console.error("Error fetching sent requests:", error);
    }
};


fetchSentRequests();


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

const flaggedinfluencers1 = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/flag'
        , {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': authToken,
            },
        });
        const data = await response.json();
        data.forEach((influencer) => {
            flaggedInfluencers.value[influencer.influencer_id] = true;
        });
    } catch (error) {
        console.error('Error fetching flagged influencers:', error);
    }
};

flaggedinfluencers1();

</script>

<template>
    <div>
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
                    <td>{{ item.name }} </td>
                    <td>{{ item.category }}</td>
                    <td>{{ item.niche }}</td>
                    <td>{{ item.reach }}</td>
                    <td>
                        <select v-model="selectedCampaign[item.influencer_id]">
                            <option value="" disabled Selected>Select a Campaign</option>
                            <option v-for="campaign in campData" :key="campaign.campaign_id"
                                :value="campaign.campaign_id">
                                {{ campaign.name }}
                            </option>
                        </select>
                        <button :disabled="!selectedCampaign[item.influencer_id] ||
                            (sentRequests[item.influencer_id]?.has(selectedCampaign[item.influencer_id]) ?? false)"
                            @click="ad_Request(item.influencer_id, selectedCampaign[item.influencer_id])">
                            Add
                        </button>
                    </td>
                    <td>
                        <button :disabled="flaggedInfluencers[item.influencer_id]"
                            @click="flagInfluencer(item.influencer_id)">Flag</button>
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
