import { createApp } from 'vue'
import Antd from 'ant-design-vue';
import App from '@/App.vue'
import router from "@/router";

import 'ant-design-vue/dist/antd.css';
import * as Icons from '@ant-design/icons-vue';
import language from "./language";

// import language from "./language";

import '@/style/index.scss'

const app = createApp(App)
app.use(Antd)
app.use(router)
app.use(language)
app.mount('#app')

// 全局使用图标
for (const i in Icons) {
    app.component(i, Icons[i]);
}
