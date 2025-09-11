---
title: QQ登录
description: QQ登录
---

<Result :title="qq_title">
    <template #icon>
        <LoadingOutlined class="loading-icon" v-if="loaded == 0" />
        <CheckCircleOutlined v-if="loaded == 1" />
        <CloseCircleOutlined v-if="loaded == 2" />
    </template>
</Result>

<script setup>
import { ref, onMounted } from 'vue'
import { Result } from 'ant-design-vue'
import { LoadingOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons-vue'
import { mainStore } from ".vitepress/store";

const qq_title = ref("登录中..")
const loaded = ref(0)
const store = mainStore()

/**
 * QQ登录回调处理函数
 * 处理QQ OAuth回调，获取用户信息并保存到store中
 */
async function qqCallback() {
    const store = mainStore();

    if (location.pathname === '/qq_callback') {
        const code = new URLSearchParams(location.search).get('code');
        // 发送code到后端
        try {
            const res = await fetch('https://auth.al01.cn/qq_callback?code=' + code, {
                method: 'GET',
            });

            if (!res.ok) {
                const error = await res.json();
                toggleState(2, error.error)
                // 登录失败后重定向到首页
                setTimeout(() => {
                    location.href = '/';
                }, 2000);
                return;
            }

            const data = await res.json();

            // 保存用户信息和token到store，实现数据持久化
            const token = store.login(data, data.sessionId);

            toggleState(1, data.username)

            // 登录成功后重定向到首页
            setTimeout(() => {
                location.href = '/';
            }, 1500);
        } catch (error) {
            console.error('QQ登录处理错误:', error);
            toggleState(2, "登录处理出错，请稍后重试")
            // 出错后重定向到首页
            setTimeout(() => {
                location.href = '/';
            }, 2000);
        }
    }
}

function toggleState(state, msg) {
    if (state == 0) {
        qq_title.value = "登录中.."
        loaded.value = 0
    } else if (state == 1) {
        qq_title.value = "登录成功：" + msg
        loaded.value = 1
    } else if (state == 2) {
        qq_title.value = "登录失败：" + msg
        loaded.value = 2
    }
}
onMounted( async () => {
    await qqCallback();
});
</script>
