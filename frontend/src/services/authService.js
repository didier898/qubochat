// authService.js

import api from './api';

// Ejemplo de función de inicio de sesión
export function login(credentials) {
  return api.post('/api/auth/login/', credentials);
}

// Otras funciones de autenticación
