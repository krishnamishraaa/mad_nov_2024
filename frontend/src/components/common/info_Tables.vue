<script setup>
import { defineProps } from 'vue';

defineProps({
    name: String,
    description: String,
    start_date: String,
    end_date: String,
    budget: String,
    active_Creators: Int16Array,
    category: String,
    niche: String,
    reach: String,
    current_engagement: String,
});
</script>

<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Property</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Name</td>
                    <td>{{ name }}</td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td>{{ description }}</td>
                </tr>
                <tr>
                    <td>Start Date</td>
                    <td>{{ start_date }}</td>
                </tr>
                <tr>
                    <td>End Date</td>
                    <td>{{ end_date }}</td>
                </tr>
                <tr>
                    <td>Budget</td>
                    <td>{{ budget }}</td>
                </tr>
                <tr>
                    <td>Active Creators</td>
                    <td>{{ active_Creators }}</td>
                </tr>
                <tr>
                    <td>Category</td>
                    <td>{{ category }}</td>
                </tr>
                <tr>
                    <td>Niche</td>
                    <td>{{ niche }}</td>
                </tr>
                <tr>
                    <td>Reach</td>
                    <td>{{ reach }}</td>
                </tr>
                <tr>
                    <td>Current Engagement</td>
                    <td>{{ current_engagement }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.table-container {
    margin: 20px;
    overflow-x: auto;
    /* Ensures the table is scrollable on smaller screens */
}

table {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
    color: #333;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

tr:hover {
    background-color: #f1f1f1;
}

td {
    color: #555;
}
</style>
