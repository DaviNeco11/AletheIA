<script setup>
import ApiService from '@/services/ApiService.js'; 
import { ref } from 'vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ResultDisplay from '@/components/ResultDisplay.vue';

const conversation = ref([]); 
const newsText = ref('');
const isLoading = ref(false);

async function submitNews() {
  const textToSubmit = newsText.value;
  if (textToSubmit.trim() === '') return;

  conversation.value.push({
    id: Date.now(),
    role: 'user',
    content: textToSubmit
  });
  
  newsText.value = '';
  isLoading.value = true;

  try {
    const response = await ApiService.checkNews(textToSubmit);
    conversation.value.push({
      id: Date.now() + 1,
      role: 'bot',
      content: response.data 
    });
  } catch (error) {
    console.error('Erro ao verificar notícia:', error);
    conversation.value.push({
      id: Date.now() + 1,
      role: 'bot',
      content: { error: 'Ocorreu um erro ao verificar.' }
    });
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="home-container" :class="{ 'chat-active': conversation.length > 0 }">
    
    <div class="chat-area">
      
      <h2 v-if="conversation.length === 0" class="welcome-title">
        Como posso ajudar?
      </h2>

      <div v-if="conversation.length > 0" class="chat-history">
        <div v-for="message in conversation" :key="message.id" class="message-wrapper">
          
          <div v-if="message.role === 'user'" class="user-message">
            <p>{{ message.content }}</p> 
          </div>
          <ResultDisplay v-if="message.role === 'bot'" :result="message.content" />

        </div>
      </div>
      
      <LoadingSpinner v-if="isLoading" class="bottom-spinner" />
    </div>

    <div class="input-section">
      <div class="text-input-wrapper">
        <textarea
          v-model="newsText"
          placeholder="Insira o texto"
          :disabled="isLoading" 
          @keydown.enter.prevent="submitNews" 
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
    </div>
  </div>
</template>

<style scoped>

.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding-top: 4rem; 
  padding-bottom: 4rem;
}

.welcome-title {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  color: var(--cor-texto);
  text-align: center;
}

.input-section {
  margin-top: 3rem; 
}

.home-container.chat-active {
  height: calc(100vh - (1.5rem + 24px + 1rem) - 4rem);
  display: flex;
  flex-direction: column;
  padding-top: 0;
  padding-bottom: 0;
}

.chat-active .chat-area {
  flex-grow: 1; 
  overflow-y: auto; 
  padding-top: 2rem; 
}

.chat-active .input-section {
  margin-top: 0;
  flex-shrink: 0; 
  padding-top: 1rem;
  padding-bottom: 2rem; 
  border-top: 1px solid var(--cor-input);
}

.chat-history {
  width: 100%;
}

.message-wrapper {
  margin-bottom: 2rem;
  display: flex;
}

.message-wrapper > .user-message {
  background-color: var(--cor-input);
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
  max-width: 80%;
  display: inline-block;
  text-align: left; 
  margin-left: auto;
}
.user-message p {
  white-space: pre-wrap; 
  margin: 0;
}

.message-wrapper > :deep(.message-bubble) {
  margin-right: auto;
  width: auto;
  max-width: 90%;
  display: inline-block;
  text-align: left;
}

.bottom-spinner {
  margin-bottom: 2rem;
}

.text-input-wrapper {
  position: relative;
  width: 100%;
  min-height: 150px; 
  background-color: var(--cor-input);
  border-radius: 12px;
  padding: 1.5rem;
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
  padding-bottom: 2rem; 
  min-height: 100px;
}

.text-input-wrapper textarea::placeholder { color: var(--cor-principal); opacity: 0.8; }
.text-input-wrapper textarea:focus { outline: none; }
.add-button { position: absolute; bottom: 1.5rem; left: 1.5rem; background: none; border: none; color: var(--cor-principal); cursor: pointer; opacity: 0.7; }
.add-button:hover { opacity: 1; }
.internal-send-button { position: absolute; bottom: 1.5rem; right: 1.5rem; background: none; border: none; color: var(--cor-principal); cursor: pointer; opacity: 0.9; }
.internal-send-button:hover { opacity: 1; }
</style>