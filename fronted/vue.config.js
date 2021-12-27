module.exports = {
    chainWebpack: config => {
        config.resolve.alias.set('vue-i18n', 'vue-i18n/dist/vue-i18n.cjs.js')
    },

    devServer: {
        open: true,                                             // 启动程序自动从浏览器打开页面
        proxy: {
            '/api': {                                        //  WC
                target: 'http://127.0.0.1:9080',
                pathRewrite:{
                    '^/api':''
                }
            },
        },
    }
}
