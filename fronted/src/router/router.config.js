import {BasicLayout} from "@/layouts";

export const basicLayout = [
    {
        path: '/',
        name: 'home',
        redirect: '/dashboard',
        component: BasicLayout,
        info:{ hidden: true },
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                component: () => import('@/views/dashboard/DashBoard'),
                info:{ title: 'side.dashboard', icon: 'dashboard-outlined' },
            },
            {
                path: 'novel',
                name: 'novel',
                component: () => import('@/views/novel/Novel'),
                info:{ title: 'side.novel', icon: 'book-outlined' },
            },
            {
                path: 'novel/catalog',
                name: 'catalog',
                component: () => import('@/views/novel/Catalog'),
                info:{ hidden: true },
            }
        ]
    },
    {
        path: '/video',
        name: 'video',
        redirect: '/video/huYa',
        component: BasicLayout,
        info:{ title: 'side.video', icon: 'video-camera-two-tone' },
        children: [
            {
                path: 'huYa',
                name: 'huYa',
                component: () => import('@/views/video/HuYa'),
                info:{ title: 'side.huYa', icon: 'video-camera-outlined' },
            },
            {
                path: 'iQiYi',
                name: 'iQiYi',
                component: () => import('@/views/video/IQiYi'),
                info:{ title: 'side.iQiYi', icon: 'video-camera-outlined' },
            },
            {
                path: 'tencent',
                name: 'tencent',
                component: () => import('@/views/video/Tencent'),
                info:{ title: 'side.tencent', icon: 'video-camera-outlined' },
            },
            {
                path: 'youKu',
                name: 'youKu',
                component: () => import('@/views/video/YouKu'),
                info:{ title: 'side.youKu', icon: 'video-camera-outlined' },
            },
        ]
    },
    {
        path: '/404',
        name: '404',
        component: () => import('@/views/exception/404'),
        info:{ hidden: true },
    }
]
