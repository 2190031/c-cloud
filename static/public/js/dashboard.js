function downloadFile(filename) {
    console.log(filename);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/download_file', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        swal(
            `Archivo ${filename} descargado correctamente.`,
            {
                buttons: false,
                icon: 'success',
                timer: 3000
            }
        )
    } else {
        swal(
            'Ha ocurrido un error.\nRevise su carpeta de Descargas.',
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
    var url = 'http://127.0.0.1:5000/userFiles/MR/savedFiles/' + encodeURIComponent(filenameWithDate);
    xhr.send('url=' + encodeURIComponent(url));  
}