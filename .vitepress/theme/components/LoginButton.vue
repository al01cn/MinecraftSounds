<template>
  <div class="login-container">
    <button @click="handleUserClick" class="login-button">{{ store.isLoggedIn ? (store.userInfo?.username?.substring(0, 10) || '注销') :
      '登录' }}</button>

    <!-- 登录弹窗 -->
    <div v-if="showModal" class="login-modal-overlay" @click.self="showModal = false">
      <div class="login-modal">
        <div class="login-modal-header">
          <h3>用户登录</h3>
          <button class="close-button" @click="showModal = false">×</button>
        </div>
        <div class="login-modal-body">
          <div class="form-group">
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="username" placeholder="请输入用户名">
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input type="password" id="password" v-model="password" placeholder="请输入密码">
          </div>
          <div class="form-actions">
            <button class="login-submit" @click="login">登录</button>
          </div>

          <!-- 第三方平台登录 -->
          <div class="third-party-login">
            <div class="divider">
              <span>第三方账号登录</span>
            </div>
            <div class="third-party-buttons">
              <button class="third-party-button qq" @click="thirdPartyLogin('QQ')">
                <svg viewBox="0 0 24 24" width="24" height="24">
                  <path fill="currentColor"
                    d="M12.003 2c-2.265 0-6.29 1.364-6.29 7.325v1.195S3.55 14.96 3.55 17.474c0 .665.17 1.025.281 1.025.114 0 .902-.484 1.748-2.072 0 0-.18 2.197 1.904 3.967 0 0-1.77.495-1.77 1.182 0 .686 4.078.43 6.29 0 2.239.425 6.287.687 6.287 0 0-.688-1.768-1.182-1.768-1.182 2.085-1.77 1.905-3.967 1.905-3.967.845 1.588 1.634 2.072 1.746 2.072.111 0 .283-.36.283-1.025 0-2.514-2.166-6.954-2.166-6.954V9.325C18.29 3.364 14.268 2 12.003 2z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { mainStore } from '../../store'
import checkIsMobile from '../../utils/IsMobile'

const store = mainStore();

const showModal = ref(false)
const username = ref('')
const password = ref('')

// 用户按钮点击事件
const handleUserClick = () => {
  if (store.isLoggedIn) {
    // 提供登出选项
    Modal.confirm({
      title: '提示',
      centered: true,
      content: '是否要退出登录？',
      okText: '确定',
      cancelText: '取消',
      onOk: () => {
        store.logout();
        message.success({
          content: '已成功退出登录',
          duration: 2
        });
      }
    })
  } else {
    // 未登录则显示登录表单
    showModal.value = true;
  }
};

const login = () => {
  if (!username.value) {
    message.warning({
      content: "请输入用户名",
      duration: 2
    });
    return;
  }
  if (!password.value) {
    message.warning({
      content: "请输入密码",
      duration: 2
    });
    return;
  }
  // 这里添加登录逻辑
  const userData = {
    username: username.value,
    loginTime: new Date().toLocaleString()
  };
  store.login(userData);
  showModal.value = false;
  username.value = '';
  password.value = '';
  message.success({
    content: '登录成功',
    duration: 2
  });
}

const thirdPartyLogin = (platform) => {
  // 这里添加第三方平台登录逻辑
  message.info({
    content: `正在使用${platform}账号登录`,
    duration: 3,
  })
  switch (platform.toLowerCase()) {
    case 'qq':
      const qqRedirectUri = encodeURIComponent('https://mcsd.al01.cn/qq_callback');
      const qqAuthUrl = `https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=102810408&redirect_uri=${qqRedirectUri}&display=${checkIsMobile() ? 'mobile' : 'pc'}`;
      delayRedirect(qqAuthUrl);
      break;
    default:
      break;
  }
}

// 延迟跳转链接
const delayRedirect = (url, delay = 1000) => {
  setTimeout(() => {
    location.href = url;
  }, delay);
};
</script>

<style scoped>
.login-container {
  display: inline-block;
}

.login-button {
  border-color: var(--vp-button-brand-border);
  color: var(--vp-button-brand-text);
  background-color: var(--vp-button-brand-bg);
  padding: 4px 16px;
  border-radius: 20px;
  text-align: center;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.5s ease;
  position: relative;
}

.login-button:hover {
  border-color: var(--vp-button-brand-hover-border);
  color: var(--vp-button-brand-hover-text);
  background-color: var(--vp-button-brand-hover-bg);
}

.login-button:active {
  border-color: var(--vp-button-brand-active-border);
  color: var(--vp-button-brand-active-text);
  background-color: var(--vp-button-brand-active-bg);
}

.login-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.login-modal {
  background-color: var(--vp-button-alt-hover-bg);
  border-radius: 8px;
  width: 350px;
  max-width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.login-modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--vp-c-text-1);
}

.close-button {
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  color: var(--vp-c-text-1);
}

.login-modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: var(--vp-c-text-1);
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--vp-c-text-1);
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: var(--vp-c-text-1);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.login-submit {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.login-submit {
  background-color: transparent;
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-text-1);
  flex: 1;
  transition: all 0.5s ease;
}

.login-submit:hover {
  border-color: rgba(255, 215, 0, 0.8);
  color: rgba(255, 215, 0, 0.8);
  filter: drop-shadow(0 0 5px rgba(255, 215, 0, 0.4));
  transform: scale(1.05);
}

.register-button {
  background-color: transparent;
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-divider);
  flex: 1;
  transition: all 0.5s ease;
}

.register-button:hover {
  border-color: rgba(255, 215, 0, 0.8);
  color: rgba(255, 215, 0, 0.8);
  filter: drop-shadow(0 0 5px rgba(255, 215, 0, 0.4));
  transform: scale(1.05);
}

/* 第三方登录样式 */
.third-party-login {
  margin-top: 20px;
}

.divider {
  display: flex;
  align-items: center;
  margin: 15px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--vp-c-divider);
}

.divider span {
  padding: 0 10px;
  font-size: 12px;
  color: var(--vp-c-text-2);
}

.third-party-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
}

.third-party-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--vp-c-divider);
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--vp-c-text-1);
}

.third-party-button:hover {
  transform: scale(1.1);
  border-color: transparent;
}

.third-party-button.github:hover {
  background-color: #24292e;
  color: white;
}

.third-party-button.wechat:hover {
  background-color: #07C160;
  color: white;
}

.third-party-button.qq:hover {
  background-color: #12B7F5;
  color: white;
}
</style>