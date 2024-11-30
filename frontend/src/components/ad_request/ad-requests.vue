<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

// Initialize ads as an empty array
const ads = ref([]);
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));


// Fetch ads from the backend
const fetchAds = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/ad_request', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });

        // Check if the response is okay
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const currentAds = await response.json();
        console.log('Current Ads:', currentAds);
        ads.value = currentAds;
    } catch (error) {
        console.error('Failed to fetch ads:', error);
    }
};

const revoke = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/ad_request/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        alert('Ad Revoked Successfully');
        const fetchedAds = await fetchAds();
    } catch (error) {
        console.error('Failed to revoke ad:', error);
    }
};

const negotiation = async (id, param) => {

    let params = {param};

    if (param === "negotiate") {
        const amount = prompt("Enter the Amount you want to negotiate");
        if (amount === null || amount.trim() === "") {
            alert("Please enter a valid amount.");
            return; // Exit if no amount is provided
        }

        params = { param, amount: parseFloat(amount) }; 
    } else if (param === "message") {
        const message = prompt("Enter your message");
        if (message === null || message.trim() === "") {
            alert("Please enter a valid message.");
            return; 
        }

        params = { param, message }; 
    } else{
        params = { param };
    }

    
    console.log(params);
    try {
            const response = await fetch(`http://127.0.0.1:5000/api/ad_request/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
            body: JSON.stringify(params),
            });
            if (response.ok) {
            alert(`${param} Request Sent Successfully`);
        }       
    } catch (error) {

        console.error(`Failed to ${param}:`, error);
    }
};
        


// Fetch ads when the component is mounted
onMounted(() => {
    fetchAds();
});
</script>

<template>
    <div>
        <h2>Ad Requests Status</h2>
        <!-- Display a message if no ads are available -->
        <div v-if="ads.length === 0">
            <p>No ads to display</p>
        </div>

        <!-- Iterate over the ads and display their information -->
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <th>Campaign_ID </th>
                        <th>Influencer_ID</th>
                        <th>Message</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th colspan="2" class="text-center"> Actions</th>

                    </tr>
                </thead>
                <!-- <tbody>
                    <tr v-for="ad in ads" :key="ad.ad_request_id">
                        <td>{{ ad.campaign_id }}</td>
                        <td>{{ ad.influencer_id }}</td>
                        <td>{{ ad.messages }}</td>
                        <td>{{ ad.payment_amount }}</td>
                        <td>{{ ad.status }}</td>
                        <div v-if="userDetails.role !== 'admin'">
                        <div v-if="userDetails.role === 'influencer'">
                            <div v-if="ad.status === 'Pending'">
                                <td>
                                    <button @click="negotiation(ad.ad_request_id, 'accept')">Accept</button>
                                    <button @click="negotiation(ad.ad_request_id, 'reject')">Reject</button>

                                </td>
                            
                                <td>
                                    <button @click="negotiation(ad.ad_request_id, 'message')"> Negotiate </button>
                                </td>
                            </div>
                        </div>
                            <div v-else>
                                <td>
                <button @click="revoke(ad.ad_request_id)" class="btn btn-warning">Revoke </button>
            </td>
            <td>
                <button @click="negotiation(ad.ad_request_id, 'negotiate')" class="btn btn-primary"> Negotiate </button>
            </td>
        </div>
    </div>
        </tr>
        </tbody> -->
                <tbody>
                    <tr v-for="ad in ads" :key="ad.ad_request_id">
                        <td>{{ ad.campaign_id }}</td>
                        <td>{{ ad.influencer_id }}</td>
                        <td>{{ ad.messages }}</td>
                        <td>{{ ad.payment_amount }}</td>
                        <td>{{ ad.status }}</td>

                        <!-- Conditional rendering for user roles -->
                        <td v-if="userDetails.role !== 'admin'">
                            <template v-if="userDetails.role === 'influencer'">
                                <template v-if="ad.status === 'Pending'">
                                    <button @click="negotiation(ad.ad_request_id, 'accept')">Accept</button>
                                    <button @click="negotiation(ad.ad_request_id, 'reject')">Reject</button>
                                </template>
                                <template v-else>
                                    <button @click="revoke(ad.ad_request_id)" class="btn btn-warning">Revoke</button>
                                    <button @click="negotiation(ad.ad_request_id, 'negotiate')"
                                        class="btn btn-primary">Negotiate</button>
                                </template>
                            </template>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
/* Style the ads for a cleaner look */
.ad-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #f9f9f9;
}

h3 {
    margin: 0;
}

p {
    margin: 5px 0;
}
</style>
