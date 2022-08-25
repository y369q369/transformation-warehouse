import router from "@/router"
// import { routeStore } from '@/stores/cache'
//
// // 登录控制：①未登录先登录，在进入登录前访问的页面 ②已登陆直接访问
// router.beforeEach((to, from) => {
//     const access = routeStore()
//     const token = localStorage.getItem('token')
//     if (token) {
//         if (access.access != '' && access.access != to.name) {
//             return { name: access.access }
//         } else {
//             access.access = ''
//         }
//     } else {
//         if (to.name != 'login') {
//             access.access = <string>to.name
//             return { name: 'login' }
//         }
//     }
//     return true
// })
//
export default router