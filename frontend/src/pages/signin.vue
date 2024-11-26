<script setup>
import { ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'

import aboutus from '../components/AboutUs.vue'
import services from '../components/Services.vue'
import contactus from '../components/ContactUs.vue'
import ourwork from '../components/OurWork.vue'
import brands_stars from '../components/brands_stars.vue'


const email = ref('')
const password = ref('')
const router = useRouter()

const activeTab = ref('aboutus');

const changeTab = (tab) => {
    activeTab.value = tab;
};

const submitForm = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/user-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        localStorage.setItem('auth-token', data.token);
        localStorage.setItem('userDetails', JSON.stringify({ id: data.id, role: data.role, name: data.name }));

        if (data.role === 'influencer') {
            router.push('/influencer')
        }
        else if (data.role === 'sponsor') {
            router.push('/sponsor')
        }
        else if (data.role === 'admin') {
            router.push('/admin')
        }
        else {
            console.log('Unknown role:', data.role);
        }


    } catch (error) {
        console.error('Error during login:', error);
        return alert('Enter Correct Email / Password')
    }
};
</script>

<template>
    <h1> Influencer Management & Sponsor Coordination Platform</h1>

    <div class="container">

        <div class="tab-container">
            <div class="tabs">
                <button @click="changeTab('aboutus')" :class="{ active: activeTab === 'aboutus' }">AboutUs</button>
                <button @click="changeTab('services')" :class="{ active: activeTab === 'services' }">Services</button>
                <button @click="changeTab('contactus')"
                    :class="{ active: activeTab === 'contactus' }">ContactUs</button>
                <button @click="changeTab('ourwork')" :class="{ active: activeTab === 'ourwork' }">OurWork</button>
            </div>
        </div>



        <div class="signblock">
            <form @submit.prevent="submitForm">

                <div class="form-inline">
                    <!-- Email Input -->
                    <input v-model="email" type="email" id="floatingInput" placeholder="Enter your email" />

                    <!-- Password Input -->
                    <input v-model="password" type="password" id="floatingPassword" placeholder="Enter your password" />

                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary">Sign In</button>
                </div>
                <p>
                    Don't have an account?
                    <router-link to="/register">Sign Up</router-link>
                </p>
            </form>
        </div>
        <div class="sections">
        </div>

        <div class="sections">
            <div v-if="activeTab === 'aboutus'">
                <p>
                    <aboutus />
                </p>
            </div>
            <div v-else-if="activeTab === 'services'">
                <p>
                    <services />
                </p>
            </div>
            <div v-else-if="activeTab === 'contactus'">
                <p>
                    <contactus />
                </p>
            </div>
            <div v-else-if="activeTab === 'ourwork'">
                <p>
                    <ourwork />
                </p>
            </div>
        </div>
        <div class="sections">
            <brands_stars />
        </div>
    </div>
</template>

<style scoped>
h1{
    text-align: left;
    color:#0056b3;
    font-size: 1.6em;
    /* font-weight: bold; */
    padding-top: 10px;
}
h3{
    text-align: center;
    color: #ff9900;
    font-size: 1.5em;
}
.sections {
    display: flex;
    /* border: #0056b3 1px solid; */
    gap: 10px;
    justify-content: top;
    padding: 20px;
    text-align: left;
    word-wrap: break-word;
    box-sizing: border-box;
    flex: 1;

    width: 100%;
   
}

.container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    /* Two sections per row */
    grid-template-rows: repeat(2, auto);
    /* Automatically adjust height */
    gap: 20px;
    height: 100vh;
    margin: 0;
    padding: 20px;
    box-sizing: border-box;
    width: 100%;
    /* Ensures the container fills the screen width */
}


.signblock {
    position: absolute;
        top: 0px; 
        right: 20px;
        width: auto;    
        padding: 10px;
        
    
}
.tab-container {
    width: 50%;
    /* Ensures the tab section takes 50% of the screen */
    margin: 0 auto;
    /* Centers the tab section */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0px 0;
    box-sizing: border-box;
}

.tabs {
    display: flex;
    justify-content: center;
    width: 100%;
    /* Ensure buttons span the container */
}

.tabs button {
    padding: 10px 20px;
    /* Increase padding for a wider appearance */
    width: 150px;
    /* Adjust button width */
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    background-color: white;
    transition: background-color 0.3s ease;
    text-align: center;
}

.tabs button.active {
    background-color: #007bff;
    color: white;
    font-weight: bold;
}

.tabs button:hover {
    background-color: #0056b3;
    color: white;
}
.form-inline {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    align-items: center;
}

input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 200px;
    height: 40px;
}



p {
    margin-top: 10px;
    margin-bottom: auto;
    text-align: center;
}

</style>
