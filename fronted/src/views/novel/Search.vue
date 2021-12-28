<template>
    <a-row>
        <a-row v-for="result in data.searchResults" :key="result.bookUrl" class = "book">
            <a-col class = "pic">
                <a-image
                    :src="result.picUrl"
                />
            </a-col>

            <a-col class = "detail">
                <a-col>
                    <a :href="result.url" target="_blank" class="title">
                        {{ result.name }}
                    </a>
                </a-col>
                <a-col class="info">
                    <span>{{ result.author }}&nbsp;&nbsp;&nbsp;</span>
                    <span>|&nbsp;&nbsp;&nbsp;{{ result.type }}&nbsp;&nbsp;&nbsp;</span>
                    <span v-show="bookSource === 'qiDian'">|&nbsp;&nbsp;&nbsp;{{ result.status }}&nbsp;&nbsp;&nbsp;</span>
                    <span>|&nbsp;&nbsp;&nbsp;{{ result.newChapter }}&nbsp;·&nbsp;&nbsp;&nbsp;{{ result.updateTime }}</span>

                </a-col>
                <a-col class="intro" :title="result.description">
                    {{ result.description }}
                </a-col>
            </a-col>

            <a-col class = "operation">
                <a-button type="primary" :title="$t('novel.categories')" @click="queryCatalog(result.url)">
                    <template #icon>
                        <folder-view-outlined />
                    </template>
                </a-button>
                <a-button type="primary" :title="$t('novel.download')" @click="download(result.url)">
                    <template #icon>
                        <DownloadOutlined />
                    </template>
                </a-button>
            </a-col>
        </a-row>
    </a-row>
</template>

<script setup>
    import { reactive, ref, defineExpose } from 'vue'
    import api from "@/http/api";
    import http from "@/http";

    let data = reactive({
        searchResults: []
    })

    let bookSource = ref('')

    const searchBook = (source, name) => {
        bookSource.value = source
        http.get(api.novel.search(source, name)).then(response => {
            data.searchResults = response;
        })
    }

    // 将方法暴露出去，供外部访问
    defineExpose({
        searchBook
    })

    // 查看目录
    const queryCatalog = (url) => {
        console.log(url)
    }

    // 查看目录
    const download = (url) => {
        console.log(url)
    }

</script>

<style lang="sass">
.book
    width: 100%
    height: 200px
    padding-top: 25px
    border-top: 1px solid #e6e6e6

    .pic
        width: 140px
        height: 150px

    .detail
        width: 70%
        height: 120px
        line-height: 32px

        .title
            font-size: 18px
            font-weight: bold

        .info
            font-size: 12px
            color: #a6a6a6

        .intro
            font-size: 14px
            line-height: 24px
            overflow: hidden
            text-overflow: ellipsis
            display: -webkit-box
            -webkit-line-clamp: 3
            -webkit-box-orient: vertical
            height: 72px
            margin-bottom: 8px
            color: #666

    .operation
        width: calc(100% - 70% - 140px)
        text-align: right

        .ant-btn
            margin-right: 5px

.ant-image
    .ant-image-img
        height: 150px
        width: 120px
</style>
