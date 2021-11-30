import {BasicLayout} from "@/layouts";

export const basicLayout = [
    {
        path: '/',
        component: BasicLayout,
        redirect:'/dashboard'
    },
    {
        path: '/dashboard',
        name: 'topicModule',
        redirect: '/dashboard/workplace',
        hidden: true,
        children: [{
            path: 'workplace',
            name: 'workplace',
            component: () => import('@/views/dashboard/Workplace'),
        }]
    },
    {
        path: '/404',
        component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
    }
]