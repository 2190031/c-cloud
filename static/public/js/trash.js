function confirmDelete(file) {
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

function confirmRestore(file) {
    swal(
        "Estás seguro de que quieres restaurar este archivo?", {
        buttons: {
            cancel: "Cancelar",
            confirm: "Restaurar"
        }
    }
    ).then((value) => {
        switch (value) {
            case true:
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/restore_file', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            swal(`Archivo ${file} restaurado exitosamente.`)
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