<template>
    <template v-if="showCurrentMenu()">
        <template v-if="isMenuItem()">
            <a-menu-item v-for="item in showMenus" :key="item.name">
                <template #icon>
                    <component :is="item.info.icon"/>
                </template>
                <span>{{ $t(item.info.title) }}</span>
            </a-menu-item>
        </template>

        <a-sub-menu v-else :key="showMenus[0].name">
            <template #icon>
                <component :is="showMenus[0].info.icon"/>
            </template>
            <template #title>{{ $t(showMenus[0].info.title) }}</template>
            <side-bar-menu v-for="item in menuItems" :key="item.path" :menu="item"></side-bar-menu>
        </a-sub-menu>
    </template>

</template>

<script>
export default {
    name: "SideBarMenu",
    props: {
        menu: Object
    },
    data() {
        return {
            showMenus: [],
            menuItems: []
        }
    },
    created() {
        this.handleMenu()
    },
    methods: {
        /**
         * 没有子节点 且 自身无 info.hidden 属性, 展示自身
         * 自身有 info.hidden 属性，自身的name为home，展示所有子节点（无 info.hidden 属性,）
         *
         *  子节点 无 info.hidden 属性， 展示下一级
         */
        handleMenu() {
            if (this.menu.info) {
                if (this.menu.info.hidden) {
                    if (this.menu.name === 'home' && this.menu.children !== undefined) {
                        if (this.menu.children.length > 0) {
                            this.menu.children.forEach(child => {
                                if (child.info && !child.info.hidden) {
                                    this.showMenus.push(child)
                                }
                            })
                        }
                    }
                    // if (this.menu.children !== undefined) {
                    //     if(this.menu.children.length === 1) {
                    //         let tempMenu = this.menu.children[0]
                    //         if(tempMenu.info && !tempMenu.info.hidden) {
                    //             this.showMenu = tempMenu
                    //             if (tempMenu.children !== undefined) {
                    //                 tempMenu.children.forEach(child => {
                    //                     if (child.info && !child.info.hidden) {
                    //                         this.menuItems.push(child)
                    //                     }
                    //                 })
                    //             }
                    //         }
                    //     }
                    // }
                } else {
                    this.showMenus.push(this.menu)
                    if (this.menu.children !== undefined) {
                        this.menu.children.forEach(child => {
                            if (child.info && !child.info.hidden) {
                                this.menuItems.push(child)
                            }
                        })
                    }
                }
            }
        },

        /**
         * 判断当前菜单是否有展示的菜单
         */
        showCurrentMenu() {
            return this.showMenus.length > 0
        },

        /**
         * 判断是否为单条展示：      1. 没有子节点且自身有info属性展示自身（* 确保router中没有特例：没有子节点且自身也没有meta属性）
         *                         2. 有且只有一个子节点，且本身没有meat属性，子节点有meta属性
         */
        isMenuItem() {
            return this.showMenus.length > 0 && this.menuItems.length === 0
        }
    }
}
</script>

