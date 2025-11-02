<script setup>
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { ref } from 'vue'

// O estado inicial da sidebar (false = recolhido)
const isSidebarExpanded = ref(false)

// Função para inverter o estado da sidebar
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
        
        <div class="title-wrapper">
          <img src="@/assets/logo.png" alt="AletheIA Logo" class="header-logo" />
          <h1 class="header-title">AletheIA</h1>
        </div>

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
  min-width: 0; /* Correção para evitar overflow do flexbox */
}

.main-header {
  /* Altura calculada para alinhar com o topo da sidebar */
  height: calc(1.5rem + 24px + 1rem);
  padding-left: 4rem;
  padding-right: 4rem;
  
  /* Alinha o .title-wrapper verticalmente */
  display: flex;
  align-items: center; 
  
  flex-shrink: 0; /* Previne que o header encolha */
}

/* Wrapper para alinhar ícone e texto */
.title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem; /* Espaço entre o ícone e o texto */
}

/* Estilo para o logo */
.header-logo {
  height: 28px; /* Alinhado com o font-size do título (1.75rem = 28px) */
  width: 28px;
}

.header-title {
  font-size: 1.75rem; 
  font-weight: 600;
  color: var(--cor-principal);
  line-height: 1; /* Garante alinhamento vertical */
}

/* Onde o conteúdo da HomeView aparece */
.main-content {
  flex-grow: 1; /* Ocupa todo o espaço vertical restante */
  padding: 2rem 4rem;
  max-width: 100%;
}
</style>