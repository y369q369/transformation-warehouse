<template>
    <div style="float: left; height: 100%; background: #151f29; color: #ffffff" :style="{ width: width + 'px' }">
        <Sidebar></Sidebar>
    </div>
    <div style="float: left; height: 100%; " :style="{ width: 'calc(100% - ' + width + 'px)' }">
        <Navbar></Navbar>
        <div style="padding: 20px; height: calc(100% - 90px)">
            <router-view/>
        </div>
    </div>
</template>

<script setup lang="ts">
import Sidebar from "./Sidebar.vue";
import Navbar from "./Navbar.vue";
import {computed} from "vue";
import {localStore} from "@/stores/local";

const store = localStore()

const translateRight = store.sidebarShowFlag ? 0 : 145;
const width = computed(() => {

    return store.sidebarShowFlag ? 210 : 65;
})

</script>

<style scoped>

</style>