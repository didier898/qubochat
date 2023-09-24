import React, { useEffect, useState } from 'react';
import {  useNavigate } from 'react-router-dom'; // Importa Link y useNavigate desde react-router-dom
import InterfazBase from './InterfazBase'; // Importa tu componente base

function ProfileComponent() {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate(); // Obtiene la función navigate

  // Realiza una solicitud al backend para obtener los datos del perfil del usuario
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/profilee/') // Asegúrate de usar la URL correcta para obtener el perfil desde tu backend Django
      .then((response) => response.json())
      .then((data) => {
        setUserData(data);
      })
      .catch((error) => {
        console.error('Error al obtener los datos del perfil:', error);
      });
  }, []);

  if (!userData) {
    // Muestra un mensaje de carga mientras se obtienen los datos del perfil
    return <div>Cargando perfil...</div>;
  }

  return (
    <InterfazBase> {/* Utiliza tu componente base aquí */}
      <div className="container">
        <h2>Perfil de Usuario</h2>
        <div className="row">
          <div className="col-md-4">
            <h4>Información del Perfil</h4>
            <ul>
              <li>PIN: {userData.pin}</li>
              <li>ID de Usuario: {userData.user_id}</li>
            </ul>
          </div>
          <div className="col-md-4">
            <h4>Imagen de Perfil</h4>
            <img src={userData.profile_picture_url} alt="Imagen de perfil" />
          </div>
        </div>
        {/* Utiliza navigate para redirigir a la página de edición de perfil */}
        <button onClick={() => navigate('/profile/edit')} className="btn btn-primary">Editar Perfil</button>
      </div>
    </InterfazBase>
  );
}

export default ProfileComponent;
