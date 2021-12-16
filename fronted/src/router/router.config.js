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
                info:{ title: '首页', icon: 'dashboard-outlined' },
            },
        ]
    },
    {
        path: '/video',
        name: 'video',
        redirect: '/video/huYa',
        component: BasicLayout,
        info:{ title: '视频', icon: 'video-camera-two-tone' },
        children: [
            {
                path: 'huYa',
                name: 'huYa',
                component: () => import('@/views/video/HuYa'),
                info:{ title: '虎牙', icon: 'video-camera-outlined' },
            },
            {
                path: 'iQiYi',
                name: 'iQiYi',
                component: () => import('@/views/video/IQiYi'),
                info:{ title: '爱奇艺', icon: 'video-camera-outlined' },
            },
            {
                path: 'tencent',
                name: 'tencent',
                component: () => import('@/views/video/Tencent'),
                info:{ title: '腾讯', icon: 'video-camera-outlined' },
            },
            {
                path: 'youKu',
                name: 'youKu',
                component: () => import('@/views/video/YouKu'),
                info:{ title: '优酷', icon: 'video-camera-outlined' },
            },
        ]
    },
    {
        path: '/novel',
        name: 'novel',
        redirect: '/novel/biQuGe',
        component: BasicLayout,
        info:{ title: '小说', icon: 'book-two-tone' },
        children: [
            {
                path: 'biQuGe',
                name: 'biQuGe',
                component: () => import('@/views/novel/BiQuGe'),
                info:{ title: '笔趣阁', icon: 'book-outlined' },
            },
            {
                path: 'qiDian',
                name: 'qiDian',
                component: () => import('@/views/novel/QiDian'),
                info:{ title: '起点', icon: 'book-outlined' },
            }
        ]
    },
    {
        path: '/404',
        name: '404',
        component: () => import('@/views/exception/404'),
        info:{ hidden: true },
    }
]
