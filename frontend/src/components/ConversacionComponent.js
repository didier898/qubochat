import React, { Component } from 'react';
import axios from 'axios';
import InterfazBase from './InterfazBase';

class ConversacionComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      mensajes: [],
      mensajeNuevo: '',
    };
  }

  componentDidMount() {
    // Realiza una solicitud GET para obtener los mensajes de la conversación
    axios.get(`http://127.0.0.1:8000/api/chat_conversacion/${this.props.conversacionId}/mensajes/`)
      .then((response) => {
        this.setState({ mensajes: response.data.mensajes });
      })
      .catch((error) => {
        console.error('Error al obtener los mensajes:', error);
      });
  }

  handleInputChange = (event) => {
    this.setState({ mensajeNuevo: event.target.value });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    // Realizar una solicitud POST para enviar un mensaje en la conversación
    axios.post(`http://127.0.0.1:8000/api/conversacion/${this.props.conversacionId}/enviar_mensaje/`, {
      mensaje: this.state.mensajeNuevo,
    })
      .then((response) => {
        // Agrega el mensaje enviado a la lista de mensajes
        this.setState((prevState) => ({
          mensajes: [...prevState.mensajes, response.data],
          mensajeNuevo: '',
        }));
      })
      .catch((error) => {
        console.error('Error al enviar el mensaje:', error);
      });
  }

  render() {
    const { mensajes, mensajeNuevo } = this.state;

    return (
      <InterfazBase>
        <div className="container">
          <h2>Conversación con {this.props.otherUser}</h2>

          <div id="chat-box">
            <ul>
              {mensajes.map((mensaje) => (
                <li key={mensaje.id}>
                  {mensaje.sender === this.props.currentUser ? (
                    <strong>Tú:</strong>
                  ) : (
                    <strong>{mensaje.sender.username}:</strong>
                  )}
                  {mensaje.message}
                </li>
              ))}
            </ul>
          </div>

          <form onSubmit={this.handleSubmit}>
            <textarea
              name="mensaje"
              placeholder="Escribe tu mensaje aquí"
              value={mensajeNuevo}
              onChange={this.handleInputChange}
              required
            ></textarea>
            <button type="submit">Enviar</button>
          </form>
        </div>
      </InterfazBase>
    );
  }
}

export default ConversacionComponent;
