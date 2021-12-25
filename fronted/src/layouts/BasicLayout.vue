<template>
    <a-row class="layout">
        <a-col class="side-container">
            <side-bar></side-bar>
        </a-col>
        <a-col class="main-container">
            <page-header></page-header>

            <Test></Test>

            <router-view />
        </a-col>
    </a-row>

</template>

<script>
    import SideBar from '@/layouts/SideBar'
    import PageHeader from "@/layouts/PageHeader";
    import Test from '@/layouts/Test'

    export default {
        name: "BasicLayout",
        components: {
            SideBar,
            PageHeader,
            Test
        }
    }
</script>

<style lang="sass">
.layout
    height: 100%

    .side-container
        width: 210px
        height: 100%
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
</style>
