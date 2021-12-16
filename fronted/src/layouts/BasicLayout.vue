<template>
    <a-row class="layout">
        <a-col class="side-container">
            <side-bar></side-bar>
        </a-col>
        <a-col class="main-container">
            <router-view />
        </a-col>
    </a-row>

</template>

<script>
    import SideBar from "@/layouts/SideBar";

    export default {
        name: "BasicLayout",
        components: {
            SideBar,
        }
    }
</script>

<style scoped lang="sass">
.layout
    height: 100%

    .side-container
        width: 210px
        height: 100%
        background: #001529

    .main-container
        width: calc(100% - 210px)
        min-height: 100%
        background: aliceblue

</style>
