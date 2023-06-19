function deactivateUser(user) {
    swal({
        title: "Estás seguro de que quieres desactivar este usuario?",
        text: "Esta acción podrá revertirse más tarde.",
        icon: "warning",
        dangerMode: true,
        buttons: {
            neutral: "Cancelar",
            confirm: "Desactivar"
        }
    }).then((value) => {
        switch (value) {
            case true:
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/control_deactivate_user', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr && xhr.readyState === 4 && xhr.status === 200) {
                            swal({
                                title: 'Usuario eliminado directamente',
                                text: 'La página se recargará a continuación.',
                                icon: 'success',
                                timer: 3000,
                                buttons: false,
                            }).then(function () {
                                location.reload();
                            });
                        } else {
                            swal({
                                title: 'Ha ocurrido un error',
                                text: 'Recargue la página y vuelva a intentar nuevamente',
                                icon: 'error',
                                timer: 3000,
                                buttons: false,
                            });
                        }
                    };
                    var data = JSON.stringify({
                        user: user
                    });
                    xhr.send(data);
                } catch (error) {
                    console.error(error);
                }
                break;
            case null:
                console.log('Cancelar');
                break;
            default:
                console.log('Cancel');
        }
    })
}

function reactivateUser(user) {
    swal({
        title: "Estás seguro de que quieres desactivar este usuario?",
        text: "Esta acción podrá revertirse más tarde.",
        icon: "warning",
        dangerMode: true,
        buttons: {
            neutral: "Cancelar",
            confirm: "Reactivar"
        }
    }).then((value) => {
        switch (value) {
            case true:
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/control_reactivate_user', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr && xhr.readyState === 4 && xhr.status === 200) {
                            swal({
                                title: 'Usuario reactivado correctamente.',
                                text: 'La página se recargará a continuación.',
                                icon: 'success',
                                timer: 3000,
                                buttons: false,
                            }).then(function () {
                                location.reload();
                            });
                        } else {
                            swal({
                                title: 'Ha ocurrido un error',
                                text: 'Recargue la página y vuelva a intentar nuevamente',
                                icon: 'error',
                                timer: 3000,
                                buttons: false,
                            });
                        }
                    };
                    var data = JSON.stringify({
                        user: user
                    });
                    xhr.send(data);
                } catch (error) {
                    console.error(error);
                }
                break;
            case null:
                console.log('Cancelar');
                break;
            default:
                console.log('Cancel');
        }
    })
}

function updateUser(user) {
    const role = document.querySelector('#update-role-' + user);
    const status = document.querySelector('#update-status-' + user);

    let roleValue = role.options[role.selectedIndex].value;
    let statusValue = status.options[status.selectedIndex].value;

    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/control_update_user', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr && xhr.readyState === 4 && xhr.status === 200) {
                swal({
                    title: 'Usuario actualizado correctamente.',
                    text: 'La página se recargará a continuación.',
                    icon: 'success',
                    timer: 3000,
                    buttons: false,
                }).then(function () {
                    location.reload();
                });
            } else {
                swal({
                    title: 'Ha ocurrido un error',
                    text: 'Recargue la página y vuelva a intentar nuevamente.',
                    icon: 'error',
                    timer: 3000,
                    buttons: false,
                });
            }
        };
        var data = JSON.stringify({
            user: parseInt(user),
            role: parseInt(roleValue),
            status: statusValue,
        });
        xhr.send(data);
    } catch (error) {
        console.error(error);
    }
}