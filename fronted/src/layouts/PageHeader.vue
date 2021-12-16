<template>
    <a-col class="header">
<!--        <a @click="goBack">-->
<!--            <arrow-left-outlined />-->
<!--        </a>-->
        <a-col>
            <a-select
                ref="select"
                style="width: 120px"
                @change="handleLang"
            >
                <a-select-option value="jack">Jack</a-select-option>
                <a-select-option value="lucy">Lucy</a-select-option>
            </a-select>
        </a-col>
    </a-col>
</template>

<script>
export default {
    name: "PageHeader",
    methods: {
        goBack() {
            this.$router.back()
        },
        handleLang(value) {
            console.log(value)
        }
    }
}
</script>

<style scoped lang="sass">
.header
    height: 50px
    line-height: 50px
    border-bottom: 1px solid #f0f0f0
    padding-left: 30px
    margin-bottom: 20px
</style>
