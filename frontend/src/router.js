import {createRouter, createWebHistory} from 'vue-router'

import SignIn from './pages/signin.vue'
import Register from './pages/register.vue'
import Dummy from './pages/dummy.vue'

const routes = [
  { path: "/signin", component: SignIn, name: "Signin" },
  { path: "/register", component: Register, name: "Register" },
  { path: "/dummy", component: Dummy, name: "Dummy" },
];

const router = createRouter({history: createWebHistory(), routes})

export default router