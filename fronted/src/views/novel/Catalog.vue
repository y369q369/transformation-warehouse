<template>
    <a-row>

    </a-row>
</template>

<script setup>
    import { reactive, ref, defineExpose } from 'vue'
    import api from "@/http/api";
    import http from "@/http";

    let data = reactive({
        catalogs: []
    })

    let bookSource = ref('')

    const searchCatalog = (source, url) => {
        bookSource.value = source
        http.get(api.novel.catalog(source, url)).then(response => {
            data.catalogs = response;
        })
    }

    // 将方法暴露出去，供外部访问
    defineExpose({
        searchCatalog
    })
</script>

<style scoped>

</style>
