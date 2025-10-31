<script setup>
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { ref } from 'vue'

const isSidebarExpanded = ref(true)

function toggleSidebar() {
  isSidebarExpanded.value = !isSidebarExpanded.value
}
</script>

<template>
  <div class="app-layout">
    <Sidebar 
      :is-expanded="isSidebarExpanded" 
      @toggle="toggleSidebar" 
    />

    <div class="content-wrapper">
      
      <header class="main-header">
        <h1 class="header-title">AletheIA</h1>
      </header>

      <main class="main-content">
        <RouterView />
      </main>
    </div>

  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-width: 0; 
}

.main-header {
  height: calc(1.5rem + 24px + 1rem);
  padding-left: 4rem;
  padding-right: 4rem;
  display: flex;
  align-items: center; 
  flex-shrink: 0;
}

.header-title {
  font-size: 1.75rem; 
  font-weight: 600;
  color: var(--cor-principal);
  line-height: 1; 
}

.main-content {
  flex-grow: 1; 
  padding: 2rem 4rem;
  max-width: 100%;
}
</style>