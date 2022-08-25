import ElementPlus from 'element-plus';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import type {App} from "vue";

const installElementPlus = (app: App) => {
    // 注册所有图标
    for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
        app.component(key, component)
    }
    // 引入element-plus
    app.use(ElementPlus);
}

export default installElementPlus

