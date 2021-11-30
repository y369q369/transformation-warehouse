import Vue from 'vue';
import VueRouter from 'vue-router';
import {basicLayout} from "./router.config";


Vue.use(VueRouter);


const router = new VueRouter({
    mode: 'history',
    routes: basicLayout
})

export default router