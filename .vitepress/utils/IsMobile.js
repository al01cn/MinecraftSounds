export default function checkIsMobile() {
    // 确保在客户端环境中执行
    if (typeof window === 'undefined') {
        return false; // 或者在服务端返回一个默认值
    }

    const mobileAgent = ["iphone", "ipod", "ipad", "android", "mobile", "blackberry", "webos", "incognito", "webmate", "bada", "nokia", "lg", "ucweb", "skyfire"];
    const userAgent = window.navigator.userAgent.toLowerCase();

    for (let i = 0; i < mobileAgent.length; i++) {
        if (userAgent.indexOf(mobileAgent[i]) !== -1) {
            return true;
        }
    }
    return false;
};