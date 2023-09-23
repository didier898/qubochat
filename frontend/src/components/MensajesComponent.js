// MensajesComponent.js

import React, { Component } from 'react';
import axios from 'axios';

class MensajesComponent extends Component {
  state = {
    mensajes: [],
  };

  componentDidMount() {
    // Realizar una solicitud GET para obtener los mensajes desde la API de Django
    axios.get('http://127.0.0.1:8000/api/mensajes/')  // Reemplaza la URL con la de tu API de Django
      .then(response => {
        this.setState({ mensajes: response.data });
      })
      .catch(error => {
        console.error(error);
      });
  }

  render() {
    return (
      <div>
        <h1>Mensajes</h1>
        <ul>
          {this.state.mensajes.map(mensaje => (
            <li key={mensaje.id}>{mensaje.texto}</li>
          ))}
        </ul>
      </div>
    );
  }
}

export default MensajesComponent;
