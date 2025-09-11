<template>
  <div class="navbar-login">
    <ClientOnly>
      <LoginButton />
    </ClientOnly>
  </div>
</template>

<script setup>

</script>

<style scoped>
.navbar-login {
  width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>