<template>
    <a-row style="padding-bottom: 20px">
        <a-col style="width: 300px">
            <a-input-search
                v-model:value="searchContent"
                @search="searchNovel"
                enter-button
                :placeholder="$t('placeholder.novel')" />
        </a-col>

        <a-col style="text-align: right; width: calc(100% - 300px)">
            <a-select
                ref="select"
                v-model:value="novel_source"
            >
                <a-select-option value="biQuGe">{{ $t('website.biQuGe') }}</a-select-option>
                <a-select-option value="qiDian">{{ $t('website.qiDian') }}</a-select-option>
            </a-select>
        </a-col>
    </a-row>

    <Seach></Seach>
</template>

<script setup>
    import {ref} from "vue";
    import Seach from "@/views/novel/Seach";
    import api from "@/http/api";
    import http from "@/http";

    let novel_source = ref('biQuGe')
    let searchContent = ref('')


    // 搜索小说
    const searchNovel = ()=>{
        if (searchContent.value) {
            http.get(api.novel.search(novel_source.value, searchContent.value)).then(response => {
                console.log(response)
            })
        }

    }
</script>

<style scoped>

</style>
