<script setup>
import { onMounted, ref } from 'vue';

const flagged_data = ref({});

const flagged_func = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/flag', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
            },
        });
       if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }	
        
        return await response.json();
    }
    catch (error) {
        console.error('Error:', error);
    }
};

const deactivateUser = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/deactivateuser/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
            },
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        console.log('User deactivated');
        flagged_data.value = await flagged_func();
        resetFlag(id);
    }
    catch (error) {
        console.error('Error:', error);
    }
};

const resetFlag = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/resetflag/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth-token'),
            },
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        flagged_data.value = await flagged_func();
    }
    catch (error) {
        console.error('Error:', error);
    }
};



onMounted( async () => {
    flagged_data.value = await flagged_func();
});


</script>
<template>
    <div>
        <h1>Flagged Posts</h1>
        <table class="table">
            <thead>
            <tr>
                <th>FLAG ID</th>
                <th>SPONSOR ID</th>
                <th>INFLUENCER ID</th>
                <th>REASON</th>
                <th colspan="2">Take Action</th>
            </tr>
            </thead>
            <tr v-for="flag in flagged_data">
                <td>{{ flag.flag_id }}</td>
                <td>{{ flag.sponsor_id }}</td>
                <td>{{ flag.influencer_id }}</td>
                <td class="longMsg">{{ flag.reason }}</td>
                <td><button class="btn btn-success" @click="resetFlag(flag.flag_id)" >Reset Flag</button></td>
                <td><button class="btn btn-danger" @click="deactivateUser(flag.influencer_id)">Deactivate</button></td>
            </tr>
        </table>
    </div>

    
</template>
<style scoped>

.longMsg {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
};
</style>

