function getSign(e) {
    function t(e, t) {
        return e << t | e >>> 32 - t
    }

    function n(e, t) {
        var n, r, i, o, a;
        return i = 2147483648 & e,
            o = 2147483648 & t,
            a = (1073741823 & e) + (1073741823 & t),
            (n = 1073741824 & e) & (r = 1073741824 & t) ? 2147483648 ^ a ^ i ^ o : n | r ? 1073741824 & a ? 3221225472 ^ a ^ i ^ o : 1073741824 ^ a ^ i ^ o : a ^ i ^ o
    }

    function r(e, r, i, o, a, s, c) {
        return e = n(e, n(n(function (e, t, n) {
            return e & t | ~e & n
        }(r, i, o), a), c)),
            n(t(e, s), r)
    }

    function i(e, r, i, o, a, s, c) {
        return e = n(e, n(n(function (e, t, n) {
            return e & n | t & ~n
        }(r, i, o), a), c)),
            n(t(e, s), r)
    }

    function o(e, r, i, o, a, s, c) {
        return e = n(e, n(n(function (e, t, n) {
            return e ^ t ^ n
        }(r, i, o), a), c)),
            n(t(e, s), r)
    }

    function a(e, r, i, o, a, s, c) {
        return e = n(e, n(n(function (e, t, n) {
            return t ^ (e | ~n)
        }(r, i, o), a), c)),
            n(t(e, s), r)
    }

    function s(e) {
        var t, n = "", r = "";
        for (t = 0; 3 >= t; t++)
            n += (r = "0" + (e >>> 8 * t & 255).toString(16)).substr(r.length - 2, 2);
        return n
    }

    var c, l, u, d, f, p, h, m, v, y;
    for (y = function (e) {
        for (var t, n = e.length, r = n + 8, i = 16 * ((r - r % 64) / 64 + 1), o = new Array(i - 1), a = 0, s = 0; n > s;)
            a = s % 4 * 8,
                o[t = (s - s % 4) / 4] = o[t] | e.charCodeAt(s) < < a,
                s++;
        return a = s % 4 * 8,
            o[t = (s - s % 4) / 4] = o[t] | 128 < < a,
            o[i - 2] = n << 3,
            o[i - 1] = n >>> 29,
            o
    }(e = function (e) {
        e = e.replace(/\r\n/g, "\n");
        for (var t = "", n = 0; n < e.length; n++) {
            var r = e.charCodeAt(n);
            128 > r ? t += String.fromCharCode(r) : r > 127 && 2048 > r ? (t += String.fromCharCode(r >> 6 | 192),
                t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
                t += String.fromCharCode(r >> 6 & 63 | 128),
                t += String.fromCharCode(63 & r | 128))
        }
        return t
    }(e)),
             p = 1732584193,
             h = 4023233417,
             m = 2562383102,
             v = 271733878,
             c = 0; c < y.length; c += 16)
        l = p,
            u = h,
            d = m,
            f = v,
            p = r(p, h, m, v, y[c + 0], 7, 3614090360),
            v = r(v, p, h, m, y[c + 1], 12, 3905402710),
            m = r(m, v, p, h, y[c + 2], 17, 606105819),
            h = r(h, m, v, p, y[c + 3], 22, 3250441966),
            p = r(p, h, m, v, y[c + 4], 7, 4118548399),
            v = r(v, p, h, m, y[c + 5], 12, 1200080426),
            m = r(m, v, p, h, y[c + 6], 17, 2821735955),
            h = r(h, m, v, p, y[c + 7], 22, 4249261313),
            p = r(p, h, m, v, y[c + 8], 7, 1770035416),
            v = r(v, p, h, m, y[c + 9], 12, 2336552879),
            m = r(m, v, p, h, y[c + 10], 17, 4294925233),
            h = r(h, m, v, p, y[c + 11], 22, 2304563134),
            p = r(p, h, m, v, y[c + 12], 7, 1804603682),
            v = r(v, p, h, m, y[c + 13], 12, 4254626195),
            m = r(m, v, p, h, y[c + 14], 17, 2792965006),
            p = i(p, h = r(h, m, v, p, y[c + 15], 22, 1236535329), m, v, y[c + 1], 5, 4129170786),
            v = i(v, p, h, m, y[c + 6], 9, 3225465664),
            m = i(m, v, p, h, y[c + 11], 14, 643717713),
            h = i(h, m, v, p, y[c + 0], 20, 3921069994),
            p = i(p, h, m, v, y[c + 5], 5, 3593408605),
            v = i(v, p, h, m, y[c + 10], 9, 38016083),
            m = i(m, v, p, h, y[c + 15], 14, 3634488961),
            h = i(h, m, v, p, y[c + 4], 20, 3889429448),
            p = i(p, h, m, v, y[c + 9], 5, 568446438),
            v = i(v, p, h, m, y[c + 14], 9, 3275163606),
            m = i(m, v, p, h, y[c + 3], 14, 4107603335),
            h = i(h, m, v, p, y[c + 8], 20, 1163531501),
            p = i(p, h, m, v, y[c + 13], 5, 2850285829),
            v = i(v, p, h, m, y[c + 2], 9, 4243563512),
            m = i(m, v, p, h, y[c + 7], 14, 1735328473),
            p = o(p, h = i(h, m, v, p, y[c + 12], 20, 2368359562), m, v, y[c + 5], 4, 4294588738),
            v = o(v, p, h, m, y[c + 8], 11, 2272392833),
            m = o(m, v, p, h, y[c + 11], 16, 1839030562),
            h = o(h, m, v, p, y[c + 14], 23, 4259657740),
            p = o(p, h, m, v, y[c + 1], 4, 2763975236),
            v = o(v, p, h, m, y[c + 4], 11, 1272893353),
            m = o(m, v, p, h, y[c + 7], 16, 4139469664),
            h = o(h, m, v, p, y[c + 10], 23, 3200236656),
            p = o(p, h, m, v, y[c + 13], 4, 681279174),
            v = o(v, p, h, m, y[c + 0], 11, 3936430074),
            m = o(m, v, p, h, y[c + 3], 16, 3572445317),
            h = o(h, m, v, p, y[c + 6], 23, 76029189),
            p = o(p, h, m, v, y[c + 9], 4, 3654602809),
            v = o(v, p, h, m, y[c + 12], 11, 3873151461),
            m = o(m, v, p, h, y[c + 15], 16, 530742520),
            p = a(p, h = o(h, m, v, p, y[c + 2], 23, 3299628645), m, v, y[c + 0], 6, 4096336452),
            v = a(v, p, h, m, y[c + 7], 10, 1126891415),
            m = a(m, v, p, h, y[c + 14], 15, 2878612391),
            h = a(h, m, v, p, y[c + 5], 21, 4237533241),
            p = a(p, h, m, v, y[c + 12], 6, 1700485571),
            v = a(v, p, h, m, y[c + 3], 10, 2399980690),
            m = a(m, v, p, h, y[c + 10], 15, 4293915773),
            h = a(h, m, v, p, y[c + 1], 21, 2240044497),
            p = a(p, h, m, v, y[c + 8], 6, 1873313359),
            v = a(v, p, h, m, y[c + 15], 10, 4264355552),
            m = a(m, v, p, h, y[c + 6], 15, 2734768916),
            h = a(h, m, v, p, y[c + 13], 21, 1309151649),
            p = a(p, h, m, v, y[c + 4], 6, 4149444226),
            v = a(v, p, h, m, y[c + 11], 10, 3174756917),
            m = a(m, v, p, h, y[c + 2], 15, 718787259),
            h = a(h, m, v, p, y[c + 9], 21, 3951481745),
            p = n(p, l),
            h = n(h, u),
            m = n(m, d),
            v = n(v, f);
    return (s(p) + s(h) + s(m) + s(v)).toLowerCase()
}


