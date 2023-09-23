import React, { Component } from 'react';
import axios from 'axios';
import InterfazBase from './InterfazBase'; // Importa tu componente base

class EnviarMensajeComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      receptor_id: '',
      mensaje: '',
      successMessage: '',
      errorMessage: '',
    };
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    // Realizar una solicitud POST para enviar un mensaje
    axios.post('http://127.0.0.1:8000/enviar-mensaje/', this.state)
      .then((response) => {
        this.setState({ successMessage: 'Mensaje enviado con éxito', errorMessage: '' });
      })
      .catch((error) => {
        console.error('Error al enviar el mensaje:', error);
        this.setState({ successMessage: '', errorMessage: 'Error al enviar el mensaje' });
      });
  }

  render() {
    const { receptor_id, mensaje, successMessage, errorMessage } = this.state;

    return (
      <InterfazBase>
        <div className="container">
          <h2>Enviar Nuevo Mensaje</h2>

          {successMessage && <div className="alert alert-success">{successMessage}</div>}
          {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}

          <form method="post" onSubmit={this.handleSubmit}>
            {/* {% csrf_token %} Esto no es necesario en React */}
            <div className="form-group">
              <label htmlFor="receptor_id">ID del Receptor:</label>
              <input
                type="text"
                id="receptor_id"
                name="receptor_id"
                value={receptor_id}
                onChange={this.handleInputChange}
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="mensaje">Mensaje:</label>
              <textarea
                id="mensaje"
                name="mensaje"
                value={mensaje}
                onChange={this.handleInputChange}
                className="form-control"
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary">Enviar Mensaje</button>
          </form>
        </div>
      </InterfazBase>
    );
  }
}

export default EnviarMensajeComponent;
