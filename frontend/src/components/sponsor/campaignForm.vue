<script setup>
import { ref } from 'vue';

const name = ref('');
const description = ref('');
const start_date = ref('');
const end_date = ref('');
const budget = ref('');
const category = ref('');
const niche = ref('');
const visibility = ref('');
const goals = ref('');
const requirements = ref([]);
const isChecked = ref(false);
const campaigns = ref([]);
const s_c = ref(null); 
const selectedCampaign = ref(null); 

const handleCheckboxChange = () => {
    if (isChecked.value) {
        getSponsorCampaigns(); // Call the first function if checked
    } else {
        resetForm(); // Call the second function if unchecked
    }
};

const resetForm = () => {
    name.value = '';
    description.value = '';
    start_date.value = '';
    end_date.value = '';
    budget.value = '';
    category.value = '';
    niche.value = '';
    visibility.value = '';
    goals.value = '';
    requirements.value = [];
    s_c.value = null;
    selectedCampaign.value = null;
};

const submit_campaign = async () => {
    const campaignData = {
        name: name.value,
        description: description.value,
        start_date: start_date.value,
        end_date: end_date.value,
        budget: budget.value,
        category: category.value,
        niche: niche.value,
        visibility: visibility.value === 'True',
        goals: goals.value,
        status: "Active",
        requirements: requirements.value.toString(),
    };

    const url = selectedCampaign.value ? `http://127.0.0.1:5000/campaign/${selectedCampaign.value.campaign_id}` : 'http://127.0.0.1:5000/campaign';
    const method = selectedCampaign.value ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
                'userDetails': localStorage.getItem('userDetails'),
            },
            body: JSON.stringify(campaignData),
        });

        if (!response.ok) {
            const message = `An error has occurred: ${response.status}`;
            throw new Error(message);
        }

        alert('Campaign ' + (selectedCampaign.value ? 'Updated' : 'Created') + ' Successfully');
        resetForm();
    } catch (error) {
        console.error('Error:', error);
    }
};

const getSponsorCampaigns = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/campaign', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
                'userDetails': localStorage.getItem('userDetails'),
            },
        });
        if (!response.ok) {
            const message = `An error has occurred: ${response.status}`;
            throw new Error(message);
        }
        const data = await response.json();
        campaigns.value = data;
    } catch (error) {
        console.error('Error:', error);
    }
};

const loadCampaignData = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/campaign/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
                'userDetails': localStorage.getItem('userDetails'),
            },
        });
        if (!response.ok) {
            const message = `An error has occurred: ${response.status}`;
            throw new Error(message);
        }
        const data = await response.json();
        selectedCampaign.value = data;

        // Prepopulate the form with the campaign data
        name.value = data.name;
        description.value = data.description;
        start_date.value = data.start_date;
        end_date.value = data.end_date;
        budget.value = data.budget;
        category.value = data.category;
        niche.value = data.niche;
        visibility.value = data.visibility ? 'True' : 'False';
        goals.value = data.goals;
        requirements.value = data.requirements.split(',');
    } catch (error) {
        console.error('Error:', error);
    }
};

const editCampaign = (id) => {
    loadCampaignData(id);
};

const deleteCampaign = async (id) => {
    try {
        let confirmation = confirm('Are you sure you want to delete this campaign?');
        if (!confirmation) {
            return;
        }
        
        const response = await fetch(`http://127.0.0.1:5000/deletecampaign/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
                'userDetails': localStorage.getItem('userDetails'),
            },
        });
        if (!response.ok) {
            const message = `An error has occurred: ${response.status}`;
            throw new Error(message);
        }
        alert('Campaign Deleted Successfully');
        window.href="/sponsor";
        resetForm();
    } catch (error) {
        console.error('Error:', error);
    }
};
</script>

<template>
    <input type="checkbox" class="checkbox" v-model="isChecked" @change="handleCheckboxChange" />
    <label>Edit Campaign</label>

    <select v-if="isChecked" v-model="s_c" @change="editCampaign(s_c)">
        <option value="" disabled>Select a Campaign</option>
        <option v-for="campaign in campaigns" :key="campaign.campaign_id" :value="campaign.campaign_id">
            {{ campaign.name }}
        </option>
    </select>

    <form @submit.prevent="submit_campaign">
        <div class="row">
            <div class="col">
                <input type="text" v-model="name" class="form-control" placeholder="Campaign Name" />
            </div>
            <div class="col">
                <input type="text" v-model="description" class="form-control" placeholder="Campaign Description" />
            </div>
        </div>

        <div class="row">
            <div class="col">
                <input type="date" v-model="start_date" class="form-control" placeholder="Start Date" />
            </div>
            <div class="col">
                <input type="date" v-model="end_date" class="form-control" placeholder="End Date" />
            </div>
        </div>

        <div class="row">
            <div class="col">
                <input type="number" v-model="budget" class="form-control" placeholder="Budget" />
            </div>
            <div class="col">
                <label>Visibility</label>
                <div>
                    <input type="radio" id="visibility-true" class="radiobutton" value="True" v-model="visibility" />
                    <label for="visibility-true">    True</label>
                    <input type="radio" id="visibility-false" class="radiobutton" value="False" v-model="visibility" />
                    <label for="visibility-false">    False</label>
                </div>
            </div>
        </div>

        <div class="col">
            <label>Requirements</label>
            <input class="checkbox" type="checkbox" v-model="requirements" id="photo" value="photo" />
            <label for="photo">Photo</label>
            <input class="checkbox" type="checkbox" v-model="requirements" id="video" value="video" />
            <label for="video">Video</label>
            <input class="checkbox" type="checkbox" v-model="requirements" id="shorts" value="shorts" />
            <label for="shorts">Shorts</label>
            <input class="checkbox" type="checkbox" v-model="requirements" id="post" value="post" />
            <label for="post">Post</label>
        </div>

        <div class="row">
            <div class="col">
                <input type="text" v-model="category" class="form-control" placeholder="Category" />
            </div>
            <div class="col">
                <input type="text" v-model="niche" class="form-control" placeholder="Niche" />
            </div>
        </div>

        <div class="row">
            <div class="col">
                <input type="text" v-model="goals" class="form-control" placeholder="Goals" />
            </div>
        </div>

        <button type="submit" class="btn btn-success">
            {{ selectedCampaign ? 'Update' : 'Create' }} Campaign
        </button>

        <buttton v-if="selectedCampaign" @click="deleteCampaign(selectedCampaign.campaign_id)" class="btn btn-danger rightbutton">
            Delete Campaign
        </buttton>
    </form>
</template>

<style scoped>

form {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    max-width: 600px;
    margin: 5px 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


.row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 15px;
}


input.form-control,
select.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

input.form-control:focus,
select.form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}


select.form-control {
    background-color: white;
    appearance: none;
    cursor: pointer;
}

.radiobutton{
    transform: scale(1.5);
    margin-right: 10px;
    margin-left: 10px;
}


button.btn {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button.btn-success {
    background-color: #28a745;
    color: white;
}

button.btn-success:hover {
    background-color: #218838;
}


h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
    font-weight: bold;
}

.checkbox {
    display: inline;
    size: big;
    margin-left: 20px;
    margin-right: 10px;
    transform: scale(1.5);
}
.rightbutton{
    float: right;
}
</style>
