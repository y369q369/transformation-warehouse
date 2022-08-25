<template>
    <template v-if="isShow()">
        <template v-if="isCurrent()">
            <el-menu-item :index="info.showRoute.path" :title="info.showRoute.meta.title">
                <svg-icon :name="info.showRoute.meta.icon" style="width: 30px"></svg-icon>
                <span>{{ info.showRoute.meta.title }}</span>
            </el-menu-item>
        </template>
        <template v-else>
            <el-sub-menu :index="info.showRoute.path" :title="info.showRoute.meta.title">
                <template #title>
                    <svg-icon :name="info.showRoute.meta.icon" style="width: 30px"></svg-icon>
                    <span>{{ info.showRoute.meta.title }}</span>
                </template>
                <sidebar-item v-for="route in info.showingChildren" :key="route.path" :route="route"></sidebar-item>
            </el-sub-menu>
        </template>
    </template>
</template>

<script setup lang="ts">
import {reactive} from "vue";

const props = defineProps(['route'])

// 判断当前菜单是否显示
const isShow = () => {
    // todo 权限控制
    let hideFlag = props.route.meta && props.route.meta.hidden
    return !hideFlag
}

// 当前展示的路由
let info = reactive({
    showRoute: {},
    showingChildren: []
})

// 判断是否只展示当前
const isCurrent = () => {
    let showingChildren = []
    if (props.route.children) {
        showingChildren = props.route.children.filter((child: { meta: { hidden: boolean; }; }) => {
            return child.meta && !child.meta.hidden
        })
    }
    info.showingChildren = showingChildren

    if (showingChildren.length == 0) {
        info.showRoute = props.route
    } else if (showingChildren.length == 1) {
        info.showRoute = showingChildren[0]
    } else if (showingChildren.length > 1) {
        info.showRoute = props.route
        return false
    }

    return true
}


</script>

<style scoped>

</style>