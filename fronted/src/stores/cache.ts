import {defineStore} from "pinia";

export const routeStore = defineStore({
    id: "route",
    state: () => ({
        access: '',
    }),
});