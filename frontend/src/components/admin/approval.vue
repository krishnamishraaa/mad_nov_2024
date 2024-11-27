<script setup>
import { ref, onMounted, defineEmits } from 'vue';

const emit = defineEmits('sponsorCountUpdated');

const sponsors = ref([]); // Holds the sponsors data

const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const fetchSponsors = async (action) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/sponsors?action=${action}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',  
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
        },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        sponsors.value = data; // Store the fetched sponsors data
        emit('sponsorCountUpdated', sponsors.value.length);

    } catch (error) {
        console.error(`Error fetching sponsors:`, error);
    }
};


const approveSponsor = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/sponsors/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
        },
        });
        if (response.ok) {
            // Remove approved sponsor from the list
            sponsors.value = sponsors.value.filter((sponsor) => sponsor.sponsor_id !== id);
        }
    } catch (error) {
        console.error(`Error approving sponsor ${id}:`, error);
    }
};

const rejectSponsor = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/sponsors/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });
        if (response.ok) {
            // Remove rejected sponsor from the list
            sponsors.value = sponsors.value.filter((sponsor) => sponsor.sponsor_id !== id);
        }
    } catch (error) {
        console.error(`Error rejecting sponsor ${id}:`, error);
    }
};

// Fetch data on component mount
onMounted(async () => {
    await fetchSponsors('unapproved');
    console.log('Sponsors:', sponsors.value);
});
</script>

<template>
    <div>
        <!-- Table of unapproved sponsors -->
        <h3>Pending Sponsors</h3>
        <div v-if="sponsors.length === 0">No pending sponsors at the moment.
        </div>
        <div v-else>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Industry</th>
                        <th>Budget</th>
                        <th>Website</th>
                        <th>Notes</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="sponsor in sponsors" :key="sponsors.sponsor_id">
                        <td>{{ sponsor.name }}</td>
                        <td>{{ sponsor.industry }}</td>
                        <td>{{ sponsor.budget }}</td>
                        <td><a :href="sponsor.company_website" target="_blank">{{ sponsor.company_website }}</a></td>
                        <td>{{ sponsor.notes }}</td>
                        <td>
                            <button @click="approveSponsor(sponsor.sponsor_id)" class="btn btn-success">Approve</button>
                            <button @click="rejectSponsor(sponsor.sponsor_id)" class="btn btn-danger">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th,
td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
}

th {
    background-color: #f4f4f4;
}

button {
    margin-right: 10px;
    padding: 5px 10px;
    cursor: pointer;
}

button:hover {
    background-color: #f0f0f0;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>
