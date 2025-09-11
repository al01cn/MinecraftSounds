<template>
  <div class="navbar-login">
    <ClientOnly>
      <LoginButton />
    </ClientOnly>
  </div>
</template>

<script setup>
import { mainStore } from '../../store'
const store = mainStore();
</script>

<style scoped>
.navbar-login {
  margin-left: v-bind('store.isLoggedIn ? (store.userInfo?.username?.length >= 10 ? "40px" : store.userInfo?.username?.length >= 5 ? "30px" : "20px") : "5px"');
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>