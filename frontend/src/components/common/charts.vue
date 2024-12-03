<script setup>
import { ref, onMounted } from "vue";
import { Line } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale } from "chart.js";

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale);

// Declare reactive data for chart
// const chartData = ref({});
const chartData = ref({
  labels: [],
  datasets: []
});
const chartOptions = ref({
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: "Time Series Data"
    }
  },
  scales: {
    x: {
      type: "category",
      title: {
        display: true,
        text: "Date"
      }
    },
    y: {
      title: {
        display: true,
        text: "Count"
      }
    }
  }
});

// Define props
const props = defineProps({
  apiEndpoint: {
    type: String,
    required: true
  }
});


const fetchData = async () => {
  try {
    const response = await fetch(props.apiEndpoint); 
    const data = await response.json();
    // const { campaigns, ad_requests, users } = data;

    const campaigns = data.campaigns || {};
    const ad_requests = data.ad_requests || {};
    const users = data.users || {};

    // Collect all unique dates from all data sources
    const allDates = new Set([
      ...Object.keys(campaigns),
      ...Object.keys(ad_requests),
      ...Object.keys(users)
    ]);

    // Prepare chart data
    chartData.value = {
      labels: Array.from(allDates).sort(),
      datasets: [
        {
          label: "Campaigns",
          data: Array.from(allDates).map((date) => campaigns[date] || 0),
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1
        },
        {
          label: "Ad Requests",
          data: Array.from(allDates).map((date) => ad_requests[date] || 0),
          fill: false,
          borderColor: "rgb(255, 99, 132)",
          tension: 0.1
        },
        {
          label: "User Signups",
          data: Array.from(allDates).map((date) => users[date] || 0),
          fill: false,
          borderColor: "rgb(54, 162, 235)",
          tension: 0.1
        }
      ]
    };
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};


onMounted(() => {
  fetchData();
});
</script>

<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
   
  </div>
</template>
