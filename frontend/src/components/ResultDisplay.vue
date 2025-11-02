<script setup>
// 1. Define que este componente espera um 'prop' chamado 'result'
defineProps({
  result: Object // Espera um objeto (o verificationResult)
});
</script>

<template>
  <div class="result-display">
    <div v-if="result.error" class="error-message">
      <h3>Ocorreu um Erro</h3>
      <p>{{ result.error }}</p>
    </div>

    <div v-else>
      <h3>Resultado da Verificação:</h3>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<style scoped>
.result-display {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f0f4f7;
  border: 1px solid var(--cor-input);
  border-radius: 8px;
}

.result-display h3 {
  color: var(--cor-principal);
  margin-bottom: 1rem;
}

.result-display pre {
  background-color: #fff;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

/* Estilo específico para mensagens de erro */
.error-message {
  color: #D9534F; /* Um tom de vermelho */
}
.error-message h3 {
  color: #D9534F;
}
</style>