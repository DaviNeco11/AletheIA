<script setup>
defineProps({
  isExpanded: Boolean
})

const emit = defineEmits(['toggle'])
</script>

<template>
  <nav class="sidebar" :class="{ collapsed: !isExpanded }">
    
    <div class="sidebar-top">
      <button class="menu-btn" @click="emit('toggle')">
        <vue-feather type="menu" size="24" /> 
      </button>
    </div>

    <template v-if="isExpanded">
      
      <div class="top-menu-section">
        <ul class="menu-list">
          <li>
            <vue-feather type="edit-2" size="20" /> <span>Novo Chat</span>
          </li>
          <li>
            <vue-feather type="archive" size="20" /> <span>Histórico</span>
          </li>
        </ul>
      </div>

      <div class="empty-space"></div> 
      
      <div class="sidebar-bottom-panel">
        <div class="menu-section">
          <ul class="menu-list">
            <li><vue-feather type="user" size="20" /> <span>Personalização</span></li>
            <li><vue-feather type="settings" size="20" /> <span>Configuração</span></li>
            <li><vue-feather type="help-circle" size="20" /> <span>Ajuda</span></li>
            <li><vue-feather type="log-out" size="20" /> <span>Sair</span></li>
          </ul>
        </div>
        <div class="profile-section">
          <div class="divider"></div>
          <div class="profile-info">
            <vue-feather type="user" size="24" class="profile-avatar" />
            <span>@email.com</span>
          </div>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="empty-space"></div> <div class="collapsed-profile">
        <vue-feather type="user" size="24" class="profile-avatar" />
      </div>
    </template>
    
  </nav>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: 280px;
  min-height: 100vh;
  padding: 1.5rem;
  background-color: var(--cor-principal);
  color: #f0f0f0;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
  
  transition: width 0.3s ease-in-out;
}

.sidebar.collapsed {
  width: 90px;
  padding: 1.5rem 1rem;
}

.sidebar-top {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.sidebar:not(.collapsed) .sidebar-top {
  justify-content: flex-start;
  margin-left: 0.5rem;
}

.menu-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.empty-space {
  flex-grow: 1;
}

.sidebar ul.menu-list {
  list-style: none;
}

.sidebar ul.menu-list li {
  display: flex;
  align-items: center;
  gap: 1rem; 
  padding: 0.8rem 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 8px;
}

.sidebar ul.menu-list li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-section {
  margin-bottom: 1rem;
}

.sidebar-bottom-panel {
  background-color: #4C778F;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  opacity: 1;
  transition: opacity 0.1s ease-out;
}

.divider {
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 0.8rem;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
}

.profile-avatar {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  padding: 4px;
}

.sidebar.collapsed .sidebar-bottom-panel,
.sidebar.collapsed .top-menu-section {
  opacity: 0;
  height: 0;
  padding: 0;
  overflow: hidden; 
  margin: 0;
}

.collapsed-profile {
  display: flex;
  justify-content: center; 
}

.collapsed-profile .profile-avatar {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  padding: 4px;
}
</style>