$(document).ready(function() {
    // Función para cargar mensajes de una conversación al hacer clic en un enlace
    $('ul li a').on('click', function(e) {
        e.preventDefault();
        var conversationId = $(this).attr('data-conversation-id');
        loadMessages(conversationId);
    });

    // Función para cargar mensajes de una conversación
    function loadMessages(conversationId) {
        $.ajax({
            url: '/api/load_messages/', // Cambia la URL a la vista que carga los mensajes
            type: 'GET',
            data: { 'conversation_id': conversationId },
            success: function(data) {
                // Manipula los datos de respuesta para mostrar los mensajes en la interfaz de usuario
                var messages = data.messages;
                var chatBox = $('#chat-box');
                chatBox.empty();

                if (messages.length > 0) {
                    $.each(messages, function(index, message) {
                        var messageText = message.sender + ': ' + message.message;
                        chatBox.append('<p>' + messageText + '</p>');
                    });
                } else {
                    chatBox.append('<p>No hay mensajes en esta conversación.</p>');
                }
            },
            error: function(xhr, status, error) {
                // Maneja errores aquí
            }
        });
    }
});
