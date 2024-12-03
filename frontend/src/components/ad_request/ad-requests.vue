<script setup>
import { ref, watch, onMounted } from 'vue';

// Initialize ads as an empty array
const ads = ref([]);
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const filter = ref('all')


const fetchAds = async () => {
    try {
        let params = new URLSearchParams({
            filter: filter.value,
        });
        const response = await fetch(`http://127.0.0.1:5000/api/ad_request?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });

    
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const currentAds = await response.json();
        ads.value = currentAds.map(ad => {
            try {
                ad.messages = JSON.parse(ad.messages);
            } catch {
                ad.messages = ad.messages ? [ad.messages] : [];
            }
            return ad;
        });

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
        if (amount === null || amount.trim() === "" || isNaN(amount) || parseFloat(amount) < 0) {
            alert("Please enter a valid amount.");
            return; 
        }

        params = { param, amount: parseFloat(amount) }; 
    } else if (param === "message") {
        const message_input = prompt("Enter your message");
        if (message_input  === null || message_input.trim() === "") {
            alert("Please enter a valid message.");
            return; 
        }
        const message = userDetails.name.split(' ')[0] + ": " + message_input;
        
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
        



onMounted(() => {
    fetchAds();
});
watch(filter, fetchAds);
</script>

<template>
    <div>
        <div class="searchBar">

        <h2>Ad Requests Status</h2>
        
        <select v-model="filter">
            <option value="all" selected>All</option>
            <option value="pending">Pending</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
        </select>
   
        </div>
      
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
                        <th v-if="userDetails.role !== 'admin'">Message</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th v-if="userDetails.role !== 'admin'" colspan=" 2" class="text-center"> Actions</th>

                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in ads" :key="ad.ad_request_id">
                        <td>{{ ad.campaign_id }}</td>
                        <td>{{ ad.influencer_id }}</td>
                        <td v-if="userDetails.role !== 'admin'">
                                <p v-for="(msg, index) in ad.messages.slice(-3)" :key="index">
                {{ msg }}
                                </p>
                        </td>
                        <td>{{ ad.payment_amount }}</td>
                        <td>{{ ad.status }}</td>

                        <!-- Conditional rendering for user roles -->
                        <td v-if=" userDetails.role !=='admin'">
                            <template v-if=" userDetails.role==='influencer' ">
                                <template v-if=" ad.status==='Pending'">
                                    <div class=" buttns">

                                        <button class="btn btn-success" @click="negotiation(ad.ad_request_id, 'accept')"
                                            title="Accept"><i class="bi bi-hand-thumbs-up"></i></button>

                                        <button @click="negotiation(ad.ad_request_id, 'message')" title="Negotiate"
                                            class="btn btn-primary"><i class="bi bi-chat-left-quote-fill"></i></button>

                                        <button class="btn btn-danger" @click="negotiation(ad.ad_request_id, 'reject')"
                                            title="Reject"><i class="bi bi-hand-thumbs-down"></i></button>
                                    </div>
                                </template>
                                <template v-else ="ad.status === 'Accepted' ">
                                        <div class="buttns">
                                            <button > <i class="bi bi-file-earmark-pdf-fill"></i>Sign</button>
                                            <button disabled > <i class="bi bi-cash-coin"> Pending</i> </button>
                                        </div>
                                    </template>
                            </template>

                            <template v-if="userDetails.role === 'sponsor' ">
                                <template v-if="ad.status === 'Pending' ">
                                    <div class="buttns">
                                        <button @click="revoke(ad.ad_request_id)" class="btn btn-warning"
                                            title="Revoke"><i class="bi bi-trash3"></i></button>
                                        <button @click="negotiation(ad.ad_request_id, 'negotiate')"
                                            class="btn btn-primary" title="Negotiate"><i
                                                class="bi bi-currency-rupee"></i></button>
                                    </div>
                                </template>
                                <template v-else ="ad.status === 'Accepted' ">
                                        <div class="buttns">
                                            <button disabled> <i class="bi bi-file-earmark-pdf-fill"></i> Contract</button>
                                            <button disabled> <i class="bi bi-cash-coin"></i> Remit </button>
                                        </div>
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
.buttns {
   display: inline-block;
   display: flex;
    gap: 10px;
    justify-content: center;
}
.searchBar{
    display: flex;
    gap: 10px;
    margin: 10px;
    justify-content: space-between;
    margin-right:10px;
    padding: 10px;
}

</style>
