import cn from './cn'
import en from './en';
import { createI18n } from 'vue-i18n'

declare const language: ()=> createI18n({
    locale: 'en',
    messages: {
        cn: cn,
        en: en,
    }
})

export default language
