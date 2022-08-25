<template>
    <el-row style="background: #c9c4c4; line-height: 50px; padding: 0 20px">
        <el-col :span="12">
            <span @click="switchStatus()" style="cursor: pointer">
                <svg-icon v-show="sidebarShowFlag" name="sidebar-hide"></svg-icon>
                <svg-icon v-show="!sidebarShowFlag" name="sidebar-show"></svg-icon>
            </span>
        </el-col>
        <!--        <el-col :span="12" style="text-align: right; padding-right: 30px">{{ user.name }}</el-col>-->
    </el-row>
</template>

<script setup lang="ts">
import {localStore} from "@/stores/local";
import SvgIcon from "@/components/SvgIcon.vue";
import {ref} from "vue";

const store = localStore()
// const user = store.user
const sidebarShowFlag = ref<boolean>(store.sidebarShowFlag)


const switchStatus = () => {
    store.storeSidebar(!sidebarShowFlag.value)
    sidebarShowFlag.value = !sidebarShowFlag.value
}

</script>

<style scoped>

</style>