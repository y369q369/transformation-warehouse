<template>
    <a-dropdown>
        <a class="ant-dropdown-link" @click.prevent>
            <translation-outlined />
        </a>
        <template #overlay>
            <a-menu>
                <a-menu-item>
                    <a href="javascript:;">1st menu item</a>
                </a-menu-item>
                <a-menu-item>
                    <a href="javascript:;">2nd menu item</a>
                </a-menu-item>
                <a-menu-item>
                    <a href="javascript:;">3rd menu item</a>
                </a-menu-item>
            </a-menu>
        </template>
    </a-dropdown>
</template>

<script >
export default {
    name: "Test"
}
</script>

<style scoped>

</style>
