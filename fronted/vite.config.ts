import {fileURLToPath, URL} from "node:url";
import {createSvgIconsPlugin} from 'vite-plugin-svg-icons'
import path from 'path'
import {defineConfig} from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue(), vueJsx(),
        createSvgIconsPlugin({
            // 指定需要缓存的图标文件夹
            iconDirs: [path.resolve(process.cwd(), 'src/assets/icons/iconfont')],
            // 指定symbolId格式
            symbolId: 'icon-[name]',

            /**
             * 自定义插入位置
             * @default: body-last
             */
            // inject?: 'body-last' | 'body-first'

            /**
             * custom dom id
             * @default: __svg__icons__dom__
             */
            customDomId: 'svgIconsDom',
        })
    ],
    server: {
        port: 8701,
        open: '/',
        proxy: {
            '/api': {
                target: 'http://localhost:8282/business',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    },
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
});
