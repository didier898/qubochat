import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './components/LoginComponent';
import EditarPerfilComponent from './components/EditarPerfilComponent';
import RegisterComponent from './components/Registro';
import ProfileComponent from './components/Profile';
import ChatComponent from './components/ChatComponent';
import EnviarMensajeComponent from './components/EnviarMensajeComponent';
import ConversacionComponent from './components/ConversacionComponent';
import LogoutComponent from './components/LogoutComponent'; // Agrega la importación de LogoutComponent

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas para las interfaces */}
        <Route path="/" element={<LoginComponent />} />
        <Route path="/profile/edit" element={<EditarPerfilComponent />} />
        <Route path="/register" element={<RegisterComponent />} />
        <Route path="/profile" element={<ProfileComponent />} />
        <Route path="/chat" element={<ChatComponent />} />
        <Route path="/enviar-mensaje" element={<EnviarMensajeComponent />} />
        <Route path="/chat/:conversacion_id" element={<ConversacionComponent />} />

        {/* Ruta para el componente de cierre de sesión */}
        <Route path="/logout" element={<LogoutComponent />} />

        {/* Otras rutas o redireccionamiento */}
        <Route path="*" element={<div>404 - Página no encontrada</div>} />
      </Routes>
    </Router>
  );
}

export default App;
