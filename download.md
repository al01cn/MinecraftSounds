---
title: 下载
description: 下载 MinecraftSounds 我的世界音乐包生成器
---

# 下载 MinecraftSounds

在这里，你可以下载最新版本的 MinecraftSounds
我的世界音乐包生成器。我们提供适用于 Windows 10/11 的安装包 或
免安装版本的压缩包。

## 最新版本

**当前版本**：v1.0.0 (2025-08-27)

### Windows

<div class="download-container">
  <div class="download-list">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul class="download-links" v-else>
      <h4>下载链接</h4>
      <!-- 固定的国内和境外下载节点 -->
      <li class="download-link-item">
        <a href="https://aloss-02.al01.cn/al01/MinecraftSound/releases/1.0.0/MinecraftSounds.zip" target="_blank" class="download-item">
          国内下载节点（免安装版）
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://aloss-02.al01.cn/al01/MinecraftSound/releases/1.0.0/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          国内下载节点（安装版）
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://pan.baidu.com/s/1xRb8rKfht7iUEJ3_EBzLyQ?pwd=mcsd" target="_blank" class="download-item">
          百度网盘（提取码: mcsd）
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds.zip" target="_blank" class="download-item">
          境外下载节点（Github）（免安装版）
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          境外下载节点（Github）（安装版）
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.dbhg.top/al01/MinecraftSounds/releases/1.0.0/MinecraftSounds.zip" target="_blank" class="download-item">
          境外下载节点（备用）（免安装版）
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.dbhg.top/al01/MinecraftSounds/releases/1.0.0/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          境外下载节点（备用）（安装版）
        </a>
      </li>
      <!-- API获取的加速节点 -->
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds.zip`" target="_blank" class="download-item">
          境外加速节点{{ index + 1 }} (延迟: {{ link.latency }}ms, 速度: {{ link.speed }})（免安装版）
        </a>
      </li>
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds_setup.exe`" target="_blank" class="download-item">
          境外加速节点{{ index + 1 }} (延迟: {{ link.latency }}ms, 速度: {{ link.speed }})（安装版）
        </a>
      </li>
    </ul>
  </div>
</div>

---

**当前版本**：v0.0.1-beta (2025-08-13)

### Windows

