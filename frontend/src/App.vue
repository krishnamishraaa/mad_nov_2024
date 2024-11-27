<script setup> 
import { useRouter } from 'vue-router'
import Logout from './components/common/logout.vue';


const router = useRouter()

router.beforeEach((to, from, next) => {
  const publicPages = ['Signin', 'Register', 'Home', 'AboutUs', 'ContactUs', 'Services', 'OurWork'];

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