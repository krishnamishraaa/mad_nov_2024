<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
console.log(route.params);
const id = route.params.id;

const influencer = ref({});
const stats = ref({});
const loading = ref(true);
const error = ref(null);

const fetchInfluencerDetails = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/profilepage?id=${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        influencer.value = data.influnecer_details || {};
        console.log(data);
        stats.value = data.stats || {};
    } catch (err) {
        error.value = err.message;
        console.error('Failed to fetch influencer details:', err);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchInfluencerDetails();
});
</script>

<template>
    <div class="profile-page">
        <div class="profile-header">
            <h2>{{ influencer.name }}</h2>
            <p>{{ influencer.category }} - {{ influencer.niche }}</p>
        </div>
        <div class="profile-content">
            <div class="profile-details">
                <h3>Details</h3>
                <p><strong>Reach:</strong> {{ influencer.reach }}</p>
                <p><strong>Website:</strong> <a :href="influencer.website">{{ influencer.website }}</a></p>
                <h3>Social Links</h3>
                <!-- <ul>
                    <li v-if="influencer.socialLinks.facebook">
                        <i class="fab fa-facebook"></i>
                        <a :href="influencer.socialLinks.facebook">{{ influencer.socialLinks.facebook }}</a>
                    </li>
                    <li v-if="influencer.socialLinks.twitter">
                        <i class="fab fa-twitter"></i>
                        <a :href="influencer.socialLinks.twitter">{{ influencer.socialLinks.twitter }}</a>
                    </li>
                    <li v-if="influencer.socialLinks.instagram">
                        <i class="fab fa-instagram"></i>
                        <a :href="influencer.socialLinks.instagram">{{ influencer.socialLinks.instagram }}</a>
                    </li>
                    <li v-if="influencer.socialLinks.linkedin">
                        <i class="fab fa-linkedin"></i>
                        <a :href="influencer.socialLinks.linkedin">{{ influencer.socialLinks.linkedin }}</a>
                    </li>
                    <li v-if="influencer.socialLinks.youtube">
                        <i class="fab fa-youtube"></i>
                        <a :href="influencer.socialLinks.youtube">{{ influencer.socialLinks.youtube }}</a>
                    </li>
                    <li v-if="influencer.socialLinks.tiktok">
                        <i class="fab fa-tiktok"></i>
                        <a :href="influencer.socialLinks.tiktok">{{ influencer.socialLinks.tiktok }}</a>
                    </li>
                </ul> -->
            </div>
            <div class="profile-stats">
                <h3>Statistics</h3>
                <p><strong>Ad Requests:</strong> {{ stats.adRequests }}</p>
                <p><strong>Completed Ads:</strong> {{ stats.completedAds }}</p>
                <p><strong>Revenue:</strong> {{ stats.revenue }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.profile-page {
    margin: 20px;
}


</style>