import SvgIcon from '@/components/SvgIcon'

const requireAll = requireContext => requireContext.keys().map(requireContext)
const req = require.context('./svg', false, /\.svg$/)
requireAll(req)


/**
 * 全局注册自定义组件
 * @param app
 */
export function setupCustomComponents(app) {
    app.component('svg-icon', SvgIcon);
}
