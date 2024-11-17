<script setup>
import { ref } from 'vue'
const name = ref('')
const description = ref('')
const start_date = ref('')
const end_date = ref('')
const budget = ref('')
const visibility = ref('')



const submit_campaign= async() => {
  try{
    const response = await fetch('http://localhost:5000/api/campaign', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'},
        body: JSON.stringify({
          "name": name.value,
          "description": description.value,
          "start_date": start_date.value,
          "end_date": end_date.value,
          "budget": budget.value,
          "visibility": visibility.value
      })
    }
    )
      if (!response.ok)
       {
        const message = `An error has occured: ${response.status}`
        throw new Error(message)

      }
      return await response.json()
    }
  catch (error) {
    console.error('Error:', error);
  }
}

</script>

<template>
  <!-- Forms -->
   <form @submit.prevent="submit_campaign">
   <div class="row">
  <div class="col">
    <input type="text" v-model="name" class="form-control" placeholder="Campaign_name" aria-label="Campaign_name">
  </div>
  <div class="col">
    <input type="text" v-model="description" class="form-control" placeholder="Campaign_Description" aria-label="Campaign_Description">
  </div>
</div>
<br>
<div class="row">
  <div class="col">
    <input type="date" v-model="start_date" class="form-control" placeholder="Start Date" aria-label="Start Date">
  </div>
  <div class="col">
    <input type="date" v-model="end_date" class="form-control" placeholder="End Date" aria-label="End Date">
  </div>
</div>
<br>
<div class="row">
  <div class="col">
    <input type="text" v-model="budget" class="form-control" placeholder="Budget" aria-label="Budget">
  </div>
  <select class="col form-control" v-model="visibility" placeholder="Visibility" aria-label="Visibility">
    <option value = "True" > True </option>
    <option value = "False" > False </option>
  </select>
</div>
<button type="submit" class="btn btn-success">Create Campaign</button>
</form>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
