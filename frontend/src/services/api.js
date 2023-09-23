// api.js

import axios from 'axios';

// Configura la URL base de la API de Django
const BASE_API_URL = 'http://localhost:8000';

// Configura axios para usar la URL base
const api = axios.create({
  baseURL: BASE_API_URL,
});

export default api;
