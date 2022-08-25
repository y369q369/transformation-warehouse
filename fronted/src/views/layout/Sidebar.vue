<template>
    <el-menu
        active-text-color="#ffd04b"
        background-color="#151f29"
        class="el-menu-vertical-demo"
        text-color="#fff"
        router
        :collapse="isCollapse"
        :collapse-transition=transition
    >
        <sidebar-item v-for="route in routes" :key="route.path" :route="route"></sidebar-item>
    </el-menu>
</template>

<script setup lang="ts">
import SidebarItem from "@/views/layout/SidebarItem.vue";
import {useRouter} from "vue-router";
import {computed, ref} from "vue";
import {localStore} from "@/stores/local";

const routes = useRouter().options.routes

const transition = ref(false)

const store = localStore()

const isCollapse = computed(() => {
    return !store.sidebarShowFlag
})


</script>

<style scoped>
.el-menu {
    border-right: none
}
</style>