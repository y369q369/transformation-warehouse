<template>
    <a-row style="padding-bottom: 20px">
        <a-col style="width: 300px">
            <a-input-search
                v-model:value="searchUrl"
                @search="searchSource"
                enter-button
                :placeholder="$t('placeholder.tencent.search')" />
        </a-col>

        <a-col style="text-align: right; width: calc(100% - 300px)">
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

    <a-row>
        {{ title }}
    </a-row>
</template>

<script setup>
import {ref} from "vue";
import api from "@/http/api";
import http from "@/http";

let videoType = ref('tv')
let searchUrl = ref('')
let title = ref('')

// 搜索视频
const searchSource = ()=>{
    if (searchUrl.value) {
        http.get(api.video.search('tencent', videoType.value, searchUrl.value)).then(response => {
            console.log(response)
            title.value = response.title
        })
    }
}
</script>

<style scoped>

</style>
