import {BasicLayout} from "@/layouts";

export const basicLayout = [
    {
        path: '/',
        redirect: '/dashboard',
        component: BasicLayout,
        children: [{
            path: 'dashboard',
            name: 'dashboard',
            component: () => import('@/views/dashboard/DashBoard'),
        }]
    },
    // {
    //     path: '/dashboard',
    //     name: 'topicModule',
    //     redirect: '/dashboard/workplace',
    //     hidden: true,
    //     children: [{
    //         path: 'workplace',
    //         name: 'workplace',
    //         component: () => import('@/views/dashboard/Workplace'),
    //     }]
    // },
    {
        path: '/404',
        component: () => import('@/views/exception/404')
    }
]