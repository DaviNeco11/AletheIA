import axios from 'axios';

// 1. Configuração do Axios
// Esta URL agora aponta para o seu servidor FastAPI
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', 
  headers: {
    'Content-Type': 'application/json'
  }
});

// 2. Definição dos métodos da API
export default {
  
  /**
   * Envia o texto da notícia para o backend para verificação.
   * @param {string} newsText - O texto a ser verificado.
   * @returns {Promise<Object>} A resposta da API
   */
  checkNews(newsText) {
    return apiClient.post('/verify', { text: newsText });
  },

  /**
   * Busca o histórico de verificações do usuário.
   * (Ainda simulado, pois não implementamos no backend)
   * @returns {Promise<Array>} Uma lista de verificações anteriores.
   */
  getHistory() {
    console.log('ApiService.getHistory foi chamado.');
    return Promise.resolve({ data: [
      { id: 1, text: 'Notícia de exemplo 1', result: 'FATO' },
      { id: 2, text: 'Notícia de exemplo 2', result: 'FALSO' },
    ]});
  }
};