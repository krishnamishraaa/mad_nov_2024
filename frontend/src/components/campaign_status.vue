<script setup>
import { ref, onMounted, computed } from "vue";
import ProgressCard from '/src/components/progress.vue';

// Reactive variable to hold the projects
const projects = ref([]);
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

// Simulate an API call
const fetchProjects = async () => {
    try {
        // Replace with your API endpoint
        const response = await fetch("http://127.0.0.1:5000/api/campaign",{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
        } });
    
        if (!response.ok) throw new Error("Failed to fetch projects");
        const data = await response.json();
        projects.value = data; // Assuming data is an array of project objects
        console.log("Fetched projects:", projects.value);
    } catch (error) {
        console.error("Error fetching projects:", error);
    }
};

const progressValues = computed(() => {
    return projects.value.map((project) => {
        const now = Date.now();
        const startDate = new Date(project.start_date).getTime();
        const endDate = new Date(project.end_date).getTime();

        if (endDate === startDate || now < startDate) {
            // If dates are invalid or the project hasn't started yet
            return 0;
        }

        // Calculate progress percentage
        const progress = ((now - startDate) / (endDate - startDate)) * 100;

        // Clamp the value between 0 and 100
        return Math.min(100, Math.max(0, progress)).toFixed(0);
    });
});


// Fetch data when the component mounts
onMounted(() => {
    fetchProjects();
});
</script>

<template>
    <div class="card-container">
        <ProgressCard v-for="(project, index) in projects" :key="index" :title="project.name"
            :progress="progressValues[index]" :description="project.description" />
    </div>
</template>

<style>
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
}
</style>
