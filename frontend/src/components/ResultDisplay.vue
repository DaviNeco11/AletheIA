<script setup>
import { computed } from 'vue';

const props = defineProps({
  result: Object 
});

const resultStyle = computed(() => {
  if (props.result.error) {
    return {
      icon: 'alert-circle',
      class: 'error'
    };
  }
  const veracidade = props.result.veracidade.toUpperCase();

  if (veracidade === 'FATO') {
    return { icon: 'check-circle', class: 'fato' };
  }
  if (veracidade === 'FALSO') {
    return { icon: 'x-circle', class: 'falso' };
  }
  return { icon: 'alert-triangle', class: 'inconclusivo' };
});
</script>

<template>
  <div class="message-bubble" :class="resultStyle.class">
    
    <div v-if="result.error">
      <div class="result-header">
        <vue-feather :type="resultStyle.icon" size="20" />
        <h3 class="veracidade-title">Ocorreu um Erro</h3>
      </div>
      <p class="analise-text">{{ result.error }}</p>
    </div>

    <div v-else>
      <div class="result-header">
        <vue-feather :type="resultStyle.icon" size="20" />
        <h3 class="veracidade-title">{{ result.veracidade }}</h3>
      </div>
      <p class="analise-text">{{ result.analise }}</p>
      <div class="score-display">
        <strong>Score:</strong> {{ (result.score * 100).toFixed(0) }}%
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 1. Estilo da bolha de resposta (como no Figma) */
.message-bubble {
  width: 100%;
  padding: 1.5rem;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.veracidade-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  line-height: 1;
}

.analise-text {
  font-size: 1rem;
  color: var(--cor-principal); /* <-- MUDANÇA (texto escuro) */
  margin: 0;
}

.score-display {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--cor-principal); /* <-- MUDANÇA (texto escuro) */
  opacity: 0.8;
}

/* 2. Cores dinâmicas (apenas para o cabeçalho) */
.fato .result-header { color: #28a745; }
.falso .result-header { color: #dc3545; }
.inconclusivo .result-header { color: #ffc107; }
.error .result-header { color: #dc3545; }
</style>