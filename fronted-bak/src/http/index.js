import axios from 'axios';
import {notification} from 'ant-design-vue';
import i18n from "@/locales";

export default {
    get: function (url, headers, data) {
        return common('get', url, headers, data).then(response => response);
    },

    post: function (url, headers, data) {
        return common('post', url, headers, data).then(response => response);
    },

    delete: function (url, headers, data) {
        return common('delete', url, headers, data).then(response => response);
    },

    put: function (url, headers, data) {
        return common('put', url, headers, data).then(response => response);
    },

    full: function (method, url, headers, data) {
        return common(method, url, headers, data).then(response => response);
    },
}

function common(method, url, headers, data) {
    return new Promise((resolve) => {
        axios({
            method: method,
            url: url,
            headers: headers,
            data: data
        })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                if (error.response) {
                    if (error.response.status === 404) {
                        notification.error({
                            message: i18n.global.t('tips.abnormalInterface'),
                            description: url + '\n' + i18n.global.t('tips.noInterface'),
                            style: {
                                whiteSpace: 'pre-wrap',
                            },
                        });
                    }
                } else {
                    notification.error({
                        message: i18n.global.t('tips.abnormalInterface'),
                        description: i18n.global.t('tips.unKnownError'),
                    });
                }
            })
    })
}
