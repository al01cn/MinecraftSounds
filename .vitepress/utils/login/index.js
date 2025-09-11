import { mainStore } from "../../store";

/**
 * 检查用户登录状态
 * 从localStorage中恢复用户登录状态
 */
export function checkLoginStatus() {
    const store = mainStore();
    // Pinia的persistedstate插件已经处理了数据持久化
    // 这里可以添加额外的登录状态检查逻辑
    if (store.isLoggedIn && store.token) {
        console.log('用户已登录:', store.userInfo?.username);
        return true;
    }
    return false;
}
