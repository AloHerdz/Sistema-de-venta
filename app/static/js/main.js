async function crearCliente({nombre, telefono, colonia}) {
    const token = getToken();
    if(!token) return {success:false, error:'No hay token'};
    try {
        const res = await fetch('/clientes/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({nombre, telefono, colonia})
        });
        const data = await res.json();
        if(res.ok) {
            return {success: true, data: data};
        } else {
            return {success: false, error: data.error};
        }
    } catch(e) {
        return {success:false, error:'Error de conexión'};
    }
}

async function agregarTransaccion(id_cliente, {monto, tipo}) {
    const token = getToken();
    if(!token) return {success:false, error:'No hay token'};
    try {
        const res = await fetch('/transacciones/'+id_cliente, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({monto, tipo})
        });
        const data = await res.json();
        if(res.ok) {
            return {success:true, data:data};
        } else {
            return {success:false, error:data.error};
        }
    } catch(e) {
        return {success:false, error:'Error de conexión'};
    }
}

async function verSaldo(id_cliente) {
    const token = getToken();
    if(!token) return {success:false, error:'No hay token'};
    try {
        const res = await fetch('/clientes/'+id_cliente+'/saldo', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        const data = await res.json();
        if(res.ok) {
            return {success:true, saldo:data.saldo};
        } else {
            return {success:false, error:data.error};
        }
    } catch(e) {
        return {success:false, error:'Error de conexión'};
    }
}
