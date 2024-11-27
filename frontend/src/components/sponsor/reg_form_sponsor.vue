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

const sponsor = reactive({
    industry: '',
    budget: '',
    company_website: '',
    notes: '',
    
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
    if (!user.name || !user.password || !sponsor.industry) {
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
            industry: sponsor.industry,
            budget: sponsor.budget,
            approved:false,
            company_website: sponsor.company_website,
            notes: sponsor.notes
            
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/api/sponsors', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Error saving influencer data');
            }
            const data = await response.json();
            alert('Sponsor data saved successfully!');
            // redirects to signin page
            window.location.href = '/signin';
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to save Sponsor data.');
            window.location.reload();
        }

    } else {
        alert('User creation failed. Cannot save Sponsor data.');
    }
};
</script>

<template>
    <div class="form-container">
        <h2>Create Sponsor</h2>
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
                <label for="category">Industry *</label>
                <input v-model="sponsor.industry" type="text" id="category" required />
            </div>

            <div>
                <label for="niche">Budget</label>
                <input v-model="sponsor.budget" type="number" id="budget" />
            </div>

            <div>
                <label for="reach">Company Website</label>
                <input v-model="sponsor.company_website" type="text" id="reach" />
            </div>
            <div>
                <label for="notes">Notes to Admin (Helps is faster approval)</label>
                <input v-model="sponsor.notes" type="text" id="notes" />
            </div>



            <button type="submit" :disabled="loading">
                <span v-if="loading">Creating...</span>
                <span v-else>Submit</span>
            </button>
        </form>
        <button href="/signin" class="btn btn-danger">
            Cancel & Go Back
        </button>
    </div>
</template>

<style scoped>
/* .form-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
} */

/* form div {
    margin-bottom: 15px;
} */

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
