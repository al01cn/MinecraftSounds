import { defineStore } from "pinia";

export const mainStore = defineStore("main", {
  state: () => {
    return {
      isLoggedIn: false, // 用户登录状态
      userInfo: null, // 用户信息
      token: null, // 用户token
    };
  },
  actions: {
    // 设置用户登录状态
    setLoginState(value) {
      this.isLoggedIn = value;
    },
    // 设置用户信息
    setUserInfo(value) {
      this.userInfo = value;
    },
    // 设置用户token
    setToken(value) {
      this.token = value;
    },
    // 用户登录
    login(userData, token = null) {
      this.isLoggedIn = true;
      this.userInfo = userData;
      this.token = token;
      return token;
    },
    // 用户登出
    logout() {
      this.isLoggedIn = false;
      this.userInfo = null;
      this.token = null;
    },
  },
  persist: {
    key: "data",
    storage: window.localStorage,
    paths: [
      "coverType",
      "siteStartShow",
      "footerBlur",
      "isLoggedIn",
      "userInfo",
      "token",
    ],
  },
});
