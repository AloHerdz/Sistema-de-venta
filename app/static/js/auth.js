async function login(username, password) {
    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        if(res.ok) {
            // Guardar el token en localStorage
            localStorage.setItem('token', data.token);
            return {success: true};
        } else {
            return {success: false, error: data.error || 'Error al iniciar sesión'};
        }
    } catch (err) {
        return {success: false, error: 'Error de conexión'};
    }
}

function getToken() {
    return localStorage.getItem('token');
}

function logout() {
    localStorage.removeItem('token');
}
