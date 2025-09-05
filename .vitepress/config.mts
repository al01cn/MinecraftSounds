import { defineConfig } from 'vitepress'
import { inject } from "@vercel/analytics"
import { injectSpeedInsights } from '@vercel/speed-insights';

injectSpeedInsights();
inject()

let title = 'MinecraftSounds - 我的世界音乐包生成器'
let description = '简单易用的我的世界音乐包生成器，专为小白制作。提供最简单的可视化界面，支持最新版本的游戏。标准化的项目管理。'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: title,
  description: description,
  lang: 'zh-CN',
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      title: 'MinecraftSounds - 我的世界音乐包生成器',
      description: description,
      themeConfig: {
        langMenuLabel: '切换语言',
        nav: [
          { text: '首页', link: '/' },
          { text: '快速开始', link: '/guide/getting-started' },
          { text: '下载', link: '/download' },
          { text: '关于', link: '/about' }
        ],
        sidebar: [
          {
            text: '指南',
            items: [
              { text: '介绍', link: '/guide/' },
              { text: '快速开始', link: '/guide/getting-started' },
            ]
          },
          {
            text: '进阶教程',
            items: [
              { text: '认识soundkey', link: '/tutorials/soundkey' },
              { text: '使用命令', link: '/tutorials/command' },
              { text: '分类功能', link: '/tutorials/category' },
            ]
          }
        ]
      }
    },
    en: {
      label: 'English',
      lang: 'en-US',
      title: 'MinecraftSounds - Minecraft Music Pack Generator',
      description: 'A simple and easy-to-use Minecraft music pack generator, specially made for beginners. Provides the simplest visual interface, supports the latest game versions.',
      themeConfig: {
        langMenuLabel: 'Language',
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Getting Started', link: '/en/guide/getting-started' },
          { text: 'Download', link: '/en/download' },
          { text: 'About', link: '/en/about' }
        ],
        sidebar: [
          {
            text: 'Guide',
            items: [
              { text: 'Introduction', link: '/en/guide/' },
              { text: 'Getting Started', link: '/en/guide/getting-started' },
            ]
          },
          {
            text: 'Advanced Tutorials',
            items: [
              { text: 'Understanding Soundkey', link: '/en/tutorials/soundkey' },
              { text: 'Using Commands', link: '/en/tutorials/command' },
              { text: 'Category Feature', link: '/en/tutorials/category' },
            ]
          }
        ]
      }
    }
  },
  ignoreDeadLinks: true,
  head: [
    ['link', { rel: 'icon', type: 'image/png', href: '/note_block.png' }],
    ['link', { rel: 'shortcut icon', href: '/note_block.png' }],
    ['meta', { name: 'description', content: description }],
    ['meta', { name: 'keywords', content: 'MinecraftSounds, 我的世界音乐包生成器, 音乐包, 我的世界, 小阿狼是也, AL01, 零一狼' }],
    ['meta', { name: 'author', content: '小阿狼是也 & 零一狼AL01' }],
    ['meta', { name: 'og:title', content: title }],
    ['meta', { name: 'og:description', content: description }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:url', content: 'https://mcsd.al01.cn/' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: title }],
    ['meta', { name: 'twitter:description', content: description }],
    ['meta', { name: 'twitter:site', content: '@alwolf_cn' }],
    ['meta', { name: 'twitter:creator', content: '@alwolf_cn' }],
    ['meta', { name: 'twitter:domain', content: 'https://mcsd.al01.cn/' }],
    ['script', { async: 'true', src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9092291426352834', crossorigin: 'anonymous' }],
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/note_block.png',
    siteTitle: 'MinecraftSounds',
    socialLinks: [
      { icon: 'gitee', link: 'https://gitee.com/al01/minecraft-sounds' },
      { icon: 'github', link: 'https://github.com/al01cn/MinecraftSounds' }
    ],
    
    footer: {
      message: '软件和站点基于 GPL-2.0 许可发布<br><a href="https://beian.miit.gov.cn" target="_blank"> 粤ICP备2025454179号 </a>',
      copyright: 'Copyright © 2025 <a href="https://space.bilibili.com/415963320" target="_blank">小阿狼是也</a> & <a href="https://al01.cn" target="_blank">零一狼AL01</a>',
    },
    
    // 修改 localeLinks 为正确的属性名称
    locales: {
      root: {
        label: '简体中文',
        link: '/'
      },
      en: {
        label: 'English',
        link: '/en/'
      }
    }
  }
})
