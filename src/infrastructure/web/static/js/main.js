// Cargar datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('totalClientes')) {
        cargarDashboard();
    }
});

function cargarDashboard() {
    fetch('/api/clientes')
        .then(response => response.json())
        .then(clientes => {
            const total = clientes.length;
            const activos = clientes.filter(c => c.activo).length;
            
            document.getElementById('totalClientes').textContent = total;
            document.getElementById('activosClientes').textContent = activos;
            document.getElementById('inactivosClientes').textContent = total - activos;

            const tbody = document.getElementById('tablaClientes');
            tbody.innerHTML = '';
            
            // Mostrar últimos 5 clientes
            clientes.slice(-5).forEach(cliente => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.nombre} ${cliente.apellido}</td>
                    <td>${cliente.dni}</td>
                    <td>
                        <span class="badge ${cliente.activo ? 'bg-success' : 'bg-secondary'}">
                            ${cliente.activo ? 'Activo' : 'Inactivo'}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="verCliente(${cliente.id})">
                            Ver
                        </button>
                    </td>
                `;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('tablaClientes').innerHTML = 
                '<tr><td colspan="5" class="text-center text-danger">Error al cargar</td></tr>';
        });
}

function verCliente(id) {
    window.location.href = `/clientes/${id}`;
}