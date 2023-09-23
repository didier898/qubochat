import React, { Component } from 'react';
import axios from 'axios';
import InterfazBase from './InterfazBase'; // Importa tu componente base
import { Link } from 'react-router-dom'; // Importa Link de react-router-dom

class ChatComponent extends Component {
  state = {
    conversaciones: [],
    conversacionSeleccionada: null,
    mensajesPorConversacion: [],
  };

  componentDidMount() {
    // Realizar una solicitud GET para obtener la lista de conversaciones desde la API de Django
    axios.get('http://127.0.0.1:8000/api/chat/') // Reemplaza la URL con la de tu API de Django
      .then(response => {
        this.setState({ conversaciones: response.data });
      })
      .catch(error => {
        console.error(error);
      });
  }

  handleConversacionSeleccionada = (conversacionId) => {
    // Realizar una solicitud GET para obtener los mensajes de la conversación seleccionada
    axios.get(`http://127.0.0.1:8000/api/chat_conversacion/${conversacionId}/mensajes/`) // Utiliza conversacionId directamente
      .then(response => {
        const conversacionSeleccionada = this.state.conversaciones.find(conversacion => conversacion.id === conversacionId);
        this.setState({ conversacionSeleccionada, mensajesPorConversacion: response.data });
        
        // Redirige al usuario a la página de la conversación
        this.props.history.push(`/conversacion/${conversacionId}`); // Utiliza 'history.push' para redirigir
      })
      .catch(error => {
        console.error(error);
      });
  }

  render() {
    const { conversaciones, conversacionSeleccionada, mensajesPorConversacion } = this.state;

    return (
      <InterfazBase> {/* Utiliza tu componente base aquí */}
        <div className="container">
          <h2>Chats</h2>
          <ul>
            {conversaciones.map(conversacion => (
              <li key={conversacion.id}>
                <Link to={`/conversacion/${conversacion.id}`}>{conversacion.nombre}</Link>
              </li>
            ))}
          </ul>
          <div id="chat-box">
            {conversacionSeleccionada ? (
              <> 
                <h3>Chat con {conversacionSeleccionada.nombre}</h3>
                <ul>
                  {mensajesPorConversacion.map(mensaje => (
                    <li key={mensaje.id}>
                      {mensaje.sender}: {mensaje.message}
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <p>Selecciona una conversación para comenzar a chatear.</p>
            )}
          </div>
        </div>
      </InterfazBase>
    );
  }
}

export default ChatComponent;
