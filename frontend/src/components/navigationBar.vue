<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
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
</script>

<template>
    <!-- Conditional Navigation Bar -->
    <div v-if="userDetails">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand" :href="'/' + (userDetails.role || '/signin')">{{ userDetails.name }}'s Home</a>
                <button class=" navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">

                        <!-- Admin Role -->

                        <template v-if="userDetails.role === 'admin'">
                            <li class="nav-item">
                                <router-link to="/admin-users" class="nav-link">Users</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/admin-campaign" class="nav-link">Campaign</router-link>
                            </li>
                        </template>

                        <!-- Sponsor Role -->
                        <template v-else-if="userDetails.role === 'sponsor'">

                            <li class="nav-item">
                                <router-link to="/campaign" class="nav-link">Campaigns</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/explore_INfluencier" class="nav-link">Search
                                    Influencers</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/adRequests" class="nav-link">AD Requests</router-link>
                            </li>
                        </template>

                        <!-- Influencer Role -->
                        <template v-else-if="userDetails.role === 'influencer'">

                            <li class="nav-item">
                                <router-link to="/search-campaign" class="nav-link">Campaigns</router-link>
                            </li>

                            <li class="nav-item">
                                <router-link to="/edit-profile" class="nav-link">Edit Profile</router-link>
                            </li>

                        </template>

                        <!-- Common Avatar and Logout -->
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                data-bs-toggle="dropdown" aria-expanded="false">
                                <img src="../assets/avatar.png" alt="User Photo" class="rounded-circle" width="30"
                                    height="30">
                            </a>
                        </li>
                        <li>
                            <a href="#" @click="logout()" class="dropdown-item">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
    <!-- No User Logged In -->
    <div v-else>
        <!-- Navigation bar is hidden -->
    </div>
</template>

<style>

</style>
