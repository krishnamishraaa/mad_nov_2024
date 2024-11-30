import {createRouter, createWebHistory} from 'vue-router'

import SignIn from './pages/signin.vue'
import Register from './pages/register.vue'
import Admin from './pages/admin.vue'
import Influencer from './pages/influencer.vue'
import Sponsor from './pages/sponsor.vue'
// import Campaign from './pages/campaign.vue'
// import InfluencerProfile from './pages/influencerProfile.vue'
// import explore_INfluencier from './components/explore_INfluencier.vue'



const routes = [
  {path	: "/", redirect: "/signin"},
  { path: "/signin", component: SignIn, name: "Signin" },
  { path: "/register", component: Register, name: "Register" },
  { path: "/admin", component: Admin, name: "Admin" },
  {path: "/influencer", component: Influencer, name: "Influencer"},
  {path: "/sponsor", component: Sponsor, name: "Sponsor"},
  // {path: "/campaign", component: Campaign, name: "Campaign"},
  // {path: "/influencerProfile", component: InfluencerProfile, name: "InfluencerProfile"},
  // {path: "/explore_INfluencier", component: explore_INfluencier, name: "explore_INfluencier"},
 

];

const router = createRouter({history: createWebHistory(), routes})

export default router