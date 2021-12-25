module.exports = {
    chainWebpack: config => {
        config.resolve.alias.set('vue-i18n', 'vue-i18n/dist/vue-i18n.cjs.js')
    }
}
