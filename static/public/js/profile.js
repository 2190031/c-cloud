// convierte la imagen a base64
function convertToBase64(file_input) {
    return new Promise((resolve, reject) => {
        const file = file_input.files[0];
        const reader = new FileReader();
        reader.onloadend = function () {
            const base64Image = reader.result;
            resolve(base64Image);
        };
        reader.onerror = function (error) {
            reject(error);
        };
        reader.readAsDataURL(file);
    });
}

// actualiza la informacion del usuario
async function updatePersonalData() {
    let imageInput = document.querySelector('#upload');
    let image = imageInput.value;
    let firstname = document.querySelector('#firstname').value;
    let surname = document.querySelector('#surname').value;
    let username = document.querySelector('#username').value;
    let password = document.querySelector('#new-password').value;
    let repeat_password = document.querySelector('#repeat-password').value;

    try {
        if (image != '') { // Si hay una imagen seleccionada
            if (password == '' && repeat_password == '') { // Si no hay contraseña
                try {
                    let image_b64 = await convertToBase64(imageInput);
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/upload_profile_picture', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            var response = JSON.parse(xhr.responseText);
                            if (response.message) {
                                console.log(response.message);
                                try {
                                    var xhr2 = new XMLHttpRequest();
                                    xhr2.open('POST', '/update_profile_data', true);
                                    xhr2.setRequestHeader('Content-Type', 'application/json');
                                    xhr2.onreadystatechange = function () {
                                        if (xhr2 && xhr.readyState === 4 && xhr2.status === 200) {
                                            swal(
                                                'Información actualizada correctamente',
                                                {
                                                    icon: 'success',
                                                    timer: 3000,
                                                    buttons: false,
                                                }
                                            );
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
                                        firstname: firstname,
                                        surname: surname,
                                        username: username,
                                    });
                                    xhr2.send(data);
                                } catch (error) {
                                    console.error(error);
                                    swal({
                                        title: 'Ha ocurrido un error',
                                        text: 'Recargue la página y vuelva a intentar nuevamente',
                                        icon: 'error',
                                        timer: 3000,
                                        buttons: false,
                                    });
                                }
                            } else {
                                console.error(response.error);
                                swal({
                                    title: 'Ha ocurrido un error',
                                    text: 'Recargue la página y vuelva a intentar nuevamente',
                                    icon: 'error',
                                    timer: 3000,
                                    buttons: false,
                                });
                            }
                        }
                    };
                    var data = JSON.stringify({
                        image: image_b64
                    });
                    xhr.send(data);
                } catch (e) {
                    console.error(e);
                    swal({
                        title: 'Ha ocurrido un error',
                        text: 'Recargue la página y vuelva a intentar nuevamente',
                        icon: 'error',
                        timer: 3000,
                        buttons: false,
                    });
                }
            } else if (password && repeat_password) { // Si hay contraseña
                if (password == repeat_password) { // Si son iguales
                    try {
                        let image_b64 = await convertToBase64(imageInput);
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', '/upload_profile_picture', true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                var response = JSON.parse(xhr.responseText);
                                if (response.message) {
                                    console.log(response.message);
                                    try {
                                        var xhr2 = new XMLHttpRequest();
                                        xhr2.open('POST', '/update_profile_data', true);
                                        xhr2.setRequestHeader('Content-Type', 'application/json');
                                        xhr2.onreadystatechange = function () {
                                            if (xhr2 && xhr.readyState === 4 && xhr2.status === 200) {
                                                swal(
                                                    'Información actualizada correctamente',
                                                    {
                                                        icon: 'success',
                                                        timer: 3000,
                                                        buttons: false,
                                                    }
                                                );
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
                                            firstname: firstname,
                                            surname: surname,
                                            username: username,
                                            password: password
                                        });
                                        xhr2.send(data);
                                    } catch (error) {
                                        console.error(error);
                                        swal({
                                            title: 'Ha ocurrido un error',
                                            text: 'Recargue la página y vuelva a intentar nuevamente',
                                            icon: 'error',
                                            timer: 3000,
                                            buttons: false,
                                        });
                                    }
                                } else {
                                    console.error(response.error);
                                    swal({
                                        title: 'Ha ocurrido un error',
                                        text: 'Recargue la página y vuelva a intentar nuevamente',
                                        icon: 'error',
                                        timer: 3000,
                                        buttons: false,
                                    });
                                }
                            }
                        };
                        var data = JSON.stringify({
                            image: image_b64
                        });
                        xhr.send(data);
                    } catch (e) {
                        console.error(e);
                        swal({
                            title: 'Ha ocurrido un error',
                            text: 'Recargue la página y vuelva a intentar nuevamente',
                            icon: 'error',
                            timer: 3000,
                            buttons: false,
                        });
                    }
                } else if (password != repeat_password) { // Si no son iguales
                    swal(
                        'Contraseñas no coinciden',
                        'Por favor, introduce las contraseñas nuevamente.',
                        'error'
                    );
                }
            }
        } else if (image == '') { // Si no hay imagen seleccionada
            if (password == '' && repeat_password == '') { // Si no hay contraseña
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/update_profile_data', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            console.log('a')
                            swal({
                                title: 'Información actualizada correctamente',
                                text: 'Puede cerrar esta ventana',
                                icon: 'success',
                                timer: 3000,
                                buttons: false,
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
                        firstname: firstname,
                        surname: surname,
                        username: username
                    });
                    xhr.send(data);
                } catch (error) {
                    console.error(error);
                    swal({
                        title: 'Ha ocurrido un error',
                        text: 'Recargue la página y vuelva a intentar nuevamente',
                        icon: 'error',
                        timer: 3000,
                        buttons: false,
                    });
                }
            } else if (password  && repeat_password) { // Si hay contraseña
                if (password == repeat_password) { // Si son iguales
                    try {
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', '/update_profile_data', true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                swal({
                                    title: 'Información actualizada correctamente',
                                    text: 'Puede cerrar esta ventana',
                                    icon: 'success',
                                    timer: 3000,
                                    buttons: false,
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
                            firstname: firstname,
                            surname: surname,
                            username: username,
                            password: password
                        });
                        xhr.send(data);
                    } catch (error) {
                        console.error(error);
                        swal({
                            title: 'Ha ocurrido un error',
                            text: 'Recargue la página y vuelva a intentar nuevamente',
                            icon: 'error',
                            timer: 3000,
                            buttons: false,
                        });
                    }
                } else if (password != repeat_password) { // Si no son iguales
                    swal(
                        'Contraseñas no coinciden',
                        'Por favor, introduce las contraseñas nuevamente.',
                        'error'
                    );
                }
            }
        }
    } catch (error) {
        console.error(error);
        swal({
            title: 'Ha ocurrido un error',
            text: 'Recargue la página y vuelva a intentar nuevamente',
            icon: 'error',
            timer: 3000,
            buttons: false,
        });
    }
}


