<template>
    <a-button type="primary" :title="$t('novel.download')" @click="download()" size="small">
        <template #icon>
            <DownloadOutlined/>
        </template>
    </a-button>
</template>

<script>
import {notification} from "ant-design-vue";
import i18n from "@/locales";
import api from "@/http/api";
import {defineComponent} from "vue"

export default defineComponent({
    props: {
        source: {
            type: String
        },
        book: {
            type: Object
        }
    },
    setup(props) {
        const download = () => {
            notification.info({
                message: i18n.global.t('tips.downloadNovel'),
                description: props.book.name + "  " + i18n.global.t('tips.isDownloading'),
                duration: 0
            })
            window.location.href = api.novel.download(props.source, props.book.url, props.book.name + ' - ' + props.book.author + '.txt')
        }
        return {download}
    }
})
</script>

<style scoped>

</style>
