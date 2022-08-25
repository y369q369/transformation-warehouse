<template>
    <svg class="svg-icon" v-bind="$attrs" :style="{color: color}">
        <use :xlink:href="iconName" rel="external nofollow"/>
    </svg>
</template>

<script setup lang="ts">
import {defineProps, computed} from "vue";

const props = defineProps({
    name: {
        type: String,
        required: true
    },
    color: {
        type: String,
        default: ''
    }
})

const iconName = computed(() => `#icon-${props.name}`);

</script>

<style scoped>
.svg-icon {
    width: 1em;
    height: 1em;
    fill: currentColor;
    vertical-align: middle;
}
</style>