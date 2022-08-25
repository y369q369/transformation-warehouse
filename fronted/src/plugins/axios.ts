import axios from 'axios';
import {ElNotification} from 'element-plus'
import {localStore} from '@/stores/local'
import router from "./router"

// 添加请求拦截器
axios.interceptors.request.use(function (config) {
    // const store = localStore()
    // if (config.url !== '/api/user/login') {
    //     // @ts-ignore
    //     config.headers.token = store.token
    // }
    // 在发送请求之前做些什么
    return config;
}, function (error) {
    console.log(error)
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
axios.interceptors.response.use(function (response) {
    // const store = localStore()
    // if(response.headers.token) {
    //     store.storeToken(response.headers.token)
    // }
    // if (response.data.code !== 200) {
    //     router.push('/login')
    // }
    return response.data;
}, function (error) {
    ElNotification({
        title: error.response.status,
        message: error.response.statusText,
        type: 'error',
    })
    return Promise.reject(error.response)
})

export default axios