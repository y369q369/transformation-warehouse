import {defineStore} from "pinia"
import {Base64} from 'js-base64'


function initUser() {
    let user = localStorage.getItem('user')
    return user ? JSON.parse(Base64.decode(user)) : {}
}

export const localStore = defineStore({
    id: "local",
    state: () => ({
        token: localStorage.getItem('token'),
        user: initUser(),
        sidebarShow: localStorage.getItem('sidebar')
    }),
    getters: {
        sidebarShowFlag: (state) => {
            return state.sidebarShow && state.sidebarShow == 'hide' ? false : true
        },
    },
    actions: {
        storeToken(data: string) {
            this.token = data
            localStorage.setItem('token', data)
        },
        storeUser(data: object) {
            this.user = data
            let userInfo = Base64.encode(JSON.stringify(data))
            localStorage.setItem('user', userInfo)
        },
        storeSidebar(data: boolean) {
            let flag = 'hide'
            if (data) {
                flag = 'show'
            }
            this.sidebarShow = flag
            localStorage.setItem('sidebar', flag)
        }
    },
});