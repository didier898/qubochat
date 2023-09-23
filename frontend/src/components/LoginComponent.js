import React, { Component } from 'react';
import axios from 'axios';


class LoginComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      error: '',
      success: '',
    };
  }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
      error: '',
      success: '',
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    const { username, password } = this.state;

    axios
      .post('http://127.0.0.1:8000/login/', {
        username,
        password,
      })
      .then((response) => {
        if (response.data.message) {
          this.setState({
            success: response.data.message,
          });
          // Redirige a la página de perfil después del inicio de sesión exitoso
          // Utiliza <Link> para la navegación en lugar de navigate
          window.location.href = '/profile/edit';
        } else {
          this.setState({
            error: 'Credenciales incorrectas',
          });
        }
      })
      .catch((error) => {
        console.error(error);
        this.setState({
          error: 'Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo.',
        });
      });
  };

  render() {
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
                  <form id="login-form" className="form-group" onSubmit={this.handleSubmit}>
                    {/* {% csrf_token %} Esto no es necesario en React */}
                    <div className="row">
                      <div className="input-field col s12">
                        <input
                          name="username"
                          id="id_username"
                          type="text"
                          value={this.state.username}
                          onChange={this.handleChange}
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
                          value={this.state.password}
                          onChange={this.handleChange}
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
        {this.state.success && <p className="success">{this.state.success}</p>}
        {this.state.error && <p className="error">{this.state.error}</p>}
        <p>
          Somos la mejor app de mensajeria, REGISTRATE!
        </p>
      </div>
    );
  }
}

export default LoginComponent;
