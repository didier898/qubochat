import React from 'react';
import { Link } from 'react-router-dom';

const InterfazBase = ({ children }) => {
  return (
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Título de tu página</title>
        
      </head>
      <body>
        <header>
          <nav>
            <ul>
              <li>
                <Link to="/">Inicio</Link>
              </li>
              <li>
                <Link to="/profile/edit">Editar Perfil</Link>
              </li>
              <li>
                <Link to="/profile">Mi Perfil</Link>
              </li>
              <li>
                <Link to="/enviar-mensaje">Enviar Mensaje</Link>
              </li>
              <li>
                <Link to="/chat">Chat</Link>
              </li>
              <li>
                <Link to="/logout">Cerrar sesión</Link> {/* Actualiza la URL */}
              </li>
            </ul>
          </nav>
        </header>

        <main>{children}</main>

        <footer>
          {/* ... (pie de página común) ... */}
        </footer>
      </body>
    </html>
  );
};

export default InterfazBase;
