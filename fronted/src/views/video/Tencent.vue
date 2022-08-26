<template>
    <el-row>
        <el-col :span="11" style="padding-bottom: 20px; line-height: 40px">
            <el-input v-model="url" @change="searchVideoInfo" placeholder="请输入视频地址"/>
        </el-col>
        <el-col :span="13" style="text-align: right; padding-right: 20px">
            <el-button icon="Search" title="搜索" @click="searchVideoInfo">搜索</el-button>
            <el-button type="primary" icon="Download" title="下载" @click="download">下载</el-button>
        </el-col>
    </el-row>


    <!--    <el-row v-show="data.info.definitions.length > 0">-->
    <el-row style="margin-bottom: 10px" v-show="data.info.type !== ''">
        <el-col>
            <el-button type="primary" link style="margin-right: 30px">{{ data.info.type }}</el-button>

            <el-select v-model="downloadParam.definition" class="m-2">
                <el-option
                    v-for="item in data.info.definitions"
                    :key="item.name"
                    :label="item.cname"
                    :value="item.name"
                />
            </el-select>

            <el-button-group style="margin-left: 30px">
                <el-button @click="chooseVideos(true)">全选</el-button>
                <el-button @click="chooseVideos(false)">全不选</el-button>
            </el-button-group>
        </el-col>
    </el-row>

    <!--  电影选择框  -->
    <el-row v-show="data.info.type === '电影'" v-for="(video, index) in data.info.videos" :key="video.url"
            style="border: 1px solid gainsboro; border-radius: 4px; margin-bottom: 10px">
        <el-col :span="4" style="height: 120px;">
            <el-image style="height: 100px; border-radius: 8px; margin-top: 10px; margin-left: 5px; float: right"
                      fit="cover"
                      :src="video.imageUrl"/>
        </el-col>
        <el-col :offset="1" :span="18" style="padding: 10px;">
            <el-col style=" padding-bottom: 5px; line-height: 30px">
                <a :href="video.url" target="_blank">{{ video.title }}</a>
            </el-col>
            <el-col style="padding-bottom: 5px; line-height: 20px; font-size: 13px">
                <span>{{ data.info.type }}</span>
                <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                <span>{{ data.info.secondTitle }}</span>
            </el-col>
            <el-col class="intro" style="line-height: 20px; font-size: 12px" :title="data.info.description">
                {{ data.info.description }}
            </el-col>
        </el-col>
        <el-col :span="1">
            <div @click="chooseVideo(index)" :class="data.chooseItems.indexOf(index) > -1 ? 'is-choice' : 'not-choice'"
                 class="choice-box">
                √
            </div>
        </el-col>
    </el-row>

    <!--  其他类型选择框  -->
    <div v-show="data.info.type && data.info.type !== '电影'">
        <el-row style="border: 1px solid gainsboro; border-radius: 4px; margin: 10px 10px 20px; padding: 10px 20px">
            <el-col :span="4" style="height: 120px;">
                <el-image style="height: 100px; border-radius: 8px; margin-top: 10px; margin-left: 5px; " fit="cover"
                          :src="data.info.picUrl"/>
            </el-col>
            <el-col :span="19" style="padding: 10px; margin-left: 10px">
                <el-col style=" padding-bottom: 5px; line-height: 30px">
                    <a>{{ data.info.title }}</a>
                </el-col>
                <el-col style="padding-bottom: 5px; line-height: 20px; font-size: 13px">
                    <span>{{ data.info.type }}</span>
                    <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                    <span>{{ data.info.secondTitle }}</span>
                </el-col>
                <el-col class="intro" style="line-height: 20px; font-size: 12px" :title="data.info.description">
                    {{ data.info.description }}
                </el-col>
            </el-col>
        </el-row>

        <el-row style="border: 1px solid gainsboro; border-radius: 4px;padding: 20px 0; margin: 0 10px">
            <el-col :span="2" v-for="(video, index) in data.info.videos"
                    style="border: 1px solid #eae6e6; margin: 5px 2%; line-height: 40px; height: 40px">
                <div style="width: calc(100% - 35px); text-align: center; float: left" :title="video.url">
                    {{ video.title }}
                </div>
                <div @click="chooseVideo(index)"
                     :class="data.chooseItems.indexOf(index) > -1 ? 'is-choice' : 'not-choice'" class="choice-box">
                    √
                </div>
            </el-col>
        </el-row>
    </div>

</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import axios from "@/plugins/axios";
import {ElNotification} from "element-plus";

let url = ref<string>('')

let data = reactive({
    info: {
        title: '',
        secondTitle: '',
        picUrl: '',
        description: '',
        type: '',
        videos: [],
        definitions: []
    },
    chooseItems: <number[]>[]
})


const searchVideoInfo = () => {
    axios.get('/api/video/tencent/searchVideo', {
        params: {
            url: url.value
        }
    }).then(response => {
        data.info = response
        downloadParam.name = response.title
        downloadParam.definition = response.definitions[response.definitions.length - 1].name
        data.chooseItems = []
    })
}

const chooseVideos = (flag: boolean) => {
    if (flag) {
        data.info.videos.forEach((item, index) => {
            data.chooseItems.push(index)
        })
    } else {
        data.chooseItems = []
    }
}

const chooseVideo = (index: number) => {
    let i = data.chooseItems.indexOf(index)
    if (i > -1) {
        data.chooseItems.splice(i, 1)
    } else {
        data.chooseItems.push(index)
    }
}

const downloadParam = reactive({
    name: '',
    definition: '',
    urls: <string[]>[],
})

const download = () => {
    if (downloadParam.definition && data.chooseItems.length > 0) {
        data.chooseItems.sort()
        downloadParam.urls = []
        let title = data.info.title + '   '
        data.chooseItems.forEach(index => {
            downloadParam.urls.push(data.info.videos[index].url)
            title += data.info.videos[index].title + '    '
        })

        axios.post('/api//video/tencent/download', downloadParam)
            .then(response => {
                let message = title + '下载完成'
                let type = 'success'
                if (response.code !== 200) {
                    message = response.msg
                    type = 'error'
                }

                ElNotification({
                    title: '下载视频',
                    message: message,
                    duration: 0,
                    type: type,
                })
            })
    } else {
        ElNotification({
            title: '下载视频',
            message: '请选择清晰度和下载的视频',
            type: 'error',
        })
    }
}


</script>

<style>
.intro {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    color: #666;
}

.choice-box {
    background: #409EFF;
    width: 35px;
    line-height: 20px;
    height: 20px;
    text-align: center;
    float: right;
    border-radius: 4px;
    cursor: pointer;
}

.not-choice {
    background: #eae6e6;
    color: white
}

.is-choice {
    background: #c7cb4c;
    color: #807500
}



</style>
