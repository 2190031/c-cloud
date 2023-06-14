function downloadFile(filename) {
    console.log(filename);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/download_file', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            swal(
                `Archivo ${filename} descargado correctamente.\nRevise su carpeta de Descargas.`,
                {
                    buttons: false,
                    icon: 'success',
                    timer: 3000
                }
            )
        } else {
            swal(
                'Ha ocurrido un error.',
                {
                    buttons: false,
                    icon: 'error',
                    timer: 3000
                }
            )
        }
    };

    // Generar el nombre del archivo con la fecha actual en JavaScript
    var currentDate = new Date();
    var formattedDate = currentDate.toISOString().slice(0, 19).replace(/:/g, '_');
    var extensionIndex = filename.lastIndexOf('.');
    var filenameWithoutExtension = filename.slice(0, extensionIndex);
    var fileExtension = filename.slice(extensionIndex);
    var filenameWithDate = filenameWithoutExtension + '_' + formattedDate + fileExtension;
    var url = 'http://https://wady01.pythonanywhere.com/userFiles/_username_/savedFiles/' + encodeURIComponent(filenameWithDate);
    xhr.send('url=' + encodeURIComponent(url));
}

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
                            swal(`Archivo ${file} eliminado exitosamente.`)
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

function moveToTrash(file) {
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
                    xhr.open('POST', '/move_to_trash', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            swal(`Archivo ${file} eliminado exitosamente.`)
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