async function enviarMensaje(event) {
    event.preventDefault();

    const input = document.getElementById('mensaje-input');
    const mensaje = input.value.trim();

    if (!mensaje) return;

    // 1. Mostrar mensaje del usuario
    appendMessage('user', mensaje);
    input.value = '';

    const chatBox = document.getElementById('chat-box');

    // 2. Mostrar indicador de "Escribiendo..."
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = '<div class="message-content">Escribiendo...</div>';
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // 3. Enviar al backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mensaje: mensaje })
        });

        // Quitar indicador de escribiendo
        chatBox.removeChild(typingDiv);

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();

        // 4. Mostrar respuesta del bot
        if (data.respuesta) {
            appendMessage('bot', data.respuesta);
        } else {
            appendMessage('bot', "¡Che, algo salió mal! Intentá de nuevo.");
        }

    } catch (error) {
        // Quitar indicador si hubo error
        if (chatBox.contains(typingDiv)) {
            chatBox.removeChild(typingDiv);
        }
        console.error('Error:', error);
        appendMessage('bot', "¡Me cortaron las piernas! No puedo conectar con el servidor.");
    }
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);

    // Auto-scroll al fondo
    chatBox.scrollTop = chatBox.scrollHeight;
}
