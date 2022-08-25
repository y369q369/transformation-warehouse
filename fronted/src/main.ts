import {createApp} from "vue"
import {createPinia} from "pinia"

import App from "./App.vue"
import router from "./plugins/router"
import svgIcon from "@/components/SvgIcon.vue";
import 'virtual:svg-icons-register'
import installElementPlus from "./plugins/element"

import 'element-plus/dist/index.css'
import "./assets/css/main.css"


const app = createApp(App)

installElementPlus(app)

app.use(createPinia())
app.use(router)
app.component('svg-icon', svgIcon)
app.mount("#app")
