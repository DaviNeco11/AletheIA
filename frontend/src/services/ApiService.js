import axios from 'axios';

// 1. Configuração da Instância do Axios
// (Mesmo que não usemos agora, é bom já deixar configurado)
const apiClient = axios.create({
  // Quando seu backend estiver rodando, você mudará esta URL:
  baseURL: 'http://127.0.0.1:8000/api', // Ex: URL do seu backend Python
  headers: {
    'Content-Type': 'application/json'
  }
});

// 2. Definição dos métodos da API
export default {
  
  /**
   * Envia o texto da notícia para o backend para verificação.
   * @param {string} newsText - O texto a ser verificado.
   * @returns {Promise<Object>} A resposta da API (ex: { veracidade: 'FATO', score: 0.9 })
   */
  checkNews(newsText) {
    console.log('ApiService.checkNews foi chamado com:', newsText);
    
    // LINHA COMENTADA (para adicionar a lógica depois):
    // return apiClient.post('/verify', { text: newsText });

    // Por enquanto, vamos apenas retornar uma promessa simulada:
    return Promise.resolve({ data: { veracidade: 'SIMULADO', score: 0.99 } });
  },

  /**
   * Busca o histórico de verificações do usuário.
   * @returns {Promise<Array>} Uma lista de verificações anteriores.
   */
  getHistory() {
    console.log('ApiService.getHistory foi chamado.');
    
    // LINHA COMENTADA (para adicionar a lógica depois):
    // return apiClient.get('/history');

    // Retorno simulado:
    return Promise.resolve({ data: [
      { id: 1, text: 'Notícia de exemplo 1', result: 'FATO' },
      { id: 2, text: 'Notícia de exemplo 2', result: 'FALSO' },
    ]});
  }
};