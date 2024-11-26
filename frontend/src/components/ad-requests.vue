<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

// Initialize ads as an empty array
const ads = ref([]);
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

computed(() => {
    // take a field from ADs, which has been json.dumped. make it jsom object
    ads.value.forEach(ad => {
        ad.requirements = JSON.parse(ad.requirements);
    });
    // now select values in requirement which are true & discard false
    ads.value.forEach(ad => {
        ad.requirements = Object.entries(ad.requirements).filter(([key, value]) => value).map(([key, value]) => key);
    });

    // now join the values in requirements with a comma
    ads.value.forEach(ad => {
        ad.requirements = ad.requirements.join(', ');
    });

    return ads;

});

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
                        <th>Requirements</th>
                        <th>Payment Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad in ads" :key="ad.id">
                        <td>{{ ad.campaign_id }}</td>
                        <td>{{ ad.influencer_id }}</td>
                        <td>{{ ad.messages }}</td>
                        <td>{{ ad.requirements.slice(',')}}</td>
                        <td>{{ ad.payment_amount }}</td>
                        <td>{{ ad.status }}</td>
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
