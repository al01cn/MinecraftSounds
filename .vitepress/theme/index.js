// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { SpeedInsights } from '@vercel/speed-insights'
import { inject } from "@vercel/analytics"

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.use(SpeedInsights)
    inject()
  }
}
