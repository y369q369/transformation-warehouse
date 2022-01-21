<template>
    <a-row style="padding-bottom: 20px">
        <a-col style="width: 600px">
            <a-input-search
                v-model:value="searchUrl"
                @search="searchSource"
                enter-button
                :placeholder="$t('placeholder.tencent.search')" />
        </a-col>

        <a-col style="text-align: right; width: calc(100% - 600px)">
            <a-select
                ref="select"
                @change="searchSource"
                v-model:value="videoType"
            >
                <a-select-option value="tv">{{ $t('video.type.tv') }}</a-select-option>
                <a-select-option value="movie">{{ $t('video.type.movie') }}</a-select-option>
                <a-select-option value="variety">{{ $t('video.type.variety') }}</a-select-option>
            </a-select>
        </a-col>
    </a-row>

    <a-row style = "height: 190px; border: 1px solid rgb(136, 198, 229)" v-show="data.info.title != ''">
        <a-col style="width: 150px; height: 180px; padding: 15px; background-color: #f8f5f5;">
            <a-image style="width: 120px; height: 150px" :src="data.info.picUrl"/>
        </a-col>
        <a-col style="padding: 0 20px; width: calc(100% - 200px); height: 180px; line-height: 32px">
            <a-row class="title" style="padding-top: 20px; ">
                <a-col :span="18">
                    {{data.info.title}}
                </a-col>
                <a-col :span="6" style="text-align: right">
                    <a-button type="primary" :title="$t('novel.download')" @click="download()" size="small">
                        <template #icon>
                            <DownloadOutlined />
                        </template>
                    </a-button>
                </a-col>
            </a-row>
            <a-col class="info">
                <span>{{data.info.type}}</span>
                <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                <span>{{data.info.secondTitle}}</span>
            </a-col>
            <a-col class="intro" :title="data.info.description">
                {{data.info.description}}
            </a-col>
        </a-col>
    </a-row>

    <a-row style = "margin-top: 20px; border: 1px solid rgb(136, 198, 229)" v-show="data.info.title != ''">
        <a-col :span="4" v-for="(video, index) in data.info.videos" :key="index" class="column">
            <a :href="video" target="_blank">{{ index + 1 }}</a>
        </a-col>
    </a-row>
</template>

<script setup>
import {ref, reactive} from "vue";
import api from "@/http/api";
import http from "@/http";
import {notification} from "ant-design-vue";
import i18n from "@/locales";

let videoType = ref('tv')
let searchUrl = ref('')

let data = reactive({
    info: {
        title: '',
        secondTitle: '',
        picUrl: '',
        description: '',
        type: '',
        videos: '',
        definitions: ''
    }
})

// 搜索视频
const searchSource = ()=>{
    if (searchUrl.value) {
        http.get(api.video.search('tencent', videoType.value, searchUrl.value)).then(response => {
            data.info = response
        })
    }
}

const download = ()=>{
    let req = {
        name: data.info.title,
        urls: [data.info.videos]
    }
    http.post(api.video.download('tencent', videoType.value), {}, req).then(response => {
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
}

</script>

<style lang="sass" scoped>
.column
    text-align: center
    line-height: 40px

</style>
