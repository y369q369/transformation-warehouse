<template>
    <a-dropdown>
        <a class="ant-dropdown-link" @click.prevent>
            {{ novel_source }}
            <DownOutlined />
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

<script setup>
    import {ref} from "vue";

    const novel_source = ref('笔趣阁')
</script>

<style scoped>

</style>
