<script setup>
import DefaultTheme from 'vitepress/theme'
import NavbarLogin from './NavbarLogin.vue'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #nav-bar-content-after>
      <NavbarLogin />
    </template>
  </Layout>
</template>