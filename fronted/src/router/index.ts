import {createRouter, createWebHistory} from "vue-router";
import Layout from "../views/layout/Layout.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            redirect: '/dashboard',
            component: Layout,
            children: [
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    component: () => import('../views/Dashboard.vue'),
                    meta: {title: '面板', icon: 'dashboard'}
                }
            ]
        },
        {
            path: '/video',
            name: 'video',
            redirect: '/video/tencent',
            component: Layout,
            meta: {title: '视频', icon: 'video'},
            children: [
                {
                    path: '/video/tencent',
                    name: 'tencent',
                    component: () => import('../views/video/Tencent.vue'),
                    meta: {title: '腾讯', icon: 'tencent'}
                },
                {
                    path: '/video/youKu',
                    name: 'youKu',
                    component: () => import('../views/video/YouKu.vue'),
                    meta: {title: '优酷', icon: 'youKu'}
                },
                {
                    path: '/video/xj',
                    name: 'xj',
                    component: () => import('../views/video/Xj.vue'),
                    meta: {title: '香蕉', icon: 'xj'}
                }
            ]
        },
        {
            path: '/novel',
            name: 'novel',
            redirect: '/novel/biQuGe',
            component: Layout,
            meta: {title: '小说', icon: 'novel'},
            children: [
                {
                    path: '/menu/biQuGe',
                    name: 'biQuGe',
                    component: () => import('../views/novel/BiQuGe.vue'),
                    meta: {title: '笔趣阁', icon: 'biQuGe'}
                },
                {
                    path: '/menu/qiDian',
                    name: 'qiDian',
                    component: () => import('../views/novel/QiDian.vue'),
                    meta: {title: '起点', icon: 'qiDian'}
                }
            ]
        },
        // {
        //     path: '/user',
        //     name: 'user',
        //     redirect: '/user/info',
        //     component: Layout,
        //     children: [
        //         {
        //             path: '/user/info',
        //             name: 'UserInfo',
        //             component: () => import('../views/user/UserInfo.vue'),
        //             meta: {title: '用户', icon: 'user'}
        //         }
        //     ]
        // },
        // {
        //     path: "/login",
        //     name: "login",
        //     component: () => import('../views/login/Login.vue'),
        //     meta: {hidden: true}
        // },
    ],
});

export default router;
