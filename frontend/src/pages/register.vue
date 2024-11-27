<script setup>
import InfluencerForm from '../components/influencer/reg_form_influencer.vue';
import SponsorForm from '../components/sponsor/reg_form_sponsor.vue';
import { ref, computed } from 'vue';

const email_valid = ref(false);
const role = ref('');
const email = ref('');
const errorMessage = ref('');
const userId = ref(null);  // New reactive variable to store user_id

// Computed property to validate email format
const isEmailValid = computed(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email.value);
});

// Check if email is valid and doesn't already exist
const checkEmail = async () => {
    try {
        console.log('Checking email:', email.value);

        const response = await fetch(`http://127.0.0.1:5000/api/user?email=${email.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            email_valid.value = false;
            errorMessage.value = 'Email Already Exists.... Please Login or register with a different email';
        } else {
            email_valid.value = true;
            errorMessage.value = '';
        }
    } catch (error) {
        console.error('Error:', error);
        errorMessage.value = 'An error occurred while checking the email. Please try again.';
    }
};
const refresh = () => {
    email.value = '';
    email_valid.value = false;
    role.value = '';
    errorMessage.value = '';
    userId.value = null;
};

</script>

<template>
    <h1>Register</h1>
    <form @submit.prevent="submitData">
        <!-- Email Input -->
        <label for="email">Email</label>
        <input v-model="email" type="email" id="email" name="email" required
            :class="{ active: errorMessage, valid: email_valid }" />

        <!-- Check Email Button -->
        <button type="button" @click="checkEmail" :disabled="!isEmailValid">Check Email</button>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
            <!-- calling refresh function -->
            Go to <button class="rpb" type="button" href="/signin">Log IN</button>
            or<button class="rpb" type="button" @click="refresh">Change </button> to a different email.

        </p>

        <!-- Role Selection -->
        <div v-if="email_valid">
            <h2>Welcome! This email will be registered as your USER_ID:</h2>

            <div>
                <input v-model="role" type="radio" id="influencer" name="role" value="influencer" />
                <label for="influencer">
                    <h2>Influencer</h2>
                </label>

                <input v-model="role" type="radio" id="sponsor" name="role" value="sponsor" />
                <label for="sponsor">
                    <h2>Sponsor</h2>
                </label>
            </div>

            <!-- Role-specific Forms -->
            <div>
                <div v-if="role === 'influencer'">
                    <InfluencerForm :email="email" :role="role" />
                </div>
                <div v-if="role === 'sponsor'">
                    <SponsorForm :email="email" :role="role" />
                </div>
                <div v-else-if="role === ''">
                    <h2>Please select a role</h2>
                </div>
            </div>

            <!-- Submit Button -->
            <!-- <button type="submit" :disabled="!email_valid || !role">Submit</button> -->
        </div>
    </form>
    <div>

    </div>
</template>

<style scoped>
/* General Input Styles */
input {
    padding: 10px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
    outline: none;
    transition: border-color 0.3s, background-color 0.3s;
}

/* Input Error State */
input.active {
    border-color: red;
    background-color: #ffe6e6;
    color: red;
}

/* Input Valid State */
input.valid {
    border-color: green;
    background-color: #e6ffe6;
    color: green;
}

/* Error Message */
.error {
    color: red;
    font-size: 0.9em;
    font-family: Arial, sans-serif;
    margin: 5px 0;
}

/* Button Styles */
button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

h1 {
    text-align: center;
    margin-top: 30px;
}

/* Role Selection Styles */
h2 {
    font-size: 1.2em;
    margin-top: 20px;
}

label {
    margin-right: 15px;
    cursor: pointer;
}

form {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
}
.rpb{
    background-color: #96c870;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    height: fit-content;
    width: fit-content;
}
</style>
