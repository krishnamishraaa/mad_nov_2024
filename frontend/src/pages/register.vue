<script setup>

</script>

<template>
   <form>
    <h1> Sign IN</h1>
    <div>
        <input type ="email" id = "floatingInput" placeholder="enter your email">
        <label for="floatingInput">Email</label>

    </div>

     <div>
        <input type ="password" id = "floatingPassword" placeholder="enter your password">
        <label for="floatingPassword">Password</label>

    </div>
    <button type="submit">Sign In</button>
    <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
   </form> 

</template>

<style>

</style>