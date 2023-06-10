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

async function updatePersonalData() {
    let imageInput = document.querySelector('#upload');
    let image = imageInput.value;
    let firstname = document.querySelector('#firstname').value;
    let surname = document.querySelector('#surname').value;
    let username = document.querySelector('#username').value;
    let password = document.querySelector('#new-password').value;
    let repeat_password = document.querySelector('#repeat-password').value;

    try {
        if (image != '' || image != undefined || image != null) { // Si hay una imagen seleccionada
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
                                }
                            } else {
                                console.error(response.error);
                            }
                        }
                    };
                    var data = JSON.stringify({
                        image: image_b64
                    });
                    xhr.send(data);
                } catch (e) {
                    console.error(e);
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
                                    }
                                } else {
                                    console.error(response.error);
                                }
                            }
                        };
                        var data = JSON.stringify({
                            image: image_b64
                        });
                        xhr.send(data);
                    } catch (e) {
                        console.error(e);
                    }
                } else if (password != repeat_password) { // Si no son iguales
                    swal(
                        'Contraseñas no coinciden',
                        'Por favor, introduce las contraseñas nuevamente.',
                        'error'
                    );                    
                }
            } 
        } else if (image == '' || image == undefined || image == null) { // Si no hay imagen seleccionada
            if (password == '' && repeat_password == '') { // Si no hay contraseña
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
                        }
                    };
                    var data = JSON.stringify({
                        fname: firstname,
                        sname: surname,
                        username: username
                    });
                    xhr.send(data);
                } catch (error) {
                    console.error(error);
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
                            }
                        };
                        var data = JSON.stringify({
                            fname: firstname,
                            sname: surname,
                            username: username,
                            password: password
                        });
                        xhr.send(data);
                    } catch (error) {
                        console.error(error);
                    }
                } else if (password != repeat_password) { // Si no son iguales
                    swal(
                        'Contraseñas no coinciden',
                        'Por favor, introduce las contraseñas nuevamente.',
                        'error'
                    );
                }
            }
        } else {
            throw new Error;
        }
    } catch (error) {
        console.error(error);
    }
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

// function updatePersonalData() {
//     let imageInput = document.querySelector('#upload');
//     let image = imageInput.value;
//     let firstname = document.querySelector('#firstname').value;
//     let surname = document.querySelector('#surname').value;
//     let username = document.querySelector('#username').value;
//     let password = document.querySelector('#new-password').value;
//     let repeat_password = document.querySelector('#repeat-password').value;

//     try {
//         if (image != '' || image != undefined || image != null) { // Si hay una imagen seleccionada
//             if (password == '' && repeat_password == '') { // Si no hay contraseña
//                 try {
//                     let image_b64 = await convertToBase64(imageInput);

//                     var xhr = new XMLHttpRequest();
//                     xhr.open('POST', '/upload_profile_picture', true);
//                     xhr.setRequestHeader('Content-Type', 'application/json');
//                     xhr.onreadystatechange = function () {
//                         if (xhr.readyState === 4 && xhr.status === 200) {
//                             var response = JSON.parse(xhr.responseText);
//                             if (response.message) {
//                                 console.log(response.message);
//                                 try {
//                                     var xhr2 = new XMLHttpRequest();
//                                     xhr2.open('POST', '/update_profile_data', true);
//                                     xhr2.setRequestHeader('Content-Type', 'application/json');
//                                     xhr2.onreadystatechange = function () {
//                                         if (xhr2 && xhr.readyState === 4 && xhr2.status === 200) {
//                                             swal(
//                                                 'Información actualizada correctamente',
//                                                 {
//                                                     icon: 'success',
//                                                     timer: 3000,
//                                                     buttons: false,
//                                                 }
//                                             );
//                                         }
//                                     };
//                                     var data = JSON.stringify({
//                                         firstname: firstname,
//                                         surname: surname,
//                                         username: username,
//                                     });
//                                     xhr2.send(data);
//                                 } catch (error) {
//                                     console.error(error);
//                                 }
//                             } else {
//                                 console.error(response.error);
//                             }
//                         }
//                     };
//                     var data = JSON.stringify({
//                         image: image_b64
//                     });
//                     xhr.send(data);
//                 } catch (e) {
//                     console.error(e);
//                 }
//             } else if (password && repeat_password) { // Si hay contraseña
//                 if (password == repeat_password) { // Si son iguales
//                     try {
//                         let image_b64 = await convertToBase64(imageInput);
    