function copyValue() {
  var texto = document.getElementById("usern").value;
  var newUsernameInput = document.getElementById("newusername");

  newUsernameInput.value = texto;

}

function authUpdate () {
    const ver_email     = document.querySelector('#ver-email').value;
    const ver_password  = document.querySelector('#ver-password').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/auth_update', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (xhr.responseText === 'True') {
                try {
                    updatePersonalData();
                } catch (error) {
                    swal({
                        title: 'Ha ocurrido un error',
                        text: 'Recargue la página y vuelva a intentar nuevamente',
                        icon: 'error',
                        timer: 3000,
                        buttons: false,
                    });
                    console.error(error)
                }
            } else if (xhr.responseText === 'False') {
                swal({
                    title: 'Datos erróneos',
                    text: 'El correo o contraseña son incorrectos.',
                    icon: 'error',
                    timer: 3000,
                });
            }
        }
    };

    var data = JSON.stringify({
        ver_email: ver_email,
        ver_password: ver_password
    });
    xhr.send(data);
}

function UpdateUsernameGoogle () {
    const ver_username = document.querySelector('#newusername').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/update_profile_data_google', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (xhr.responseText === 'True') {
                swal({
                    title: 'Información actualizada correctamente',
                    text: 'Puede cerrar esta ventana',
                    icon: 'success',
                    timer: 3000,
                    buttons: false,
                });
            } else if (xhr.responseText === 'False') {
                swal({
                    title:'Datos erróneos',
                    text: 'El usuario parece no cumple con los requerimientos',
                    icon: 'error',
                    timer: 3000,
                });
            }
        }
    };
    var data = JSON.stringify({
        username: ver_username
    });
    xhr.send(data);
}


function authDeactivate () {
    const ver_email = document.querySelector('#ver-deact-email').value;
    const ver_password = document.querySelector('#ver-deact-password').value;

    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/auth_deactivate', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                if (xhr.responseText === 'False') {
                    swal({
                        title: 'Datos erróneos',
                        text: 'El correo o contraseña son incorrectos.',
                        icon: 'error',
                        timer: 3000,
                    });
                } else {
                    swal({
                        title: 'Desactivación exitosa',
                        text: 'Su cuanta ha sido desactivada, esto surtirá efecto la próxima vez que cargue o recargue la página.',
                        icon: 'info'
                    }).then(function() {
                        location.reload();
                    });
                }
            }
        };
        var data = JSON.stringify({
            ver_email: ver_email,
            ver_password: ver_password
        });
        xhr.send(data);
    } catch (error) {
        console.error(error)
        swal({
            title: 'Ha ocurrido un error',
            text: 'Recargue la página y vuelva a intentar nuevamente',
            icon: 'error',
            timer: 3000,
            buttons: false,
        });
    }
}

document.querySelector('#confirm-update-btn').addEventListener('click', authUpdate)
document.querySelector('#confirm-update-btn-google').addEventListener('click', UpdateUsernameGoogle)
document.querySelector('#confirm-deact-btn').addEventListener('click', authDeactivate)