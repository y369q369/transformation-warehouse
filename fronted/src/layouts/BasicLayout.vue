<template>
    <a-row class="layout">
        <a-col class="side-container">
            <side-bar></side-bar>
        </a-col>
        <a-col class="main-container">
            <page-header></page-header>

            <a-col class="body-container">
                <router-view />
            </a-col>
        </a-col>
    </a-row>

</template>

<script>
    import SideBar from '@/layouts/SideBar'
    import PageHeader from "@/layouts/PageHeader";

    export default {
        name: "BasicLayout",
        components: {
            SideBar,
            PageHeader,
        }
    }
</script>

<style lang="sass">
.layout
    height: 100%

    .side-container
        width: 210px
        min-height: 100%
        background: #001529

        .ant-menu-item
            span
                color: #fff

        .ant-menu-submenu
            span
                color: #fff

        .ant-menu-item-selected
            span
                color: #18ff8c

    .main-container
        width: calc(100% - 210px)
        min-height: 100%
        background: aliceblue
        padding: 0 20px 20px 20px

        .body-container
            box-shadow: 0 1px 4px rgba(0, 21, 41, .08)
            min-height: calc(100vh - 90px)
            padding: 10px 20px

</style>
