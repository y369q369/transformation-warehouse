<template>
    <div>
        <svg-icon name="dashboard"></svg-icon>
        <!--        <div class="test"></div>-->
        <!--        <el-button @click="t1"> 点击 </el-button>-->
        <!--        <div class="test2" :class="cla"></div>-->
    </div>
</template>

<script setup lang="ts">
import 'https://at.alicdn.com/t/c/font_3604969_9ocug20lrqe.js?spm=a313x.7781069.1998910419.53&file=font_3604969_9ocug20lrqe.js'
import '@/assets/icons/iconfont/user.svg'
import {ref} from "vue";

const flag = ref(false)
const cla = ref('')

const t1 = () => {
    flag.value = !flag.value
    cla.value = flag.value ? 'right1' : 'left1'
}

</script>

<style scoped>
.test {
    width: 100px;
    height: 100px;
    background: red;
    position: relative;
    animation: myfirst 5s;
    -webkit-animation: myfirst 5s;
}

.test2 {
    width: 100px;
    height: 100px;
    background: orange;
}

.right1 {
    transform: translate(100px, 50px);
    transition: all 1s linear;
}

.left1 {
    transform: translate(0px, 0px);
    transition: all 1s linear;
}

@keyframes myfirst {
    from {
        left: 0px;
    }
    to {
        left: -200px;
    }
}

/*@-webkit-keyframes myfirst !* Safari and Chrome *!*/
/*{*/
/*    from {left:0px;}*/
/*    to {left:200px;}*/
/*}*/
</style>