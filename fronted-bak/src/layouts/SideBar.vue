<template>
    <a-menu
        v-model:openKeys="openKeys"
        mode="inline"
        theme="dark"
        :inline-collapsed="collapsed"
        @click="handleClick"
    >
        <side-bar-menu v-for="route in routes" :key="route.path" :menu="route"></side-bar-menu>
    </a-menu>
</template>

<script>
import SideBarMenu from '@/layouts/SideBarMenu'

export default {
    name: "SideBar",
    components: {
        SideBarMenu
    },
    computed: {
        routes() {
            return this.$router.options.routes
        },
    },
    data() {
        return {
            collapsed: false,
            openKeys: ['sub1'],
        }
    },
    methods: {
        handleClick(event) {
            this.$router.push({name: event.key})
        }
    }
}
</script>

<style scoped>

</style>
