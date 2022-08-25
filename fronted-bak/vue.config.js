const path = require('path')

function resolve(dir) {
    return path.join(__dirname, '.', dir)
}

module.exports = {
    chainWebpack: config => {
        config.resolve.alias.set('vue-i18n', 'vue-i18n/dist/vue-i18n.cjs.js');
        config.module.rules.delete("svg"); //重点:删除默认配置中处理svg,
        config.module
            .rule('svg-sprite-loader')
            .test(/\.svg$/)
            .include
            .add(resolve('src/icons')) //处理svg目录
            .end()
            .use('svg-sprite-loader')
            .loader('svg-sprite-loader')
            .options({
                symbolId: 'icon-[name]'
            })
    },

    devServer: {
        open: true,                                             // 启动程序自动从浏览器打开页面
        proxy: {
            '/api': {                                        //  WC
                target: 'http://127.0.0.1:9080',
                pathRewrite: {
                    '^/api': ''
                }
            },
        },
    }
}
