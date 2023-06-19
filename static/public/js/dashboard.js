// tipos MIME para cada tipo de archivo sopportado
const languages = [
    { "type": "text/plain" },              // 0 txt
    { "type": "text/html" },               // 1 html
    { "type": "text/javascript" },         // 2 js
    { "type": "text/css" },                // 3 css
    { "type": "text/x-python" },           // 4 py
    { "type": "application/x-httpd-php" }, // 5 php
    { "type": "text/x-csrc" },             // 6 C
    { "type": "text/x-c++src" },           // 7 C++
    { "type": "text/x-java" },             // 8 java
    { "type": "application/sql" },         // 9 sql
    { "type": "application/json" },        // 10 json
    { "type": "application/xml" },         // 11 xml
    { "type": "text/csv" },                // 12 csv
    { "type": "text/yaml" },               // 13 yaml
    { "type": "text/markdown" },           // 14 md, markdown
    { "type": "text/x-ruby" },             // 15 ruby
    { "type": "text/x-swift" },            // 16 swift
    { "type": "application/typescript" },  // 17 typescript
    { "type": "text/x-go" },               // 18 go
    { "type": "text/x-rustsrc" },          // 19 rust
    { "type": "application/vnd.dart" }     // 20 dart
];

// obtiene el la extension del archivo y consigue su tipo MIME
function getFileType(filename) {
    file = filename.split(".");
    extension = file.length - 1
    mode = file[extension]
    try {
        switch (mode) {
            case 'txt':
                var fileType = languages[0];
                break;
            case 'html':
                var fileType = languages[1];
                break;
            case 'js':
                var fileType = languages[2];
                break;
            case 'javascript':
                var fileType = languages[2];
                break;
            case 'css':
                var fileType = languages[3];
                break;
            case 'python':
                var fileType = languages[4];
                break;
            case 'php':
                var fileType = languages[5];
                break;
            case 'c_cpp':
                var fileType = languages[6];
                break;
            case 'java':
                var fileType = languages[8];
                break;
            case 'sql':
                var fileType = languages[9];
                break;
            case 'json':
                var fileType = languages[10];
                break;
            case 'xml':
                var fileType = languages[11];
                break;
            case 'csv':
                var fileType = languages[12];
                break;
            case 'yaml':
                var fileType = languages[13];
                break;
            case 'markdown':
                var fileType = languages[14];
                break;
            case 'ruby':
                var fileType = languages[15];
                break;
            case 'swift':
                var fileType = languages[16];
                break;
            case 'typescript':
                var fileType = languages[17];
                break;
            case 'golang':
                var fileType = languages[18];
                break;
            case 'rust':
                var fileType = languages[19];
                break;
            case 'dart':
                var fileType = languages[20];
                break;
            default:
                var fileType = languages[0];
                break;
        }
        return fileType;
    } catch (e) {
        console.log(e.message)
    }
}

function downloadFile(filename) {
    var contenido = "";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/download_file', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            contenido = this.responseText;
            try {
                fileType = getFileType(filename)
                // Crear un objeto Blob con el contenido
                var blob = new Blob([contenido], { type: fileType.type });

                // Crear un objeto URL del blob
                var url = URL.createObjectURL(blob);

                // Crear un elemento <a> para descargar el archivo
                var a = document.createElement("a");
                a.href = url;
                a.download = filename;

                // Agregar el elemento <a> al DOM y hacer clic en él
                document.body.appendChild(a);
                a.click();

                // Liberar el objeto URL
                URL.revokeObjectURL(url);
            } catch (e) {
                console.log(e.message)
            }
        }
    };
    var data = JSON.stringify({
        filename: filename,
    });
    xhr.send(data);
}

