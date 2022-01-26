<template>
    <div style="border: 1px solid rgb(136, 198, 229); padding-top: 20px" v-show="showItems.length > 0">
        <div style="padding-bottom: 20px; text-align: right; margin-right: 2%">
            <a-button type="primary" @click="batchChoose(true)">全选</a-button>
            <a-button style="margin-left: 15px"  @click="batchChoose(false)">全不选</a-button>
        </div>
        <a-row>
            <a-col v-for="(item, index) in showItems" :key="item"
                   class="normal-item">
                <a-row @click="choose(item)">
                    <a-col class="normal-content" :title="item">
                        {{index + 1}}
                    </a-col>
                    <a-col class="normal-choice" :class="isChoose(item) ? 'is-choice' : 'not-choice'">
                        <span >√</span>
                    </a-col>
                </a-row>
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
    import {reactive, defineProps, defineEmits} from "vue";

    const props = defineProps({
        showItems: {
            type: Array
        },
    })

    const emit = defineEmits(['chooseItems'])

    let items = reactive({
        choose: []
    })

    const batchChoose = (flag) => {
        if (flag) {
            items.choose = JSON.parse(JSON.stringify(props.showItems))
        } else {
            items.choose = []
        }
        emit('chooseItems', items.choose);
    }

    const choose = (item) => {
        let index = items.choose.indexOf(item)
        if (index > -1) {
            items.choose.splice(index, 1)
        } else {
            items.choose.push(item)
        }
        emit('chooseItems', items.choose);
    }

    const isChoose = (item) => {
        let index = items.choose.indexOf(item)
        if (index > -1) {
            return true
        } else {
            return false
        }
    }

</script>

<style lang="sass" scoped>
$choose-width: 35px

.normal-item
    border: 1px solid gainsboro
    text-align: center
    line-height: 35px
    border-radius: 5px
    margin-bottom: 10px
    margin-left: 2%
    margin-right: 1%
    width: 30%

.normal-content
    width: calc(100% - #{$choose-width})

.normal-choice
    width: $choose-width
    line-height: 20px
    height: 20px
    border-radius: 4px
    background: #e4d4d4
    color: white

.normal-choice
    width: $choose-width
    line-height: 20px
    height: 20px
    border-radius: 4px

.not-choice
    background: #eae6e6
    color: white

.is-choice
    background: #c7cb4c
    color: #807500

</style>
