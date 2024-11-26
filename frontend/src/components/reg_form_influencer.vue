<script setup>
import { ref, reactive } from 'vue';

const props = defineProps({
    email: { type: String, required: true },
    name: { type: String, required: true },
    role: { type: String, required: true },
    password: { type: String, required: true },
});

// State for user and influencer data
const user = reactive({
    name: props.name,
    password: props.password,
    active: true,
    role: props.role,
    email: props.email,
});

const influencer = reactive({
    category: '',
    niche: '',
    reach: '',
    socialLinks: {
        facebook: '',
        twitter: '',
        instagram: '',
        linkedin: '',
        youtube: '',
        tiktok: '',
    },
    website: '',
});

var userId = ref(null);
const loading = ref(false); // Track loading state

// Function to create a user
const createUser = async () => {
    console.log('Creating user:', user);
    if (user.email && user.role) {
        loading.value = true; // Set loading to true during the request
        try {
            const response = await fetch("http://127.0.0.1:5000/api/user", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user.email,
                    name: user.name,
                    password: user.password,
                    role: user.role,
                    active: true,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('User created:', data);

                if (data) {
                    userId = data.userId; // Store the userId
                    alert(`User created successfully! Your ID is: ${userId}`);
                    console.log('ye hai User ID:', userId);
                } else {
                    alert('User creation failed');
                }
                
                // console.log('User created:', userId.value);
            } else {
                alert('User creation failed');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            loading.value = false; // Set loading to false when done
        }
    }
};

// Function to handle influencer form submission
const handleSubmit = async () => {
    if (!user.name || !user.password || !influencer.category) {
        alert('Please fill in all required fields.');
        return;
    }

    await createUser(); // Create user first

    if (userId) {
        const formData = {
            user_id: userId,
            email: user.email,
            name: user.name,
            password: user.password,
            active: user.active,
            category: influencer.category,
            niche: influencer.niche,
            reach: influencer.reach,
            socialLinks: { ...influencer.socialLinks },
            website: influencer.website,
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/api/influencer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Error saving influencer data');
            }
            const data = await response.json();
            alert('Influencer data saved successfully!');
            // redirects to signin page
            window.location.href = '/signin';
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to save influencer data.');
            window.location.reload();
        }

    } else {
        alert('User creation failed. Cannot save influencer data.');
    }
};
</script>

<template>
    <div class="form-container">
        <h2>Create Influencer</h2>
        <form @submit.prevent="handleSubmit">
            <!-- User Fields -->
            <div>
                <label for="name">Full Name *</label>
                <input v-model="user.name" type="text" id="name" required />
            </div>

            <div>
                <label for="password">Password *</label>
                <input v-model="user.password" type="password" id="password" required />
            </div>

            <!-- Influencer Fields -->
            <div>
                <label for="category">Category *</label>
                <input v-model="influencer.category" type="text" id="category" required />
            </div>

            <div>
                <label for="niche">Niche</label>
                <input v-model="influencer.niche" type="text" id="niche" />
            </div>

            <div>
                <label for="reach">Total Reach</label>
                <input v-model="influencer.reach" type="number" id="reach" min="3" required />
            </div>

            <!-- Social Links -->
            <div class="social-links">
                <div>
                    <label for="facebook">Facebook</label>
                    <input v-model="influencer.socialLinks.facebook" type="url" id="facebook" />
                </div>
                <div>
                    <label for="twitter">Twitter</label>
                    <input v-model="influencer.socialLinks.twitter" type="url" id="twitter" />
                </div>
                <div>
                    <i class="bi bi-instagram"></i>
                    <label for="instagram">Instagram</label>
                    <input v-model="influencer.socialLinks.instagram" type="url" id="instagram" />
                </div>
                <div>
                    <i class="bi bi-linkedin"></i>
                    <label for="linkedin">LinkedIn</label>
                    <input v-model="influencer.socialLinks.linkedin" type="url" id="linkedin" />
                </div>
                <div>
                    <i class="bi bi-youtube"></i>
                    <label for="youtube">YouTube</label>
                    <input v-model="influencer.socialLinks.youtube" type="url" id="youtube" />
                </div>
                <div>
                    <i class="bi bi-tiktok"></i>
                    <label for="tiktok">TikTok</label>
                    <input v-model="influencer.socialLinks.tiktok" type="url" id="tiktok" />
                </div>
            </div>

            <div>
                <label for="website">Website</label>
                <input v-model="influencer.website" type="url" id="website" />
            </div>

            <button type="submit" :disabled="loading">
                <span v-if="loading">Creating...</span>
                <span v-else>Submit</span>
            </button>
        </form>
    </div>
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
