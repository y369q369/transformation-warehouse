export default {
    // 小说相关接口
    novel: {
        search:  function(source, novelName) {                                          // 搜索小说
            return '/api/novel/' + source + '/search/' + novelName
        },
        catalog:  function(source, url) {                                               // 搜索小说目录
            return '/api/novel/' + source + '/catalog?url=' + url
        },
        download:  function(source, url, fileName) {                                    // 下载小说
            return '/api/novel/' + source + '/download?url=' + url + "&fileName=" + fileName
        }
    },
    video: {
        search:  function(source, videoType, searchUrl) {                                          // 搜索小说
            return '/api/video/' + source + '/search/' + videoType + '?url=' + searchUrl
        },
    }
}
