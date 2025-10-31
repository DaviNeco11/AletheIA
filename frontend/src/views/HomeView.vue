<script setup>
import { ref } from 'vue';

const newsText = ref('');

// Esta função agora será chamada pelo ícone de "send"
function submitNews() {
  if (newsText.value.trim() !== '') {
    alert('Texto enviado: ...' ); // Apenas um alerta para testar
    // ApiService.checkNews(newsText.value);
  } else {
    alert('Por favor, insira algum texto.');
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
        ></textarea>
        
        <button class="add-button">
          <vue-feather type="plus" size="32" />
        </button>

        <button @click="submitNews" class="internal-send-button">
          <vue-feather type="send" size="24" />
        </button>
      </div>

      </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding-top: 8rem; 
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
  /* A margin-bottom foi REMOVIDA */
}

.text-input-wrapper textarea {
  width: 100%;
  height: 100%;
  border: none;
  background: none;
  resize: none; 
  font-size: 1.2rem;
  font-family: inherit;
  color: var(--cor-principal);
  /* Adiciona padding para o texto não passar por baixo dos botões */
  padding-bottom: 4rem; 
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
  right: 2.5rem;
  background: none;
  border: none;
  color: var(--cor-principal);
  cursor: pointer;
  opacity: 0.9;
}

.internal-send-button:hover {
  opacity: 1;
}

</style>