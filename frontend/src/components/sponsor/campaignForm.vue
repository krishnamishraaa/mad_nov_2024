<script setup>
import { ref } from 'vue'
const name = ref('')
const description = ref('')
const start_date = ref('')
const end_date = ref('')
const budget = ref('')
const category = ref('')
const niche = ref('')
const visibility = ref('')
const goals= ref('')
const requirements =ref({
  photo: false,
  video: false,
  shorts: false,
  post: false
})
const authToken = localStorage.getItem('auth-token');
const userDetails = JSON.parse(localStorage.getItem('userDetails'));

const submit_campaign= async() => {
  try{
    const response = await fetch('http://127.0.0.1:5000/api/campaign', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        'userDetails': JSON.stringify(userDetails)

      },
        body: JSON.stringify({
          "name": name.value,
          "description": description.value,
          "start_date": start_date.value,
          "end_date": end_date.value,
          "budget": budget.value,
          "category": category.value,
          "niche": niche.value,
          "visibility": visibility.value,
          "goals": goals.value,
          "status": "Active",
          "requirements": JSON.stringify({
            photo: requirements.photo,
            video: requirements.video,
            shorts: requirements.shorts,
            post: requirements.post
          }),

      }),
    }
    )
      if (!response.ok)
       {
        const message = `An error has occured: ${response.status}`
        throw new Error(message)

      }
      alert('Campaign Created Successfully')

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
        <input type="text" v-model="description" class="form-control" placeholder="Campaign_Description"
          aria-label="Campaign_Description">
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
      <!-- Budget Field -->
      <div class="col">
        <label for="budget">Budget</label>
        <input type="number" id="budget" v-model="budget" class="form-control" placeholder="Budget">
      </div>


      <!-- Visibility Field -->
      <div class="col">
        <label>Visibility</label>
        <div>
          <input type="radio" id="visibility-true" value="True" v-model="visibility">
          <label for="visibility-true">True</label>

          <input type="radio" id="visibility-false" value="False" v-model="visibility">
          <label for="visibility-false">False</label>
        </div>
      </div>
    </div>
    <div class="col">
      <!-- Check boxes with details of requirements -->
      <label>Requirements</label>

    
        <input class="checkbox" type="checkbox" id="photo" value="photo">
        <label for="photo">Photo</label>
        <input class="checkbox" type="checkbox" id="video" value="video">
        <label for="video">Video</label>
        <input class="checkbox" type="checkbox" id="shorts" value="shorts">
        <label for="shorts">Shorts</label>
        <input class="checkbox" type="checkbox" id="post" value="post">
        <label for="post">Post</label>
    </div>
    <br>
    <div class="row">
      <div class="col">
        <input type="text" v-model="category" class="form-control" placeholder="Category" aria-label="Category">
      </div>
      <div class="col">
        <input type="text" v-model="niche" class="form-control" placeholder="Niche" aria-label="Niche">
      </div>
    </div>
    <div class="row">
      <div class="col">
        <input type="text" v-model="goals" class="form-control" placeholder="Goals" aria-label="Goal">
      </div>
    </div>
    <button type="submit" class="btn btn-success">Create Campaign</button>
  </form>
</template>


<style scoped>
/* General form layout */
form {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  max-width: 600px;
  margin: 5px 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Row layout */
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
}

/* Input fields */
input.form-control,
select.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

input.form-control:focus,
select.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Placeholder for select dropdown */
select.form-control {
  background-color: white;
  appearance: none;
  cursor: pointer;
}

/* Button styling */
button.btn {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button.btn-success {
  background-color: #28a745;
  color: white;
}

button.btn-success:hover {
  background-color: #218838;
}

/* Headline */
h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-weight: bold;
}
.checkbox{
  display: inline;
  size:big;
  margin-left: 20px;
  margin-right:10px;
  transform: scale(1.5);
}
</style>
