export default {
    // 小说相关接口
    novel: {
        search:  function(type, novelName) {                                        // 搜索小说
            return '/api/novel/' + type + '/' + novelName
        }
    }
}