// 获取命令行传入的参数
let args = process.argv.slice(2);


let datetime = args[0]
let data = args[1]
let token = args[2]
if (!token) {
    token = undefined
    // console.log(token)
}
let appKey = args[3]

// console.log(data)


// var token = undefined
// datetime = (new Date).getTime()
// var appKey = 24679788
// var data = '{"targetType":"SHOW","targetId":"efbfbd1e204e0fefbfbd","appName":"pc_user_page","appKey":"Nn96sXA2qdCm5bUrTW+rnw=="}'
// var data = "{\"ms_codes\":\"2019030100\",\"params\":\"{\\\"biz\\\":true,\\\"scene\\\":\\\"component\\\",\\\"componentVersion\\\":\\\"3\\\",\\\"ip\\\":\\\"112.20.94.90\\\",\\\"debug\\\":0,\\\"utdid\\\":\\\"gAXaGUK+3w8CAXAUXTWZcdbb\\\",\\\"userId\\\":\\\"\\\",\\\"platform\\\":\\\"pc\\\",\\\"gray\\\":0,\\\"nextSession\\\":\\\"{\\\\\\\"componentIndex\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"componentId\\\\\\\":\\\\\\\"61518\\\\\\\",\\\\\\\"level\\\\\\\":\\\\\\\"2\\\\\\\",\\\\\\\"itemPageNo\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"lastItemIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"pageKey\\\\\\\":\\\\\\\"LOGICSHOW_LOGICTV_DEFAULT\\\\\\\",\\\\\\\"dataSourceType\\\\\\\":\\\\\\\"episode\\\\\\\",\\\\\\\"group\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"itemStartStage\\\\\\\":1,\\\\\\\"itemEndStage\\\\\\\":30}\\\",\\\"videoId\\\":\\\"XNTg4NDExNDIyMA==\\\",\\\"showId\\\":\\\"efbfbd1e204e0fefbfbd\\\"}\",\"system_info\":\"{\\\"os\\\":\\\"pc\\\",\\\"device\\\":\\\"pc\\\",\\\"ver\\\":\\\"1.0.0\\\",\\\"appPackageKey\\\":\\\"pcweb\\\",\\\"appPackageId\\\":\\\"pcweb\\\"}\"}"
// var data = "{\"ms_codes\":\"2019030100\",\"params\":\"{\\\"biz\\\":true,\\\"scene\\\":\\\"component\\\",\\\"componentVersion\\\":\\\"3\\\",\\\"ip\\\":\\\"240e:479:c18:1ef1:c07d:6326:39f7:36d5\\\",\\\"debug\\\":0,\\\"utdid\\\":\\\"gAXaGUK+3w8CAXAUXTWZcdbb\\\",\\\"userId\\\":\\\"\\\",\\\"platform\\\":\\\"pc\\\",\\\"gray\\\":0,\\\"nextSession\\\":\\\"{\\\\\\\"componentIndex\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"componentId\\\\\\\":\\\\\\\"61518\\\\\\\",\\\\\\\"level\\\\\\\":\\\\\\\"2\\\\\\\",\\\\\\\"itemPageNo\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"lastItemIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"pageKey\\\\\\\":\\\\\\\"LOGICSHOW_LOGICTV_DEFAULT\\\\\\\",\\\\\\\"dataSourceType\\\\\\\":\\\\\\\"episode\\\\\\\",\\\\\\\"group\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"itemStartStage\\\\\\\":31,\\\\\\\"itemEndStage\\\\\\\":60}\\\",\\\"videoId\\\":\\\"XNTg4NDExNDE2OA==\\\",\\\"showId\\\":\\\"efbfbd1e204e0fefbfbd\\\"}\",\"system_info\":\"{\\\"os\\\":\\\"pc\\\",\\\"device\\\":\\\"pc\\\",\\\"ver\\\":\\\"1.0.0\\\",\\\"appPackageKey\\\":\\\"pcweb\\\",\\\"appPackageId\\\":\\\"pcweb\\\"}\"}"


let param = token + "&" + datetime + "&" + appKey + "&" + data
// console.log(param)

let sign = getSign(param)
console.log(sign)