<script setup>
import { ref, onMounted, computed } from "vue";
import ProgressCard from '/src/components/common/progress.vue';


const projects = ref([]);
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));
const user_id = ref(userDetails?.id || ''); 


const fetchProjects = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/campaign", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
                'userDetails': JSON.stringify(userDetails),
            },
        });

        if (!response.ok) throw new Error("Failed to fetch projects");

        const data = await response.json();
        projects.value = data || []; 
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
            
            return 0;
        }

       
        const progress = ((now - startDate) / (endDate - startDate)) * 100;

        
        return Math.min(100, Math.max(0, progress)).toFixed(0);
    });
});


onMounted(() => {
    if (user_id.value) {
        fetchProjects(user_id.value);
    } else {
        console.error("Error: User ID is not defined.");
    }
});
</script>

<template>
    <div class="card-container">
        
        <ProgressCard v-for="(project, index) in projects" :key="index" :title="project.name"
            :progress="progressValues[index]" :description="project.description" :category="project.category" :budget="project.budget" :ad_requests="project.ad_requests"/>
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
