<template>
    <div class="login-wrap">
        <div class="login">
            <div class="login-title">登录</div>
            <el-form :model="param" :rules="rules" ref="ruleFormRef" label-width="0px" class="login-content">
                <el-form-item prop="username">
                    <el-input v-model="param.name" placeholder="name">
                        <template #prepend>
                            <el-button icon="User"></el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="param.password"
                              @keyup.enter="submitForm()">
                        <template #prepend>
                            <el-button icon="Lock"></el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-col style="color: var(--el-color-danger); text-align: left; padding-bottom: 10px">
                        {{ loginInfo }}
                    </el-col>
                    <el-button type="primary" @click="submitForm()">登录</el-button>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {useRouter} from 'vue-router'
import axios from "@/plugins/axios";
import {localStore} from '@/stores/local'


const router = useRouter()
const param = reactive({
  name: "admin",
  password: "admin",
});

const loginInfo = ref('')

const rules = {
    name: [
        {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
        },
    ],
    password: [
        {required: true, message: "请输入密码", trigger: "blur"},
    ],
};

const ruleFormRef = ref(null)
const submitForm = () => {
    ruleFormRef!.value.validate((valid) => {
        if (valid) {
            axios.post('/api/user/login', param)
                .then(function (response) {
                    if (response.code === 200) {
                      axios.get('/api/user/userInfo', {
                        params: {
                          userName: param.name
                        }
                      }).then(function (user) {
                        const local = localStore()
                        local.storeUser(response)
                        localStorage.setItem('token', user.token)
                        router.push('/dashboard')
                      })
                    } else {
                      loginInfo.value = response.msg
                    }
                })
        } else {
            loginInfo.value = ''
        }
    });
};

</script>

<style scoped>
.login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background-image: url(/src/assets/img/login-bg.jpg);
    background-size: 100%;
}

.login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.3);
    overflow: hidden;
}

.login-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #fff;
    border-bottom: 1px solid #ddd;
}

.login-content {
    padding: 30px 30px;
}

.login-btn {
    text-align: center;
}

.login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}

</style>