// elimina permanentemente el archivo
function deleteFile(filename) {
    swal(
        "Estás seguro de que quieres eliminar este archivo?", {
        buttons: {
            cancel: "Cancelar",
            confirm: "Eliminar"
        }
    }
    ).then((value) => {
        switch (value) {
            case true:
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/perm_delete', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            swal(`Archivo ${file} eliminado exitosamente.`, {
                                buttons: false,
                                icon: 'success'
                            })
                            .then(function () {
                                location.reload();
                            })
                            console.log(this.responseText);
                        }
                    };
                    var data = JSON.stringify({
                        filename: file,
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

// mueve el archivo a la basura
function moveToTrash(file) {
    swal(
        "Estás seguro de que quieres eliminar este archivo?", {
        buttons: {
            cancel: "Cancelar",
            confirm: "Eliminar"
        }
    }).then((value) => {
        switch (value) {
            case true:
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/move_to_trash', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            swal(`Archivo ${file} eliminado exitosamente.`, {
                                buttons: false,
                                icon: 'success'
                            })
                            .then(function () {
                                location.reload();
                            })
                            console.log(this.responseText);
                        }
                    };
                    var data = JSON.stringify({
                        filename: file,
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

// modifica los datos de la licencia
function updateLicence(licence) {
    const price = document.querySelector('#update-price-' + licence).value;
    const max_storage = document.querySelector('#update-max_storage-' + licence).value;

    const support_24_7 = document.querySelector('#update-support_24_7-' + licence);
    const auto_backups = document.querySelector('#update-auto_backups-' + licence);
    const secure_access = document.querySelector('#update-secure_access-' + licence);

    const file_capacity = document.querySelector('#update-file_capacity-' + licence).value;

    let support_24_7Value = support_24_7.options[support_24_7.selectedIndex].value;
    let auto_backupsValue = auto_backups.options[auto_backups.selectedIndex].value;
    let secure_accessValue = secure_access.options[secure_access.selectedIndex].value;

    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/control_update_licence', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr && xhr.readyState === 4 && xhr.status === 200) {
                swal({
                    title: 'La información de la licencia se ha actualizado correctamente.',
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
            licence: licence,
            price: parseFloat(price),
            max_storage: parseInt(max_storage),
            support_24_7: support_24_7Value,
            auto_backups: auto_backupsValue,
            secure_access: secure_accessValue,
            file_capacity: parseInt(file_capacity)
        });
        xhr.send(data);
    } catch (error) {
        console.error(error);
    }
}

// envia el reporte de error
function sendErrorReport() {
    let topic = document.getElementById('error-topic').value;
    let report = document.getElementById('report-body').value;

    if (!report || !topic) {
        swal("Debe proporcionar una descripción del error", {
            buttons: false,
            timer: 3000,
            icon: 'error'
        });
    } else {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/send_report', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    swal(
                        'Reporte enviado correctamente.',
                        {
                            buttons: false,
                            icon: 'success',
                            timer: 3000
                        }
                    )
                } else {
                    swal(
                        "Ha ocurrido un error",
                        "Recargue la página e intente de nuevo.",
                        {
                            buttons: false,
                            timer: 3000,
                            icon: 'error'
                        }
                    );
                }
            };
            var data = JSON.stringify({
                topic: topic,
                report: report
            });
            xhr.send(data);
        } catch (e) {
            console.log(e.message)
            swal(
                "Ha ocurrido un error",
                "Error: " + e.message,
                {
                    buttons: false,
                    timer: 3000,
                    icon: 'error'
                }
            );
        }
    }
}


document.getElementById("file-input").addEventListener("change", function() {
    var file = this.files[0];
    if (file) {
        var formData = new FormData();
        formData.append("file", file);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload_file", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = xhr.responseText;
                if (response === 'Has superado el espacio máximo') {
                    swal({
                        title: 'Error',
                        text: 'Has superado el espacio máximo',
                        icon: 'error',
                        confirmButtonText: 'Cerrar'
                    });
                } else if (response === 'Archivo subido correctamente') {
                    swal({
                        title: 'Éxito',
                        text: 'Archivo subido correctamente',
                        icon: 'success',
                        confirmButtonText: 'Cerrar'
                    }).then(function() {
                        location.reload();
                    });
                } else if (response === 'Extensión de archivo no permitida') {
                    swal({
                        title: 'Error',
                        text: 'Extensión de archivo no permitida',
                        icon: 'error',
                        confirmButtonText: 'Cerrar'
                    });
                } else if (response === 'Error al guardar el archivo') {
                    swal({
                        title: 'Error',
                        text: 'Error al guardar el archivo',
                        icon: 'error',
                        confirmButtonText: 'Cerrar'
                    });
                } else if (response === 'No se recibió ningún archivo') {
                    swal({
                        title: 'Error',
                        text: 'No se recibió ningún archivo',
                        icon: 'error',
                        confirmButtonText: 'Cerrar'
                    });
                } else if (response === 'El archivo excede el tamaño máximo permitido por tu cuota') {
                                swal({
                                    title: "Error de almacenamiento",
                                    text: "No se pudo guardar el archivo porque se ha excedido el espacio disponible.",
                                    icon: "error",
                                    buttons: {
                                        cerrar: {
                                            text: "Cerrar",
                                            className: "swal-button--cancel",
                                            visible: true,
                                            closeModal: true,
                                        },
                                        premium: {
                                            text: "C-Cloud Premium",
                                            className: "swal-button--premium",
                                            visible: true,
                                            closeModal: false,
                                        }
                                    },
                                    closeOnClickOutside: false,
                                    closeOnEsc: false,
                                    dangerMode: true,
                                });

                } else if(response === 'No se puede subir porque supera el espacio máximo de tu cuota'){
                            swal({
                                    title: "Error de almacenamiento",
                                    text: "No es posible guardar los cambios de tu archivo porque supera el máximo de espacio permitido por tu cuota",
                                    icon: "error",
                                    buttons: {
                                        cerrar: {
                                            text: "Cerrar",
                                            className: "swal-button--cancel",
                                            visible: true,
                                            closeModal: true,
                                        },
                                        premium: {
                                            text: "C-Cloud Premium",
                                            className: "swal-button--premium",
                                            visible: true,
                                            closeModal: false,
                                        }
                                    },
                                    closeOnClickOutside: false,
                                    closeOnEsc: false,
                                    dangerMode: true,
                                });

                }else{
                    console.log('Respuesta desconocida: ' + response);
                }

            }

        };
        xhr.send(formData);
    }
});
// añade el evento de enviar reporte a los botones send-report-btn
document.getElementById('send-report-btn').addEventListener('click', sendErrorReport);