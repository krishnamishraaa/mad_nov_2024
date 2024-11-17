<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
const email = ref('')
const password = ref('')
const router = useRouter()
const submitForm = async () => {
    try{
        const response = await fetch('http://127.0.0.1:5000/user-login',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        })
        const data = await response.json()
        localStorage.setItem('auth-token', data.token)
        if(data.role === "admin"){
            router.push({path:'/dummy'})
        }
    }

    //  Vendor & User goes here

catch(error){
    console.log(error)
}
}

</script>

<template>
   <form @submit.prevent = "submitForm">
    <h1> Sign IN</h1>
    <div>
        <input v-model = "email" type ="email" id = "floatingInput" placeholder="enter your email">
        <label for="floatingInput">Email</label>

    </div>
     <div>
        <input v-model = "password" type ="password" id = "floatingPassword" placeholder="enter your password">
        <label for="floatingPassword">Password</label>

    </div>
    <button type="submit">Sign In</button>
    <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
   </form> 

</template>

<style>

</style>