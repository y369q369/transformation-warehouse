import { createRouter, createWebHashHistory } from 'vue-router';
import {basicLayout} from "./router.config";

const router = createRouter({
    history: createWebHashHistory(),
    routes: basicLayout
})

export default router