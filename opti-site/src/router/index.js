import Vue from 'vue'
import Router from 'vue-router'
import home from '../components/home.vue'
import filter_design from '../components/filter_design.vue'
import antenna_design from '../components/antenna_design.vue'
import architecture from '../components/architecture.vue'

Vue.use(Router)

const router = new Router({
    routes: [
        { path: '/', redirect: '/home' },
        {
            path: '/home',
            name: 'home',
            component: home
        },
        {
            path: '/antenna_design',
            name: 'antenna_design',
            component: antenna_design
        },
        {
            path: '/filter_design',
            name: 'filter_design',
            component: filter_design
        },
        {
            path: '/architecture',
            name: 'architecture',
            component: architecture
        },
    ]
})
export default router
