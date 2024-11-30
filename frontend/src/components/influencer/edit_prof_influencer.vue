<script setup>
import { ref, onMounted } from 'vue';

// Retrieve user details from localStorage
const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const authToken = localStorage.getItem('auth-token');

// Define reactive variables for form fields
const user_id = userDetails.id;
const name = ref('');
const password = ref('');
const active = ref(true);
const category = ref('');
const niche = ref('');
const reach = ref('');
const socialLinks = ref({
    facebook: '',
    twitter: '',
    instagram: '',
    linkedin: '',
    youtube: '',
    tiktok: '',
});
const website = ref('');

// Fetch influencer data when the component is mounted
const fetchInfluencerData = async () => {
    try {
        console.log(user_id)
        const response = await fetch(`http://127.0.0.1:5000/fetch_edit_profile/${user_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': authToken,
                'userDetails': JSON.stringify(userDetails)
            },
        });

        if (response.ok) {
            const data = await response.json();
            // Populate the form fields with the fetched influencer data
            name.value = data.name || '';
            password.value = ''; // Don't pre-populate password for security reasons
            active.value = data.active || true;
            category.value = data.category || '';
            niche.value = data.niche || '';
            reach.value = data.reach || '';
            socialLinks.value = data.socialLinks || {
                facebook: '',
                twitter: '',
                instagram: '',
                linkedin: '',
                youtube: '',
                tiktok: '',
            };
            website.value = data.website || '';
        } else {
            console.error('Failed to fetch influencer data:', response.statusText);
        }
    } catch (error) {
        console.error('Failed to fetch influencer data:', error);
    }
};

// Call the function to fetch influencer data when the component is mounted
onMounted(() => {
    fetchInfluencerData();
});

// Function to handle form submission and update the profile
const editProfile = async () => {
    const influencerData = {
        name: name.value,
        password: password.value,
        active: active.value,
        category: category.value,
        niche: niche.value,
        reach: reach.value,
        socialLinks: { ...socialLinks.value },
        website: website.value,
    };

    try {
        const response = await fetch(`http://127.0.0.1:5000/editprofile/${user_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': authToken,
            },
            body: JSON.stringify(influencerData),
        });

        if (response.ok) {
            const data = await response.json();
            resetform();
            alert('Profile updated successfully');
        } else {
            console.error('Failed to update profile:', response.statusText);
        }
    } catch (error) {
        console.error('Failed to update profile:', error);
    }
};

const resetform = () => {
    name.value = '';
    password.value = '';
    active.value = true;
    category.value = '';
    niche.value = '';
    reach.value = '';
    socialLinks.value = {
        facebook: '',
        twitter: '',
        instagram: '',
        linkedin: '',
        youtube: '',
        tiktok: '',
    };
    website.value = '';
};

</script>
<template>
    <h2>Edit Profile</h2>
    <form @submit.prevent="editProfile">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="name" required>

        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required>

        <label for="active">Active</label>
        <input type="checkbox" id="active" v-model="active">

        <label for="category">Category</label>
        <input type="text" id="category" v-model="category" required>

        <label for="niche">Niche</label>
        <input type="text" id="niche" v-model="niche" required>

        <label for="reach">Reach</label>
        <input type="number" id="reach" v-model="reach" required>

        <label for="socialLinks">Social Links</label>
        <div class="social-links">
            <div>
                <i class="fab fa-facebook"></i>
                <input type="text" v-model="socialLinks.facebook" placeholder="Facebook">
            </div>
            <div>
                <i class="fab fa-twitter"></i>
                <input type="text" v-model="socialLinks.twitter" placeholder="Twitter">
            </div>
            <div>
                <i class="fab fa-instagram"></i>
                <input type="text" v-model="socialLinks.instagram" placeholder="Instagram">
            </div>
            <div>
                <i class="fab fa-linkedin"></i>
                <input type="text" v-model="socialLinks.linkedin" placeholder="LinkedIn">
            </div>
            <div>
                <i class="fab fa-youtube"></i>
                <input type="text" v-model="socialLinks.youtube" placeholder="YouTube">
            </div>
            <div>
                <i class="fab fa-tiktok"></i>
                <input type="text" v-model="socialLinks.tiktok" placeholder="TikTok">
            </div>
        </div>

        <label for="website">Website</label>
        <input type="text" id="website" v-model="website">

        <button type="submit">Save</button>
    </form>
</template>


<style scoped>

label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.social-links div {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.social-links i {
    margin-right: 10px;
    font-size: 1.5rem;
}

button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>
