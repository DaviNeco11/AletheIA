<script setup>
import ApiService from '@/services/ApiService.js'; 
import { ref } from 'vue';

// 1. Importe os novos componentes
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ResultDisplay from '@/components/ResultDisplay.vue';

const newsText = ref('');
const isLoading = ref(false);
const verificationResult = ref(null); 

async function submitNews() {
  if (newsText.value.trim() === '') {
    alert('Por favor, insira algum texto.');
    return;
  }

  verificationResult.value = null;
  isLoading.value = true;

  try {
    const response = await ApiService.checkNews(newsText.value);
    verificationResult.value = response.data; 
  } catch (error) {
    console.error('Erro ao verificar notícia:', error);
    verificationResult.value = { error: 'Ocorreu um erro ao verificar.' };
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="home-container">
    <div class="input-section">
      <h2>Como posso ajudar?</h2>
      
      <div class="text-input-wrapper">
        <textarea
          v-model="newsText"
          placeholder="Insira o texto"
          :disabled="isLoading" 
        ></textarea>
        
        <button class="add-button" :disabled="isLoading">
          <vue-feather type="plus" size="32" />
        </button>

        <button 
          @click="submitNews" 
          class="internal-send-button"
          :disabled="isLoading" 
        >
          <vue-feather type="send" size="24" />
        </button>
      </div>

      <LoadingSpinner v-if="isLoading" />

      <ResultDisplay 
        v-if="verificationResult && !isLoading"
        :result="verificationResult" 
      />
      
    </div>
  </div>
</template>

<style scoped>
/* 3. O CSS ficou MUITO mais limpo! */
.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding-top: 4rem; 
}

.input-section h2 {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  color: var(--cor-texto);
  text-align: center;
}

.text-input-wrapper {
  position: relative;
  width: 100%;
  height: 140px;
  background-color: var(--cor-input);
  border-radius: 18px;
  padding: 1.5rem;
}

/* ... (estilos do textarea e botões internos) ... */
.text-input-wrapper textarea {
  width: 100%;
  height: 100%;
  border: none;
  background: none;
  resize: none; 
  font-size: 1.2rem;
  font-family: inherit;
  color: var(--cor-principal);
  padding-bottom: 2rem; 
}

.text-input-wrapper textarea::placeholder {
  color: var(--cor-principal);
  opacity: 0.8;
}

.text-input-wrapper textarea:focus {
  outline: none;
}

.add-button {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  background: none;
  border: none;
  color: var(--cor-principal);
  cursor: pointer;
  opacity: 0.7;
}

.add-button:hover {
  opacity: 1;
}

.internal-send-button {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  background: none;
  border: none;
  color: var(--cor-principal);
  cursor: pointer;
  opacity: 0.9;
}

.internal-send-button:hover {
  opacity: 1;
}

/* Os estilos .loading-indicator e .result-display foram removidos */
</style>