<div class="download-container">
  <div class="download-list">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul class="download-links" v-else>
      <h4>下载链接</h4>
      <!-- 固定的国内和境外下载节点 -->
      <li class="download-link-item">
        <a href="https://pan.baidu.com/s/1E7lcooud9uuQ8K4DZ80wIA?pwd=mcsd" target="_blank" class="download-item">
          百度网盘（提取码: mcsd）
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/beta/MinecraftSounds.zip" target="_blank" class="download-item">
          境外下载节点（Github）
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.al01.cn/al01/MinecraftSounds/beta/v0.0.1/MinecraftSounds.zip" target="_blank" class="download-item">
          境外下载节点（备用）
        </a>
      </li>
      <!-- API获取的加速节点 -->
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/beta/MinecraftSounds.zip`" target="_blank" class="download-item">
          境外加速节点{{ index + 1 }} (延迟: {{ link.latency }}ms, 速度: {{ link.speed }})
        </a>
      </li>
    </ul>
  </div>
</div>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

const downloadLinks = ref([]);
const loading = ref(false); // 初始不加载
const error = ref('');
const hasLoaded = ref(false); // 跟踪是否已经加载过

onMounted(() => {
  // 使用 Intersection Observer 监听下载容器是否进入视口
  nextTick(() => {
    const downloadContainers = document.querySelectorAll('.download-container');
    if (downloadContainers.length > 0) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          // 当下载容器进入视口且尚未加载数据时，加载数据
          if (entry.isIntersecting && !hasLoaded.value) {
            hasLoaded.value = true;
            fetchDownloadLinks();
            // 一旦加载，可以停止观察
            observer.disconnect();
          }
        });
      }, { threshold: 0.1 }); // 当10%的元素可见时触发

      // 开始观察所有下载容器
      downloadContainers.forEach(container => {
        observer.observe(container);
      });
    }
  });
});

function fetchDownloadLinks() {
  // 首先检查本地缓存
  const cachedData = localStorage.getItem('minecraftSoundsDownloadLinks');
  const cacheTime = localStorage.getItem('minecraftSoundsDownloadLinksTime');
  const now = Date.now();

  // 如果有缓存且缓存时间不超过24小时，直接使用缓存数据
  if (cachedData && cacheTime && (now - parseInt(cacheTime)) < 24 * 60 * 60 * 1000) {
    try {
      const parsedData = JSON.parse(cachedData);
      if (parsedData && parsedData.length > 0) {
        downloadLinks.value = parsedData;
        loading.value = false;
        return;
      }
    } catch (e) {
      console.error('缓存数据解析错误:', e);
      // 缓存数据解析错误，继续获取新数据
    }
  }

  // 没有有效缓存，请求API
  loading.value = true;
  error.value = '';

  // 使用 AbortController 以便在需要时可以取消请求
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10秒超时

  fetch(`https://api.akams.cn/github`, { signal: controller.signal })
    .then(response => response.json())
    .then(data => {
      clearTimeout(timeoutId);
      if (data.code === 200 && data.data && data.data.length > 0) {
        // 按延迟排序并获取前5个
        const processedLinks = data.data
          .sort((a, b) => a.latency - b.latency)
          .slice(0, 5)
          .map(link => ({
            ...link,
            // 确保speed属性存在，如果不存在则显示'未知'
            speed: link.speed || '未知'
          }));

        // 更新状态
        downloadLinks.value = processedLinks;
        loading.value = false;

        // 保存到本地缓存
        try {
          localStorage.setItem('minecraftSoundsDownloadLinks', JSON.stringify(processedLinks));
          localStorage.setItem('minecraftSoundsDownloadLinksTime', now.toString());
        } catch (e) {
          console.error('缓存保存错误:', e);
          // 缓存保存错误不影响正常显示
        }
      } else {
        // 尝试使用过期缓存作为后备
        if (cachedData) {
          try {
            downloadLinks.value = JSON.parse(cachedData);
            loading.value = false;
          } catch (e) {
            error.value = '获取下载链接失败，请稍后再试';
            loading.value = false;
          }
        } else {
          error.value = '获取下载链接失败，请稍后再试';
          loading.value = false;
        }
      }
    })
    .catch(err => {
      clearTimeout(timeoutId);
      console.error('Error:', err);

      // 发生错误时尝试使用缓存数据作为后备
      if (cachedData) {
        try {
          downloadLinks.value = JSON.parse(cachedData);
          loading.value = false;
        } catch (e) {
          error.value = '获取下载链接失败，请稍后再试';
          loading.value = false;
        }
      } else {
        error.value = '获取下载链接失败，请稍后再试';
        loading.value = false;
      }
    });
}
</script>

<style>
.download-container {
  margin: 20px 0;
  text-align: center;
  position: relative;
  width: 100%;
}

.download-list {
  margin: 0 auto;
  border-radius: 4px;
  padding: 15px;
  text-align: left;
}

.download-list h4 {
  margin-top: 0;
  margin-bottom: 15px;
}

.download-item {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  transition: background-color 0.2s;
  border-radius: 4px;
}

.download-item:hover {
  background-color: #f1f1f1;
  text-decoration: none;
}

.download-links {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.download-link-item {
  border-bottom: 1px solid #ddd;
}

.download-link-item:last-child {
  border-bottom: none;
}

.loading, .error {
  padding: 15px;
  text-align: center;
}

.error {
  color: #d9534f;
}
</style>

Github加速服务由[akams.cn](https://github.akams.cn/)提供

## 系统要求

### Windows

- Windows 10 或更高版本
- 64位操作系统
- 1GB RAM
- 500MB 可用磁盘空间

### Win7

- 经过测试在Win7会报缺少系统核心文件，可尝试，但推荐升级到Win10或更高系统版本

## 历史版本

你可以在我们的
[GitHub Releases 页面](https://github.com/al01cn/MinecraftSounds/releases)
找到所有历史版本。

## 问题反馈

如果你在下载或使用过程中遇到任何问题，请：

请在 [GitHub Issues](https://github.com/al01cn/MinecraftSounds/issues) 或
[Gitee Issues](https://gitee.com/al01/minecraft-sounds/issues) 上报告问题

## 更新日志

### v0.0.1-beta (2025-08-13)

- 内部测试版发布
- 实现了基本功能和界面
- 支持一键导出为资源包
- 分类功能（实验性）
