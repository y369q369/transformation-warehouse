<template>
    <a-row style = "height: 190px; border: 1px solid rgb(136, 198, 229)">
        <a-col style="width: 150px; height: 180px; padding: 15px; background-color: #f8f5f5;">
            <a-image style="width: 120px; height: 150px" :src="bookInfo.book.picUrl"/>
        </a-col>
        <a-col style="padding: 0 20px; width: calc(100% - 200px); height: 180px">
            <a-row style="font-size: 26px; font-weight: bold; height: 50px; line-height: 40px">
                <a-col :span="18">
                    {{ bookInfo.book.name }}
                </a-col>
                <a-col :span="6" style="text-align: right">
                    <download-novel :source="bookInfo.source" :book="bookInfo.book"></download-novel>
                </a-col>
            </a-row>
            <a-row style="height: 25px">
                <a-col :span="12">
                    <i>作&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;者：</i>
                    <span>{{ bookInfo.book.author }}</span>
                </a-col>
                <a-col :span="12">
                    <i>状&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;态：</i>
                    <span>{{ bookInfo.book.author }}</span>
                </a-col>
            </a-row>
            <a-row style="height: 25px;">
                <a-col :span="12">
                    <i>最后更新：</i>
                    <span>{{ bookInfo.book.updateTime }}</span>
                </a-col>
                <a-col :span="12">
                    <i>最后章节：</i>
                    <span>{{ bookInfo.book.newChapter }}</span>
                </a-col>
            </a-row>
            <a-row class="intro">
                {{ bookInfo.book.description }}
            </a-row>
        </a-col>
    </a-row>
    <a-row style = "margin-top: 20px; padding: 20px; border: 1px solid rgb(136, 198, 229)">
        <a-col :span="8" v-for="datalog in data.catalogs" :key="datalog.index" class = "chapter">
            <a :href="datalog.url">{{ datalog.name }}</a>
        </a-col>
    </a-row>

</template>

<script setup>
    import { reactive, onBeforeMount } from 'vue'
    import api from "@/http/api";
    import http from "@/http";
    import { useRoute } from 'vue-router';
    import DownloadNovel from '@/views/novel/DownloadNovel';

    onBeforeMount(() => {
        searchCatalog()
    })

    let data = reactive({
        catalogs: []
    })

    const route = useRoute();
    const bookInfo = JSON.parse(decodeURI(window.atob(route.query.info)))

    const searchCatalog = () => {
        http.get(api.novel.catalog(bookInfo.source, bookInfo.book.url)).then(response => {
            data.catalogs = response;
        })
    }
</script>

<style lang="sass" scoped>
.intro
    padding-top: 9px
    text-indent: 2em
    border-top: 1px dashed rgb(136, 198, 229)
    height: 81px
    line-height: 24px
    overflow: hidden
    text-overflow: ellipsis
    display: -webkit-box
    -webkit-line-clamp: 3
    -webkit-box-orient: vertical

.chapter
    border-bottom: 1px dashed rgb(204, 204, 204)
    display: inline
    float: left
    height: 30px
    line-height: 200%
    font-size: 13px
    margin-bottom: 5px
    overflow: hidden
    text-align: left
    text-indent: 10px
    vertical-align: middle
</style>
