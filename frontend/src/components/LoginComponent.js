import React, { useState } from 'react';
import axios from 'axios';
import { Outlet, useNavigate } from 'react-router-dom';

function LoginComponent() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    error: '',
    success: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
      error: '',
      success: '',
    });
  };

  const handleLoginSuccess = (token) => {
    // Almacenar el token en localStorage
    localStorage.setItem('token', token);
    
    // Redirigir a la página de edición de perfil después del inicio de sesión exitoso
    navigate('/profile/edit');
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const { username, password } = formData;

    axios
      .post('http://127.0.0.1:8000/api/login/', {
        username,
        password,
      })
      .then((response) => {
        if (response.data.success) {
          setFormData({
            ...formData,
            success: response.data.message,
          });

          // Llamar a la función para manejar el inicio de sesión exitoso y pasar el token
          handleLoginSuccess(response.data.token);
        } else {
          setFormData({
            ...formData,
            error: 'Credenciales incorrectas',
          });
        }
      })
      .catch((error) => {
        console.error(error);
        setFormData({
          ...formData,
          error: 'Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo.',
        });
      });
  };

  return (
    <div>
      <div className="section blue lighten-3">
        <div className="container white-text center-align text">
          <h2>QuboChat</h2>
          <h3>Bienvenido a QuboChat, la mejor aplicación de mensajería</h3>
        </div>
      </div>
      <div className="container">
        <div className="row">
          <div className="col s12 m8 l6 offset-m2 offset-l3">
            <div className="section center-block">
              <div>
                <h3>Ingresar</h3>
                <form id="login-form" className="form-group" onSubmit={handleSubmit}>
                  <div className="row">
                    <div className="input-field col s12">
                      <input
                        name="username"
                        id="id_username"
                        type="text"
                        value={formData.username}
                        onChange={handleChange}
                      />
                      <label htmlFor="id_username">Usuario</label>
                    </div>
                  </div>
                  <div className="row">
                    <div className="input-field col s12">
                      <input
                        name="password"
                        id="id_password"
                        type="password"
                        value={formData.password}
                        onChange={handleChange}
                      />
                      <label htmlFor="id_password">Contraseña</label>
                    </div>
                  </div>
                  <div className="row">
                    <div className="col s8">
                      <a href="/register">Regístrate</a>
                    </div>
                    <div className="col s4">
                      <div className="right">
                        <button className="btn blue waves-effect waves-light pull-s12" type="submit">
                          Ingresar
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      {formData.success && <p className="success">{formData.success}</p>}
      {formData.error && <p className="error">{formData.error}</p>}
      <p>
        Somos la mejor app de mensajería, <a href="/register">REGISTRATE</a>!
      </p>
      {/* Renderiza las rutas anidadas */}
      <Outlet />
    </div>
  );
}

export default LoginComponent;
