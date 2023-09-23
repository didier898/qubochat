import React from 'react';
import axios from 'axios';

function LogoutComponent() {
  const handleLogout = () => {
    axios.post('http://127.0.0.1:8000/logout/')  // Usa la URL configurada en Django para el cierre de sesión
      .then((response) => {
        // Django redirigirá automáticamente al usuario a la página de inicio de sesión
      })
      .catch((error) => {
        console.error('Error al cerrar sesión:', error);
      });
  };

  return (
    <div>
      <button onClick={handleLogout}>Cerrar Sesión</button>
    </div>
  );
}

export default LogoutComponent;
