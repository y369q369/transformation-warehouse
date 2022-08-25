import zhCn from './lang/zh-cn'
import enUS from './lang/en-US';
import {createI18n} from 'vue-i18n'

const i18n = createI18n({
    locale: 'zhCn',
    messages: {
        zhCn,
        enUS,
    }
})

export default i18n
