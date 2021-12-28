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

    <Search ref="childRef"></Search>
</template>

<script setup>
    import {ref} from "vue";
    import Search from "@/views/novel/Search"

    let novel_source = ref('biQuGe')
    let searchContent = ref('')
    const childRef = ref();

    // 搜索小说
    const searchNovel = ()=>{
        if (searchContent.value) {
            childRef.value.searchBook(novel_source.value, searchContent.value)
        }
    }
</script>

<style scoped>

</style>
