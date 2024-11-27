<script setup>
import { ref, onMounted } from 'vue';

const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const authToken = localStorage.getItem('auth-token');

const props = defineProps({
    campaign_id: { type: Number, required: false, default: null },
});
const campaign_id = props.campaign_id ?? null;

const fetchCampaign = async () => {
    try {
    
        const response = await fetch(`http://127.0.0.1:5000/api/campaign?id=${campaign_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
            'userDetails': JSON.stringify(userDetails),
        },
    });
    const campaign = await response.json();
    console.log('Campaign:', campaign);
    return campaign;
} catch (error) {
    console.error('Failed to fetch campaign:', error);
}
};

const campaign = ref({});
onMounted(async () => {
    campaign.value = await fetchCampaign();
});

</script>
<template>
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Budget</th>
                <th>Category</th>
                <th>Niche</th>
                <th>Requirements</th>
                <th>Interested?</th> <!-- Will try to send email to sponsor -->
            </tr>
        </thead>
        <tbody>
            <tr v-for="c in campaign" :key="c.campaign_id">
                <td>{{ c.name }}</td>
                <td>{{ c.description }}</td>
                <td>{{ c.start_date }}</td>
                <td>{{ c.end_date }}</td>
                <td>{{ c.budget }}</td>
                <td>{{ c.category }}</td>
                <td>{{ c.niche }}</td>
                <td>{{ c.requirements }}</td>
                <td>
                    <button @click="sendRequest(c.id)" class="btn btn-success"><i
                            class="bi bi-hand-thumbs-up"></i></button>
                    <button class="btn btn-warning"><i
                        class="bi bi-hand-thumbs-down"></i></button>
                </td>
            </tr>
        </tbody>
    </table>

</template>

<style scoped>
</style>