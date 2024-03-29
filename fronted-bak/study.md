# 创建

> **说明**
>
> vue3 项目创建依赖 vue3 脚手架

```sh
# 下载vue3脚手架
npm install -g @vue/cli # 或 yarn global add @vue/cli

# 创建项目
vue create front
# 选择 vue 3 preset
```

# 组件使用

## ant-design-vue

### 官网

https://next.antdv.com/components/overview-zhCn/

### 安装（^3.0.0-alpha.14）

```sh
# 通用组件
yarn add ant-design-vue@next

# 图标
yarn add @ant-design/icons-vue
```

### 全局（main.js）引用

```javascript
// 全局引用通用组件
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
app.use(Antd)

// 全局引用图标
import * as Icons from '@ant-design/icons-vue';
for (const i in Icons) {
    app.component(i, Icons[i]);
}
```

## Vue Router

### 官网

https://next.router.vuejs.org/zh/guide/

### 安装

```sh
yarn add vue-router@4
```

### 使用

#### 创建路由

如下目录结构

```sh
+-----------------------------+
| src                         |
| +-------------------------+ |
| | router                  | |
| | +---------------------+ | |
| | | index.js            | | |
| | | router.config.js    | | |
| | |                     | | |
| | +---------------------+ | |
| +-------------------------+ |
+-----------------------------+
```

**index.js**

```js
import { createRouter, createWebHashHistory } from 'vue-router';
import {basicLayout} from "@/router/router.config";

const router = createRouter({
    history: createWebHashHistory(),
    routes: basicLayout
})

export default router
```

**router.config.js**

```js
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
    {
        path: '/404',
        component: () => import('@/views/exception/404')
    }
]
```

#### 全局引用

**main.js**

```js
import router from "@/router";
app.use(router)
```

## node-sass

> **说明**
>
> node-sass版本和node版本关联，版本不匹配，报错 TypeError: this.getOptions is not a function

版本对应

- node-sass 和 node：https://github.com/sass/node-sass#node-version-support-policy

- node-sass 和 sass-loader：https://github.com/webpack-contrib/sass-loader/blob/master/CHANGELOG.md

  > **node 14**
  >
  > "node-sass": "^4.14.1"
  > "sass-loader": "^10.0.4"

  > **node 16**
  >
  > "node-sass": "5.0.0",
  > "sass-loader": "10.1.1"

安装

```sh
# 查看 包 所有版本
npm view node-sass versions
yarn info node-sass versions

# 指定版本包，当前
npm install node-sass@6.0.1 -D
yarn add node-sass@5.0.0 sass-loader@10.1.1 -D
```

## vue-i18n

### 官网

https://kazupon.github.io/vue-i18n/zh/introduction.html

### 安装

```sh
# 通用组件
yarn add ant-design-vue@next
# 图标
yarn add @ant-design/icons-vue
```

### 使用

#### 配置语言环境

```js
import {createI18n} from 'vue-i18n'

const i18n = createI18n({
    locale: 'enUS',
    messages: {
        zhCn: {
            side: {
                dashboard: '首页',
                video: '视频',
                huYa: '虎牙',
                iQiYi: '爱奇艺',
                tencent: '腾讯',
                youKu: '优酷',
                novel: '小说',
                biQuGe: '笔趣阁',
                qiDian: '起点'
            }
        },
        enUS: {
            side: {
                dashboard: 'dashboard',
                video: 'video',
                huYa: 'huYa',
                iQiYi: 'iQiYi',
                tencent: 'tencent',
                youKu: 'youKu',
                novel: 'novel',
                biQuGe: 'biQuGe',
                qiDian: 'qiDian'
            }
        }
    }
})

export default i18n
```

#### 全局引用

main.js

```javascript
import i18n from "./locales";

app.use(i18n)
```

#### 多语言使用

```html
<p>{{ $t('message.hello', { msg: 'hello' }) }}</p>
```

