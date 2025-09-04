---
title: Download
description: Download MinecraftSounds Minecraft Music Pack Generator
---

# Download MinecraftSounds

Here, you can download the latest version of MinecraftSounds Minecraft Music Pack Generator. We provide installation packages for Windows 10/11 or portable versions in zip format.

## Latest Version

**Current Version**: v1.0.0 (2025-08-27)

### Windows

<div class="download-container">
  <div class="download-list">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul class="download-links" v-else>
      <h4>Download Links</h4>
      <!-- 固定的国内和境外下载节点 -->
      <li class="download-link-item">
        <a href="https://aloss-02.al01.cn/al01/MinecraftSound/releases/1.0.0/MinecraftSounds.zip" target="_blank" class="download-item">
          Domestic Download Node (Portable Version)
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://aloss-02.al01.cn/al01/MinecraftSound/releases/1.0.0/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          Domestic Download Node (Installer Version)
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://pan.baidu.com/s/1xRb8rKfht7iUEJ3_EBzLyQ?pwd=mcsd" target="_blank" class="download-item">
          Baidu Netdisk (Extraction code: mcsd)
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds.zip" target="_blank" class="download-item">
          International Download Node (Github) (Portable Version)
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          International Download Node (Github) (Installer Version)
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.dbhg.top/al01/MinecraftSounds/releases/1.0.0/MinecraftSounds.zip" target="_blank" class="download-item">
          International Download Node (Backup) (Portable Version)
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.dbhg.top/al01/MinecraftSounds/releases/1.0.0/MinecraftSounds_setup.exe" target="_blank" class="download-item">
          International Download Node (Backup) (Installer Version)
        </a>
      </li>
      <!-- API获取的加速节点 -->
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds.zip`" target="_blank" class="download-item">
          International Acceleration Node {{ index + 1 }} (Latency: {{ link.latency }}ms, Speed: {{ link.speed }}) (Portable Version)
        </a>
      </li>
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/releases/MinecraftSounds_setup.exe`" target="_blank" class="download-item">
          International Acceleration Node {{ index + 1 }} (Latency: {{ link.latency }}ms, Speed: {{ link.speed }}) (Installer Version)
        </a>
      </li>
    </ul>
  </div>
</div>

---
**Current Version**: v0.0.1-beta (2025-08-13)

### Windows

<div class="download-container">
  <div class="download-list">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul class="download-links" v-else>
      <h4>Download Links</h4>
      <!-- Fixed domestic and international download nodes -->
      <li class="download-link-item">
        <a href="https://pan.baidu.com/s/1E7lcooud9uuQ8K4DZ80wIA?pwd=mcsd" target="_blank" class="download-item">
          Baidu Netdisk (Extraction code: mcsd)
        </a>
      </li>
      <li class="download-link-item">
        <a href="https://github.com/al01cn/MinecraftSounds/releases/download/beta/MinecraftSounds.zip" target="_blank" class="download-item">
          International Download Node (Github)
        </a>
      </li>
      <li class="download-link-item">
        <a href="http://assets-oss.al01.cn/al01/MinecraftSounds/beta/v0.0.1/MinecraftSounds.zip" target="_blank" class="download-item">
          International Download Node (Backup)
        </a>
      </li>
      <!-- API-obtained acceleration nodes -->
      <li class="download-link-item" v-for="(link, index) in downloadLinks" :key="index">
        <a :href="`${link.url}/https://github.com/al01cn/MinecraftSounds/releases/download/beta/MinecraftSounds.zip`" target="_blank" class="download-item">
          International Acceleration Node {{ index + 1 }} (Latency: {{ link.latency }}ms, Speed: {{ link.speed }})
        </a>
      </li>
    </ul>
  </div>
</div>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

const downloadLinks = ref([]);
const loading = ref(false); // Initially not loading
const error = ref('');
const hasLoaded = ref(false); // Track if already loaded

