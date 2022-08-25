<template>
    <a-row style="padding-bottom: 20px">
        <a-col style="width: 600px">
            <a-input-search
                v-model:value="searchUrl"
                @search="searchSource"
                enter-button
                :placeholder="$t('placeholder.tencent.search')"/>
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

    <a-row style="height: 235px; margin-bottom: 20px; border: 1px solid rgb(136, 198, 229)"
           v-show="data.info.title != ''">
        <a-col style="width: 170px; height: 230px; padding: 10px; background-color: #f8f5f5;">
            <a-image style="width: 150px; height: 210px" :src="data.info.picUrl"/>
        </a-col>
        <a-col style="padding: 0 20px; width: calc(99% - 170px); height: 180px; line-height: 32px">
            <a-row class="title" style="padding-top: 20px; ">
                <a-col :span="18">
                    {{ data.info.title }}
                </a-col>
                <a-col :span="6" style="text-align: right">
                    <Download type="video" source="tencent" :name="data.info.title" :urls="data.chooseItems"></Download>
                </a-col>
            </a-row>
            <a-col class="info">
                <span>{{ data.info.type }}</span>
                <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                <span>{{ data.info.secondTitle }}</span>
            </a-col>
            <a-col class="intro" :title="data.info.description">
                {{ data.info.description }}
            </a-col>
        </a-col>
    </a-row>

    <multiple-choice :show-items="data.info.videos" @chooseItems="handleChoose"
                     ref="multipleChoiceRef"></multiple-choice>
</template>

<script setup>
import {ref, reactive} from "vue";
import api from "@/http/api";
import http from "@/http";
import MultipleChoice from "@/components/MultipleChoice";
import Download from '@/components/Download'

let videoType = ref('tv')
let searchUrl = ref('')

let data = reactive({
    info: {
        title: '',
        secondTitle: '',
        picUrl: '',
        description: '',
        type: '',
        videos: [],
        definitions: ''
    },
    chooseItems: []
})

const multipleChoiceRef = ref();

// 搜索视频
const searchSource = () => {
    if (searchUrl.value) {
        http.get(api.video.search('tencent', videoType.value, searchUrl.value)).then(response => {
            data.info = response
        })
    }
}

const handleChoose = (chooseItems) => {
    data.chooseItems = chooseItems
}

</script>

<style lang="sass" scoped>
.column
    text-align: center
    line-height: 40px

</style>
