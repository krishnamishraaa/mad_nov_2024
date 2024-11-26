import { createApp, ref, onMounted, defineComponent, h } from 'vue'
import Router from './router'
// import './style.css'
import  '../src/assets/main.css'

import App from './App.vue'

const app = createApp(App)
app.use(Router)
app.mount('#app')


