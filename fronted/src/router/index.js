import { createRouter, createWebHistory } from 'vue-router';
import {basicLayout} from "@/router/router.config";

const router = createRouter({
    history: createWebHistory(),
    routes: basicLayout
})

export default router
