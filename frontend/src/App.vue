<script setup> 
import { useRouter } from 'vue-router'


const router = useRouter()


router.beforeEach((to, from, next) => {
  const publicPages = ['Signin', 'Register'];

  if (!publicPages.includes(to.name) && !localStorage.getItem('auth-token')) {
    next({ name: 'Signin' });
  } else {
    next();
  }
})
</script>

<template>
  <router-view />
</template>

<style>

</style>