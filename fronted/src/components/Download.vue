<template>
    <a-popconfirm
        :title="$t('tips.downloadTips')"
        :ok-text="$t('tips.sure')"
        :cancel-text="$t('tips.cancel')"
        @confirm="download"
    >
        <a-button type="primary" :title="$t('tips.download')" size="small">
            <template #icon>
                <DownloadOutlined />
            </template>
        </a-button>
    </a-popconfirm>

</template>

<script setup>
    import {notification } from "ant-design-vue";
    import i18n from "@/locales";
    import api from "@/http/api";
    import http from "@/http";
    import { defineProps } from "vue"

    const props = defineProps({
        // 接口下载类型： novel, video...
        type: {
            type: String
        },
        // 下载源： tencent
        source: {
            type: String
        },
        // 视频类型
        videoType: {
            type: String
        },
        // 下载名称
        name: {
            type: String
        },
        // 下载链接数组
        urls: {
            type: Array
        }
    })

    const download = () => {
        if (props.urls.length > 0) {
            let req = {
                name: props.name,
                urls: props.urls
            }
            http.post(api.video.download('tencent', props.videoType), {}, req).then(response => {
                let type = 'error'
                let status = i18n.global.t('tips.failDownload')
                if (response.code === 0) {
                    type = 'info'
                    status = i18n.global.t('tips.finishDownload')
                }
                notification[type]({
                    message: i18n.global.t('tips.downloadVideo'),
                    description: req.name + "  " + status,
                    duration: 5
                })
            })
        } else {
            notification.error({
                message: i18n.global.t('tips.downloadVideo'),
                description: i18n.global.t('tips.notChoose'),
                duration: 5
            })
        }

    }


</script>

<style scoped>

</style>