//                         var xhr = new XMLHttpRequest();
//                         xhr.open('POST', '/upload_profile_picture', true);
//                         xhr.setRequestHeader('Content-Type', 'application/json');
//                         xhr.onreadystatechange = function () {
//                             if (xhr.readyState === 4 && xhr.status === 200) {
//                                 var response = JSON.parse(xhr.responseText);
//                                 if (response.message) {
//                                     console.log(response.message);
//                                     try {
//                                         var xhr2 = new XMLHttpRequest();
//                                         xhr2.open('POST', '/update_profile_data', true);
//                                         xhr2.setRequestHeader('Content-Type', 'application/json');
//                                         xhr2.onreadystatechange = function () {
//                                             if (xhr2 && xhr.readyState === 4 && xhr2.status === 200) {
//                                                 swal(
//                                                     'Información actualizada correctamente',
//                                                     {
//                                                         icon: 'success',
//                                                         timer: 3000,
//                                                         buttons: false,
//                                                     }
//                                                 );
//                                             }
//                                         };
//                                         var data = JSON.stringify({
//                                             firstname: firstname,
//                                             surname: surname,
//                                             username: username,
//                                             password: password
//                                         });
//                                         xhr2.send(data);
//                                     } catch (error) {
//                                         console.error(error);
//                                     }
//                                 } else {
//                                     console.error(response.error);
//                                 }
//                             }
//                         };
//                         var data = JSON.stringify({
//                             image: image_b64
//                         });
//                         xhr.send(data);
//                     } catch (e) {
//                         console.error(e);
//                     }
//                 } else if (password != repeat_password) { // Si no son iguales
//                     swal(
//                         'Contraseñas no coinciden',
//                         'Por favor, introduce las contraseñas nuevamente.',
//                         'error'
//                     );                    
//                 }
//             } 
//         } else if (image == '' || image == undefined || image == null) { // Si no hay imagen seleccionada
//             if (password == '' && repeat_password == '') { // Si no hay contraseña
//                 try {
//                     var xhr = new XMLHttpRequest();
//                     xhr.open('POST', '/update_profile_data', true);
//                     xhr.setRequestHeader('Content-Type', 'application/json');
//                     xhr.onreadystatechange = function () {
//                         if (xhr.readyState === 4 && xhr.status === 200) {
//                             swal({
//                                 title: 'Información actualizada correctamente',
//                                 text: 'Puede cerrar esta ventana',
//                                 icon: 'success',
//                                 timer: 3000,
//                                 buttons: false,
//                             });
//                         }
//                     };
//                     var data = JSON.stringify({
//                         fname: firstname,
//                         sname: surname,
//                         username: username
//                     });
//                     xhr.send(data);
//                 } catch (error) {
//                     console.error(error);
//                 }
//             } else if (password  && repeat_password) { // Si hay contraseña
//                 if (password == repeat_password) { // Si son iguales
//                     try {
//                         var xhr = new XMLHttpRequest();
//                         xhr.open('POST', '/update_profile_data', true);
//                         xhr.setRequestHeader('Content-Type', 'application/json');
//                         xhr.onreadystatechange = function () {
//                             if (xhr.readyState === 4 && xhr.status === 200) {
//                                 swal({
//                                     title: 'Información actualizada correctamente',
//                                     text: 'Puede cerrar esta ventana',
//                                     icon: 'success',
//                                     timer: 3000,
//                                     buttons: false,
//                                 });
//                             }
//                         };
//                         var data = JSON.stringify({
//                             fname: firstname,
//                             sname: surname,
//                             username: username,
//                             password: password
//                         });
//                         xhr.send(data);
//                     } catch (error) {
//                         console.error(error);
//                     }
//                 } else if (password != repeat_password) { // Si no son iguales
//                     swal(
//                         'Contraseñas no coinciden',
//                         'Por favor, introduce las contraseñas nuevamente.',
//                         'error'
//                     );
//                 }
//             }
//         } else {
//             throw new Error;
//         }
//     } catch (error) {
//         console.error(error);
//     }
// }

function authDeactivate () {
    const ver_email     = document.querySelector('#ver-deact-email').value;
    const ver_password  = document.querySelector('#ver-deact-password').value;

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

document.querySelector('#confirm-update-btn').addEventListener('click', authUpdate)
document.querySelector('#confirm-deact-btn').addEventListener('click', authDeactivate)