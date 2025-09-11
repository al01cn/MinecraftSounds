// .vitepress/theme/index.js
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import LoginButton from './components/LoginButton.vue'
import Layout from './components/Layout.vue'
import Antd from 'ant-design-vue';

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate);

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    if (!import.meta.env.SSR) {
      pinia.use(piniaPluginPersistedstate);
    }
    app.component('LoginButton', LoginButton)
    app.use(Antd)
    app.use(pinia)
  }
}