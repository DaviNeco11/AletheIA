<template>
  <div class="loading-container">
    <div class="spinner"></div>
    <p>Verificando...</p>
  </div>
</template>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  font-size: 1.2rem;
  color: var(--cor-principal);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--cor-input); /* Borda clara */
  border-top-color: var(--cor-principal); /* Cor principal (a que gira) */
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Animação de rotação */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>