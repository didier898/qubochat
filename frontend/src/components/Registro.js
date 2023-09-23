import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password1: '',
    password2: '',
    pin: '',
    profile_picture: null,
  });
  const [message, setMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    const newValue = type === 'file' ? e.target.files[0] : value;

    setFormData({
      ...formData,
      [name]: newValue,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/register/', formData);

      if (response.status === 400 && response.data.error.includes('UNIQUE constraint failed: core_userprofile.username')) {
        setMessage('El usuario ya existe. Por favor, inicia sesión en lugar de registrarte.');
        setTimeout(() => {
          navigate('/inicio-sesion'); // Redirecciona a la página de inicio de sesión
        }, 2000);
      } else if (response.data.message) {
        setMessage(response.data.message);
        setSuccessMessage('Registro exitoso. ¡Bienvenido a QuboChat!');
        setTimeout(() => {
          navigate('/');
        }, 2000);
      } else {
        setMessage(response.data.error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Registro QuboChat</title>
        {/* Agrega el enlace a tu archivo de estilos CSS aquí */}
        <link rel="stylesheet" type="text/css" href="/ruta/a/tu/styles.css" />
      </head>
      <body>
        <div>
          <h3>Registro QuboChat</h3>
          {successMessage && <div className="success-message">{successMessage}</div>}
          <form onSubmit={handleSubmit}>
            <div className="row">
              <div className="input-field col s12">
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Usuario"
                />
                <label htmlFor="username">Usuario</label>
              </div>
            </div>
            <div className="row">
              <div className="input-field col s12">
                <input
                  type="password"
                  name="password1"
                  value={formData.password1}
                  onChange={handleChange}
                  placeholder="Contraseña"
                />
                <label htmlFor="password1">Contraseña</label>
              </div>
            </div>
            <div className="row">
              <div className="input-field col s12">
                <input
                  type="password"
                  name="password2"
                  value={formData.password2}
                  onChange={handleChange}
                  placeholder="Confirmar Contraseña"
                />
                <label htmlFor="password2">Confirmar Contraseña</label>
              </div>
            </div>
            <div className="row">
              <div className="input-field col s12">
                <input
                  type="text"
                  name="pin"
                  value={formData.pin}
                  onChange={handleChange}
                  placeholder="PIN 10 dígitos"
                />
                <label htmlFor="pin">PIN 10 dígitos</label>
              </div>
            </div>
            <div className="row">
              <div className="file-field input-field col s12">
                <div className="btn">
                  <span>Imagen de perfil</span>
                  <input
                    type="file"
                    name="profile_picture"
                    accept=".jpg, .jpeg, .png"
                    onChange={handleChange}
                  />
                </div>
                <div className="file-path-wrapper">
                  <input className="file-path validate" type="text" />
                </div>
              </div>
            </div>
            <div className="row">
              <div className="col s8">
                <button onClick={() => navigate('/')}>Regresar</button>
              </div>
              <div className="col s12">
                <div className="right">
                  <button className="btn blue waves-effect waves-light pull-s12" type="submit">
                    Registro
                  </button>
                </div>
              </div>
            </div>
          </form>
          {message && <div>{message}</div>}
        </div>
      </body>
    </html>
  );
}

export default Register;
