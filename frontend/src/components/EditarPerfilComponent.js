import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'; // Importa 'Link' de 'react-router-dom'
import InterfazBase from './InterfazBase'; // Importa tu componente base

class EditarPerfilComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      pin: '',
      profilePicture: null,
      successMessage: '',
      errorMessage: '',
    };
  }

  componentDidMount() {
    // Realiza una solicitud GET para obtener los datos del perfil del usuario actual
    axios.get('http://127.0.0.1:8000/api/profilee/')
      .then((response) => {
        const { username, pin, profile_picture_url } = response.data;
        this.setState({ username, pin, profilePicture: profile_picture_url });
      })
      .catch((error) => {
        console.error('Error al obtener los datos del perfil:', error);
      });
  }

  handleInputChange = (event) => {
    const { name, value, files } = event.target;
    if (name === 'profilePicture') {
      this.setState({ profilePicture: files[0] });
    } else {
      this.setState({ [name]: value });
    }
  }

  handleSubmit = (event) => {
    event.preventDefault();

    // Crear un objeto FormData para enviar el formulario con archivos
    const formData = new FormData();
    formData.append('username', this.state.username);
    formData.append('pin', this.state.pin);
    formData.append('profile_picture', this.state.profilePicture);

    // Realizar una solicitud POST para actualizar el perfil
    axios.post('http://127.0.0.1:8000/api/editar_perfilee/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Necesario para enviar archivos
      },
    })
      .then((response) => {
        this.setState({ successMessage: 'Perfil actualizado con éxito', errorMessage: '' });
      })
      .catch((error) => {
        console.error('Error al actualizar el perfil:', error);
        this.setState({ successMessage: '', errorMessage: 'Error al actualizar el perfil' });
      });
  }

  render() {
    const { username, pin, profilePicture, successMessage, errorMessage } = this.state;

    return (
      <InterfazBase> {/* Utiliza tu componente base aquí */}
        <div className="container">
          <h2>Editar tu perfil</h2>

          {successMessage && <div className="alert alert-success">{successMessage}</div>}
          {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}

          <form method="post" encType="multipart/form-data" onSubmit={this.handleSubmit}>
            {/* {% csrf_token %} Esto no es necesario en React */}
            <div className="form-group">
              <label htmlFor="username">Nombre de usuario</label>
              <input
                type="text"
                id="username"
                name="username"
                value={username}
                onChange={this.handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="pin">PIN</label>
              <input
                type="text"
                id="pin"
                name="pin"
                value={pin}
                onChange={this.handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="profilePicture">Cambiar foto de perfil</label>
              <input
                type="file"
                id="profilePicture"
                name="profilePicture"
                onChange={this.handleInputChange}
                accept="image/*"
              />
            </div>
            {profilePicture && (
              <div className="form-group">
                <label>Imagen de perfil actual</label>
                <br />
                <img src={profilePicture} alt="Imagen de perfil actual" className="img-thumbnail" />
              </div>
            )}
            <button type="submit" className="btn btn-primary">Guardar Cambios</button>
            <Link to="profile/" className="btn btn-secondary">Cancelar</Link> {/* Agrega el enlace de cancelar */}
          </form>
        </div>
      </InterfazBase>
    );
  }
}

export default EditarPerfilComponent;
