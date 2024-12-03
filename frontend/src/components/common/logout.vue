<script setup>
import { ref } from 'vue';

const userDetails = ref(null);

// Retrieve user details from localStorage
const storedDetails = localStorage.getItem('userDetails');
if (storedDetails) {
    userDetails.value = JSON.parse(storedDetails);
}

// Logout function
const logout = () => {
    localStorage.removeItem('auth-token');
    localStorage.removeItem('userDetails');
    userDetails.value = null;
    router.push('/signin');
};

import defaultAvatar from '/src/assets/avatar.png'; 

const getAvatarUrl = (id) => {
    try {
       
        return new URL(`/src/assets/images/in${id}.png`, import.meta.url).href;
    } catch {
       
        console.warn(`Avatar not found for ID ${id}. Using default avatar.`);
        return defaultAvatar;
    }
};
</script>

<template>
    <div v-if="userDetails" class="top-left-container">

        <a :href="'/' + (userDetails.role || '/signin')">{{ userDetails.name.split(' ')[0] }}'s
        Home</a>
    </div>

    <div v-if="userDetails" class="top-right-container">
        <img :src="getAvatarUrl(userDetails.id) || 'src/assets/avatar.png'"  class="avatar">
        <a href="#" @click="logout()" class="logout-link">Logout</a>
    </div>

</template>


<style>

.top-right-container {
    position: fixed;
    top: 10px;
    right: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    
    z-index: 1000;
   
}
.top-left-container {
    position: fixed;
    top: 10px;
    left: 10px;
    display: flex;
    align-items: center;
    gap: 10px;

    z-index: 1000;
    
}

/* Style the avatar */
.avatar {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
}

/* Style the logout link */
.logout-link {
    font-size: 14px;
    color: #007bff;
    text-decoration: none;
    cursor: pointer;
}

.logout-link:hover {
    text-decoration: underline;
}

</style>
