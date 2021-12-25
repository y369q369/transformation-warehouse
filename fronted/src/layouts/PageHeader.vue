<template>
    <a-col class="header">
        <a-col style="text-align: right;">
            <a-dropdown>
                <a class="dropdown" @click.prevent>
                    <translation-outlined />
                </a>
                <template #overlay>
                    <a-menu>
                        <a-menu-item @click="changeLang('zhCn')">
                            <i class="language_r" :class="{choose: lang === 'zhCn'}"></i> 中文
                        </a-menu-item>
                        <a-menu-item @click="changeLang('enUS')">
                            <i class="language_r" :class="{choose: lang === 'enUS'}"></i> English
                        </a-menu-item>
                    </a-menu>
                </template>
            </a-dropdown>

<!--            <a-select-->
<!--                v-model:value="lang"-->
<!--                ref="select"-->
<!--                @change="changeLang"-->
<!--            >,-->
<!--                <a-select-option value="zhCn">中文</a-select-option>-->
<!--                <a-select-option value="enUS">English</a-select-option>-->
<!--            </a-select>-->
        </a-col>
    </a-col>
</template>

<script>
import { useI18n } from 'vue-i18n'

const {reactive} = require("vue");

export default {
    name: "PageHeader",
    setup(){
        const { locale } = useI18n()
        // 获取语言
        // let lang = locale.value
        let lang = reactive(locale.value)
        console.log(lang)
        //语言切换
        const changeLang = (value)=>{
            //切换语言 值要对应上面index中导出的名字  要一致  第四步
            locale.value = value
            lang = value
            // console.log(value)
            // console.log(locale.value)
            console.log(lang)
            //缓存到localStorage中下次进来还是切换后的语言  如果不需要可以删除下面代码
            // localStorage.setItem('lang', "cn")
        }
        return {
            changeLang,
            lang
        }
    },
    data() {
        return {
            // lang: ''
        }
    },
    methods: {
        // changeLang(value) {
            //切换语言 值要对应上面index中导出的名字  要一致  第四步
            // locale.value = value
            // lang = value
            // console.log(value)
            // console.log(locale.value)
            //缓存到localStorage中下次进来还是切换后的语言  如果不需要可以删除下面代码
            // localStorage.setItem('lang', "cn")
        // }
    }
}
</script>

<style lang="sass">
.header
    height: 50px
    line-height: 50px
    border-bottom: 1px solid #f0f0f0
    padding-left: 30px
    padding-right: 30px
    margin-bottom: 20px

.dropdown
    padding: 5px
    &:hover
        border: 1px solid #409EFF

.choose
    background: #409EFF
    border-color: #409EFF

.language_r
    width: 10px
    height: 10px
    border-radius: 50%
    border: 1px solid #999
    margin-right: 10px !important
    display: inline-block
    //background: saddlebrown
</style>
