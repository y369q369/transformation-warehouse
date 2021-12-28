export default {
    // 小说相关接口
    novel: {
        search:  function(source, novelName) {                                        // 搜索小说
            return '/api/novel/' + source + '/search/' + novelName
        },
        catalog:  function(source, novelName) {                                        // 搜索小说目录
            return '/api/novel/' + source + '/catalog/' + novelName
        },
        download:  function(source, novelName) {                                        // 下载小说
            return '/api/novel/' + source + '/download/' + novelName
        }
    }
}