onMounted(() => {
  // Use Intersection Observer to monitor when download container enters viewport
  nextTick(() => {
    const downloadContainers = document.querySelectorAll('.download-container');
    if (downloadContainers.length > 0) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          // When download container enters viewport and data not yet loaded, load data
          if (entry.isIntersecting && !hasLoaded.value) {
            hasLoaded.value = true;
            fetchDownloadLinks();
            // Once loaded, can stop observing
            observer.disconnect();
          }
        });
      }, { threshold: 0.1 }); // Trigger when 10% of element is visible
      
      // Start observing all download containers
      downloadContainers.forEach(container => {
        observer.observe(container);
      });
    }
  });
});

function fetchDownloadLinks() {
  // First check local cache
  const cachedData = localStorage.getItem('minecraftSoundsDownloadLinks');
  const cacheTime = localStorage.getItem('minecraftSoundsDownloadLinksTime');
  const now = Date.now();
  
  // If cache exists and is less than 24 hours old, use cached data
  if (cachedData && cacheTime && (now - parseInt(cacheTime)) < 24 * 60 * 60 * 1000) {
    try {
      const parsedData = JSON.parse(cachedData);
      if (parsedData && parsedData.length > 0) {
        downloadLinks.value = parsedData;
        loading.value = false;
        return;
      }
    } catch (e) {
      console.error('Cache data parsing error:', e);
      // Continue to fetch new data if cache parsing fails
    }
  }
  
  // No valid cache, request from API
  loading.value = true;
  error.value = '';
  
  // Use AbortController to be able to cancel request if needed
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
  
  fetch(`https://api.akams.cn/github`, { signal: controller.signal })
    .then(response => response.json())
    .then(data => {
      clearTimeout(timeoutId);
      if (data.code === 200 && data.data && data.data.length > 0) {
        // Sort by latency and get the top 5
        const processedLinks = data.data
          .sort((a, b) => a.latency - b.latency)
          .slice(0, 5)
          .map(link => ({
            ...link,
            // Ensure speed property exists, if not display 'Unknown'
            speed: link.speed || 'Unknown'
          }));
          
        // Update state
        downloadLinks.value = processedLinks;
        loading.value = false;
        
        // Save to local cache
        try {
          localStorage.setItem('minecraftSoundsDownloadLinks', JSON.stringify(processedLinks));
          localStorage.setItem('minecraftSoundsDownloadLinksTime', now.toString());
        } catch (e) {
          console.error('Cache save error:', e);
          // Cache save error doesn't affect normal display
        }
      } else {
        // Try to use expired cache as fallback
        if (cachedData) {
          try {
            downloadLinks.value = JSON.parse(cachedData);
            loading.value = false;
          } catch (e) {
            error.value = 'Failed to get download links, please try again later';
            loading.value = false;
          }
        } else {
          error.value = 'Failed to get download links, please try again later';
          loading.value = false;
        }
      }
    })
    .catch(err => {
      clearTimeout(timeoutId);
      console.error('Error:', err);
      
      // Try to use cached data as fallback when error occurs
      if (cachedData) {
        try {
          downloadLinks.value = JSON.parse(cachedData);
          loading.value = false;
        } catch (e) {
          error.value = 'Failed to get download links, please try again later';
          loading.value = false;
        }
      } else {
        error.value = 'Failed to get download links, please try again later';
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
Github acceleration service provided by [akams.cn](https://github.akams.cn/)

## System Requirements

### Windows
- Windows 10 or higher
- 64-bit operating system
- 1GB RAM
- 500MB available disk space

### Win7
- Testing has shown that Win7 will report missing system core files. You can try it, but upgrading to Win10 or higher is recommended.

## Historical Versions

You can find all historical versions on our [GitHub Releases page](https://github.com/al01cn/MinecraftSounds/releases).

## Feedback

If you encounter any issues during download or use, please:

Report issues on [GitHub Issues](https://github.com/al01cn/MinecraftSounds/issues) or [Gitee Issues](https://gitee.com/al01/minecraft-sounds/issues)

## Changelog

### v0.0.1-beta (2025-08-13)

- Internal beta version released
- Implemented basic features and interface
- Support for one-click export as resource pack
- Category feature (experimental)