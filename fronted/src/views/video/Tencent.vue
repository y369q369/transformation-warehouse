<template>
    <div style="padding-bottom: 20px; height: 40px">
        <div style="line-height: 40px; width: 40%">
            <el-input v-model="url" @change="searchVideoInfo()" placeholder="请输入视频地址"/>
        </div>
    </div>


    <!--    <el-row style="height: 235px; margin-bottom: 20px; border: 1px solid rgb(136, 198, 229)"-->
    <!--            v-show="data.info.title">-->
    <div>
        <div style="width: 280px; height: 140px; padding: 10px; float: left">
            <el-image style="width: 250px; height: 140px" fit="cover"
                      src="http://puui.qpic.cn/vcover_hz_pic/0/mzc00200m8u46sg1655802451971/0"/>
        </div>
        <div style="width: calc(100% - 300px); height: 160px; padding: 10px; float: left">
            反贪风暴5：最终章(普通话版)
        </div>
    </div>


    <!--        <el-col style="padding: 0 20px; width: calc(99% - 170px); height: 180px; line-height: 32px">-->
    <!--            <el-col class="title" style="padding-top: 20px; ">-->
    <!--                <el-col :span="18">-->
    <!--                    反贪风暴5：最终章(普通话版)-->
    <!--                </el-col>-->
    <!--&lt;!&ndash;                <el-col :span="6" style="text-align: right">&ndash;&gt;-->
    <!--&lt;!&ndash;                    <Download type="video" source="tencent" :name="data.info.title" :urls="data.chooseItems"></Download>&ndash;&gt;-->
    <!--&lt;!&ndash;                </el-col>&ndash;&gt;-->
    <!--            </el-col>-->
    <!--            <el-col class="info">-->
    <!--                <span>{{ 电影 }}</span>-->
    <!--                <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>-->
    <!--                <span>{{ sfas }}</span>-->
    <!--            </el-col>-->
    <!--            <el-col class="intro" >-->
    <!--                影片讲述了ICAC首席调查主任陆志廉与总调查主任程德明共同调查走私贪污案，意外发现另一起涉及人口贩卖的海关贪腐大案，案情迷雾重重牵涉多名海关高层领导。-->
    <!--            </el-col>-->
    <!--        </el-col>-->

    <!--        <el-col style="width: 170px; height: 230px; padding: 10px; background-color: #f8f5f5;">-->
    <!--            <el-image style="width: 150px; height: 210px" :src="data.info.picUrl"/>-->
    <!--        </el-col>-->
    <!--        <el-col style="padding: 0 20px; width: calc(99% - 170px); height: 180px; line-height: 32px">-->
    <!--            <el-row class="title" style="padding-top: 20px; ">-->
    <!--                <el-col :span="18">-->
    <!--                    {{ data.info.title }}-->
    <!--                </el-col>-->
    <!--                <el-col :span="6" style="text-align: right">-->
    <!--                    <Download type="video" source="tencent" :name="data.info.title" :urls="data.chooseItems"></Download>-->
    <!--                </el-col>-->
    <!--            </el-row>-->
    <!--            <el-col class="info">-->
    <!--                <span>{{ data.info.type }}</span>-->
    <!--                <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>-->
    <!--                <span>{{ data.info.secondTitle }}</span>-->
    <!--            </el-col>-->
    <!--            <el-col class="intro" :title="data.info.description">-->
    <!--                {{ data.info.description }}-->
    <!--            </el-col>-->
    <!--        </el-col>-->

</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import axios from "@/plugins/axios";

let videoType = ref('tv')
let url = ref<string>('https://v.qq.com/x/cover/mzc00200m8u46sg/x004391msci.html')

let data = reactive({
    info: {
        title: '',
        secondTitle: '',
        picUrl: '',
        description: '',
        type: '',
        videos: [],
        definitions: ''
    },
    chooseItems: []
})


const searchVideoInfo = () => {
    axios.get('/api/video/tencent/searchVideo', {
        params: {
            url: url.value
        }
    }).then(response => {
        data.info = response
    })
}

// searchVideoInfo()


</script>

<style>

</style>
