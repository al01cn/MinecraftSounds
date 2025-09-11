// .vitepress/theme/index.js
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import LoginButton from './components/LoginButton.vue'
import Layout from './components/Layout.vue'
import Antd, { message } from 'ant-design-vue';

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate);

// PWA
navigator.serviceWorker.addEventListener("controllerchange", () => {
  // 弹出更新提醒
  console.log("站点已更新，刷新后生效");
  message.info("站点已更新，刷新后生效");
});

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('LoginButton', LoginButton)
    app.use(Antd)
    app.use(pinia)
  }
}