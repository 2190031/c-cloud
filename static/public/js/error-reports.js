function markAsResolved(report) {
    console.log(report)
    try {
        swal(
        "Estás seguro de que quiere marcar este error como resuelto?", {
        buttons: {
            cancel: "Cancelar",
            confirm: "Confirmar"
        }
        }
        ).then((value) => {
            switch (value) {
                case true:
                    try {
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', '/mark_as_resolved', true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                swal('Error resuelto exitosamente.', {
                                    buttons: false,
                                    icon: 'success'
                                }).then(function () {
                                    location.reload();
                                })
                            }
                        };
                        var data = JSON.stringify({
                            report: report,
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
    } catch (error) {
        console.error(error)
    }
}