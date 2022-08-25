# svg学习

### 基础知识

> 参考资料
>
> https://baike.baidu.com/item/SVG%E6%A0%BC%E5%BC%8F/3463453?fr=aladdin

- SVG 指可伸缩矢量图形 (Scalable Vector Graphics)
- SVG 用来定义用于网络的基于矢量的图形
- SVG 使用 [XML](https://baike.baidu.com/item/XML/86251) 格式定义图形
- SVG 图像在放大或改变尺寸的情况下其图形质量不会有所损失
- SVG 是[万维网联盟](https://baike.baidu.com/item/万维网联盟/1458269)的标准
- SVG 与诸如 [DOM](https://baike.baidu.com/item/DOM/50288) 和 [XSL](https://baike.baidu.com/item/XSL/838292)
  之类的 [W3C](https://baike.baidu.com/item/W3C/216888) 标准是一个整体

### 基础使用

> 参考资料
>
> https://www.w3school.com.cn/svg/index.asp
>
> https://www.runoob.com/svg/svg-tutorial.html

- 使用示例

```html
<!-- 直接使用 -->
<!DOCTYPE html>
<html>
    <body>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <circle cx="100" cy="50" r="40" stroke="black" stroke-width="2" fill="red"/>
        </svg>
    </body>
</html>


<!-- 本地引用其他svg -->
<!DOCTYPE html>
<html>
    <head>
        <script src="https://at.alicdn.com/t/c/font_3604969_9ocug20lrqe.js?spm=a313x.7781069.1998910419.53&file=font_3604969_9ocug20lrqe.js"></script>
    </head>
    <body>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <use xlink:href="#icon-weixiu"></use>
        </svg>
    </body>
</html>

```

- 属性说明

  部分常用属性

  | 属性   | 说明                             | 使用                                                       |
  	| ------ | -------------------------------- | ---------------------------------------------------------- |
  | path   | 使用路径自定义图形               | <path d="M150 0 L75 200 L225 200 Z" />                     |
  | symbol | 定义一个图形模板对象，本身不显示 | <symbol id="icon-weixiu" viewBox="0 0 1024 1024"></symbol> |
  | use    | 引用其他定义id的svg图形          | <use :xlink:href="#icon-weixiu"></use>                     |

  其他属性：https://www.runoob.com/svg/svg-reference.html

### iconfont字体库

> 官网： https://www.iconfont.cn/home/index?spm=a313x.7781069.1998910419.2

- 官网使用文档：https://www.iconfont.cn/help/detail?spm=a313x.7781069.1998910419.d8d11a391&helptype=code

> 下载svg图标

- 进入图标库

  ![image-20220823152232695](F:\workspace\idea\big-eat-drink\frontend\business\svg-study.assets\image-20220823152232695.png)


- 搜索图标

  ![image-20220823152540027](F:\workspace\idea\big-eat-drink\frontend\business\svg-study.assets\image-20220823152540027.png)

- 鼠标悬浮，点击下载按钮

  ![image-20220823152729339](F:\workspace\idea\big-eat-drink\frontend\business\svg-study.assets\image-20220823152729339.png)

- 下载svg格式（两种方式皆可）

  ![image-20220823152951395](F:\workspace\idea\big-eat-drink\frontend\business\svg-study.assets\image-20220823152951395.png)

> 使用svg图标

```html
<!-- 1、下载svg 示例如下 -->
<svg t="1661237225684" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2411" width="200" height="200"><path d="M217.6 659.2c0-19.2-6.4-38.4-19.2-51.2s-32-25.6-51.2-25.6c-19.2 0-38.4 12.8-51.2 25.6-12.8 12.8-25.6 32-25.6 51.2 0 19.2 6.4 38.4 19.2 51.2s32 19.2 51.2 19.2c19.2 0 38.4-6.4 51.2-19.2s25.6-32 25.6-51.2z m108.8-256c0-19.2-6.4-38.4-19.2-51.2s-32-25.6-51.2-25.6c-19.2 0-38.4 6.4-51.2 19.2s-19.2 38.4-19.2 57.6c0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2s19.2-32 19.2-51.2zM576 678.4l57.6-217.6c0-12.8 0-19.2-6.4-25.6-6.4-12.8-12.8-19.2-19.2-19.2H576c-6.4 6.4-12.8 12.8-12.8 25.6l-57.6 217.6c-25.6 0-44.8 12.8-64 25.6-19.2 12.8-32 32-38.4 57.6-6.4 32-6.4 57.6 12.8 83.2 12.8 25.6 38.4 44.8 64 51.2s57.6 6.4 83.2-12.8c25.6-12.8 44.8-38.4 51.2-64 6.4-25.6 6.4-44.8-6.4-64 0-25.6-12.8-44.8-32-57.6z m377.6-19.2c0-19.2-6.4-38.4-19.2-51.2-12.8-12.8-32-19.2-51.2-19.2-19.2 0-38.4 6.4-51.2 19.2-12.8 12.8-19.2 32-19.2 51.2 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 6.4-12.8 19.2-32 19.2-51.2zM582.4 294.4c0-19.2-6.4-38.4-19.2-51.2-12.8-19.2-32-25.6-51.2-25.6-19.2 0-38.4 6.4-51.2 19.2-12.8 19.2-19.2 38.4-19.2 57.6 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 12.8-12.8 19.2-32 19.2-51.2z m256 108.8c0-19.2-6.4-38.4-19.2-51.2-12.8-12.8-32-19.2-51.2-19.2-19.2 0-38.4 6.4-51.2 19.2-12.8 12.8-19.2 32-19.2 51.2 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 12.8-12.8 19.2-32 19.2-51.2z m185.6 256c0 102.4-25.6 192-83.2 275.2-6.4 12.8-19.2 19.2-32 19.2H108.8c-12.8 0-25.6-6.4-32-19.2C25.6 851.2 0 755.2 0 659.2c0-70.4 12.8-134.4 38.4-198.4s64-115.2 108.8-166.4 102.4-83.2 166.4-108.8 128-38.4 198.4-38.4 134.4 12.8 198.4 38.4 115.2 64 166.4 108.8c44.8 44.8 83.2 102.4 108.8 166.4 25.6 64 38.4 128 38.4 198.4z" fill="#409EFF" p-id="2412"></path></svg>


<!-- 2、下载的svg直接复制到html中可直接展示 -->

<!-- 3、将下载的svg用symbol包裹一层，可被引用，示例如下 -->
<!-- 3.1、修改后的svg文件命名为 dashboard.vue -->
<svg t="1661237225684" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2411" width="200" height="200"><symbol id="icon-dashboard" viewBox="0 0 1024 1024"><path d="M217.6 659.2c0-19.2-6.4-38.4-19.2-51.2s-32-25.6-51.2-25.6c-19.2 0-38.4 12.8-51.2 25.6-12.8 12.8-25.6 32-25.6 51.2 0 19.2 6.4 38.4 19.2 51.2s32 19.2 51.2 19.2c19.2 0 38.4-6.4 51.2-19.2s25.6-32 25.6-51.2z m108.8-256c0-19.2-6.4-38.4-19.2-51.2s-32-25.6-51.2-25.6c-19.2 0-38.4 6.4-51.2 19.2s-19.2 38.4-19.2 57.6c0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2s19.2-32 19.2-51.2zM576 678.4l57.6-217.6c0-12.8 0-19.2-6.4-25.6-6.4-12.8-12.8-19.2-19.2-19.2H576c-6.4 6.4-12.8 12.8-12.8 25.6l-57.6 217.6c-25.6 0-44.8 12.8-64 25.6-19.2 12.8-32 32-38.4 57.6-6.4 32-6.4 57.6 12.8 83.2 12.8 25.6 38.4 44.8 64 51.2s57.6 6.4 83.2-12.8c25.6-12.8 44.8-38.4 51.2-64 6.4-25.6 6.4-44.8-6.4-64 0-25.6-12.8-44.8-32-57.6z m377.6-19.2c0-19.2-6.4-38.4-19.2-51.2-12.8-12.8-32-19.2-51.2-19.2-19.2 0-38.4 6.4-51.2 19.2-12.8 12.8-19.2 32-19.2 51.2 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 6.4-12.8 19.2-32 19.2-51.2zM582.4 294.4c0-19.2-6.4-38.4-19.2-51.2-12.8-19.2-32-25.6-51.2-25.6-19.2 0-38.4 6.4-51.2 19.2-12.8 19.2-19.2 38.4-19.2 57.6 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 12.8-12.8 19.2-32 19.2-51.2z m256 108.8c0-19.2-6.4-38.4-19.2-51.2-12.8-12.8-32-19.2-51.2-19.2-19.2 0-38.4 6.4-51.2 19.2-12.8 12.8-19.2 32-19.2 51.2 0 19.2 6.4 38.4 19.2 51.2 12.8 12.8 32 19.2 51.2 19.2 19.2 0 38.4-6.4 51.2-19.2 12.8-12.8 19.2-32 19.2-51.2z m185.6 256c0 102.4-25.6 192-83.2 275.2-6.4 12.8-19.2 19.2-32 19.2H108.8c-12.8 0-25.6-6.4-32-19.2C25.6 851.2 0 755.2 0 659.2c0-70.4 12.8-134.4 38.4-198.4s64-115.2 108.8-166.4 102.4-83.2 166.4-108.8 128-38.4 198.4-38.4 134.4 12.8 198.4 38.4 115.2 64 166.4 108.8c44.8 44.8 83.2 102.4 108.8 166.4 25.6 64 38.4 128 38.4 198.4z" fill="#409EFF" p-id="2412"></path></symbol></svg>
<!-- 3.2、引用svg -->
<!DOCTYPE html>
<html>
    <head>
        <script src="./dashboard.vue"></script>
    </head>
    <body>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <use xlink:href="#icon-dashboard"></use>
        </svg> 
    </body>
</html>
```

### vue使用iconfont

> 使用思路

1. 全局引用svg图标，减少每个页面引用操作；
2. 封装组件，减少使用的重复代码；
3. 组件全局化，方便组件使用

> 当前缺陷

1. iconfont 官网下载的svg默认未用symbol标签包裹：使用插件处理

#### 全局引用svg图标

> vue3：[vite-plugin-svg-icons](https://github.com/vbenjs/vite-plugin-svg-icons) 插件

- 安装

    ```sh
    yarn add vite-plugin-svg-icons -D
    # or
    npm i vite-plugin-svg-icons -D
    # or
    pnpm install vite-plugin-svg-icons -D
    ```

- 配置 vite.config.ts

  ```typescript
  import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
  import path from 'path'
  
  export default () => {
    return {
      plugins: [
        createSvgIconsPlugin({
          // 指定icon存放的文件夹：src/icons
          iconDirs: [path.resolve(process.cwd(), 'src/icons')],
          // Specify symbolId format
          symbolId: 'icon-[name]',
  
          /**
           * custom insert position
           * @default: body-last
           */
          inject?: 'body-last' | 'body-first'
  
          /**
           * custom dom id
           * @default: __svg__icons__dom__
           */
          customDomId: '__svg__icons__dom__',
        }),
      ],
    }
  }
  
  ```

- 注册svg图标 src/main.ts

  ```typescript
  import 'virtual:svg-icons-register'
  ```

#### 封装svg组件

- 创建文件 /src/components/SvgIcon.vue

```vue
<template>
    <svg class="svg-icon" v-bind="$attrs" :style="{color: color}">
        <use :xlink:href="iconName" rel="external nofollow"/>
    </svg>
</template>

<script setup lang="ts">
import {defineProps, computed} from "vue";

const props = defineProps({
    name: {
        type: String,
        required: true
    },
    color: {
        type: String,
        default: ''
    }
})

const iconName = computed(() => `#icon-${props.name}`);

</script>

<style scoped>
.svg-icon {
    width: 1em;
    height: 1em;
    fill: currentColor;
    vertical-align: middle;
}
</style>
```

#### 组件全局化

- 添加全局组件： src/main.ts

  ```typescript
  import {createApp} from "vue"
  import svgIcon from "@/components/SvgIcon.vue"
  
  const app = createApp(App)
  app.component('svg-icon', svgIcon)
  app.mount("#app")
  ```

- 使用示例： src/views/Dashboard.vue

  ```vue
  <template>
      <div>
          <svg-icon name="dashboard"></svg-icon>
      </div>
  </template>
  
  <script setup lang="ts">
  
  </script>
  ```

	