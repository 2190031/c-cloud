// id's de las opciones de la barra de herramientas del editor
const dropdowns = [
    '#file-dropdown',
    '#preferences-dropdown',
    '#help-dropdown',
]

dropdowns.forEach(dropdown => {
    const dropdownMenu = document.querySelector(`${dropdown}>.dropdown-menu`);
    const dropdownButton = document.querySelector(`${dropdown} button`);

    // funcion de abrir el dropdown del elemento al poner el mouse encima
    function openDropdown() {
        dropdownMenu.classList.add('show');
    }

    // funcion de cerrar el dropdown del elemento al mover el mouse fuera
    function closeDropdown() {
        dropdownMenu.classList.remove('show');
    }

    // agrega los eventos a los eventos de abrir el dropdown
    dropdownButton.addEventListener('click', openDropdown);
    dropdownButton.addEventListener('mouseover', openDropdown);

    // agrega el evento de cerrar el dropdown
    dropdownMenu.addEventListener('mouseleave', closeDropdown);
});

var editor = ace.edit("editor");

// Lista de lenguajes (MIME)
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

// Lista con las posibilidades de temas
const themes = [
    "ambiance",
    "chaos",
    "chrome",
    "clouds",
    "clouds_midnight",
    "cobalt",
    "crimson_editor",
    "dawn",
    "dracula",
    "dreamweaver",
    "eclipse",
    "github",
    "gob",
    "gruvbox",
    "idle_fingers",
    "iplastic",
    "katzenmilch",
    "kr_theme",
    "kuroir",
    "merbivore",
    "merbivore_soft",
    "mono_industrial",
    "monokai",
    "nord_dark",
    "pastel_on_dark",
    "solarized_dark",
    "solarized_light",
    "sqlserver",
    "terminal",
    "textmate",
    "tomorrow",
    "tomorrow_night",
    "tomorrow_night_blue",
    "tomorrow_night_bright",
    "tomorrow_night_eighties",
    "twilight",
    "vibrant_ink",
    "xcode"
];

// Al cargar la pagina toma y coloca el tema y lenguaje de sus selects
document.addEventListener("DOMContentLoaded", function () {
    try {
        let ModeSelValue = document.getElementById('select-mode');
        let mode = ModeSelValue.options[ModeSelValue.selectedIndex].value;
        let ThemeSelValue = document.getElementById('select-theme');
        let theme = ThemeSelValue.options[ThemeSelValue.selectedIndex].value;
        let ThemeFontValue = document.getElementById('font-select');
        let font = ThemeFontValue.options[ThemeFontValue.selectedIndex].value;
        let ThemeSizeValue = document.getElementById('font-select');
        let size = ThemeSizeValue.options[ThemeSizeValue.selectedIndex].value;

        if (mode != "") {
            editor.session.setMode("ace/mode/" + mode);
        }
        if (theme != "") {
            editor.setTheme("ace/theme/" + theme);
        }
        if (font != "") {
            editor.setOptions({
                fontFamily: font,
                fontSize: size
            });
        }
    } catch (e) {
        console.log(e.message)
    }
});

// Cambia el modo de lenguaje de la pagina al cambiar el select
document.getElementById('select-mode').addEventListener('change', function () {
    try {
        let ModeSelValue = document.getElementById('select-mode');
        let mode = ModeSelValue.options[ModeSelValue.selectedIndex].value;
        if (mode != "") {
            editor.session.setMode("ace/mode/" + mode);
        }
    } catch (e) {
        console.log(e.message)
    }
});

function saveTheme() {
    const themeSelect = document.querySelector('#select-theme');
    var theme = themeSelect.value;
    console.log(theme);
}

// Cambia el tema del editor al cambiar el select
document.getElementById('select-theme').addEventListener('change', function () {
    try {
        let ThemeSelValue = document.getElementById('select-theme');
        let theme = ThemeSelValue.options[ThemeSelValue.selectedIndex].value;
        if (theme != "") {
            editor.setTheme("ace/theme/" + theme);
        }
    } catch (e) {
        console.log(e.message);
    }
});

// Cambia la fuente del editor al cambiar el select
document.getElementById('font-select').addEventListener('change', function () {
    try {
        let ThemeFontValue = document.getElementById('font-select');
        let font = ThemeFontValue.options[ThemeFontValue.selectedIndex].value;
        if (font != "") {
            editor.setOptions({
                fontFamily: font + ", monospace"
            });
        }
    } catch (e) {
        console.log(e.message);
    }
});

// Cambia el tamaño de la fuente del editor al cambiar el select
document.getElementById('font-size-select').addEventListener('change', function () {
    try {
        let ThemeSizeValue = document.getElementById('font-size-select');
        let size = ThemeSizeValue.options[ThemeSizeValue.selectedIndex].value;
        if (size != "") {
            editor.setOptions({
                fontSize: size
            });
        }
    } catch (e) {
        console.log(e.message);
    }
});

// establece el lenguaje del documento y el modo del editor
function getFileType(mode) {
    let ModeSelValue = document.getElementById('select-mode');
    mode = mode || ModeSelValue.options[ModeSelValue.selectedIndex].value;
    console.log(mode);

    try {
        switch (mode) {
            case 'txt':
                var fileType = languages[0];
                var fileExtension = 'txt';
                break;
            case 'html':
                var fileType = languages[1];
                var fileExtension = 'html';
                break;
            case 'js':
                var fileType = languages[2];
                var fileExtension = 'js';
                break;
            case 'javascript':
                var fileType = languages[2];
                var fileExtension = 'js';
                break;
            case 'css':
                var fileType = languages[3];
                var fileExtension = 'css';
                break;
            case 'python':
                var fileType = languages[4];
                var fileExtension = 'py';
                break;
            case 'php':
                var fileType = languages[5];
                var fileExtension = 'php';
                break;
            case 'c_cpp':
                var fileType = languages[6];
                var fileExtension = 'c';
                break;
            case 'java':
                var fileType = languages[8];
                var fileExtension = 'java';
                break;
            case 'sql':
                var fileType = languages[9];
                var fileExtension = 'sql';
                break;
            case 'json':
                var fileType = languages[10];
                var fileExtension = 'json';
                break;
            case 'xml':
                var fileType = languages[11];
                var fileExtension = 'xml';
                break;
            case 'csv':
                var fileType = languages[12];
                var fileExtension = 'csv';
                break;
            case 'yaml':
                var fileType = languages[13];
                var fileExtension = 'yaml';
                break;
            case 'markdown':
                var fileType = languages[14];
                var fileExtension = 'md';
                break;
            case 'ruby':
                var fileType = languages[15];
                var fileExtension = 'rb';
                break;
            case 'swift':
                var fileType = languages[16];
                var fileExtension = 'swift';
                break;
            case 'typescript':
                var fileType = languages[17];
                var fileExtension = 'ts';
                break;
            case 'golang':
                var fileType = languages[18];
                var fileExtension = 'go';
                break;
            case 'rust':
                var fileType = languages[19];
                var fileExtension = 'rs';
                break;
            case 'dart':
                var fileType = languages[20];
                var fileExtension = 'dart';
                break;
            default:
                var fileType = languages[0];
                var fileExtension = 'txt';
                break;
        }
        return [fileType, fileExtension];
    } catch (e) {
        console.log(e.message)
    }
}

// salva el archivo
function createFile() {
    var content = ace.edit("editor").getValue();
    let filename = document.getElementById('filename').value;
    let selMode = document.getElementById('select-mode');
    let mode = selMode.options[selMode.selectedIndex].value;
    [fileType, extension] = getFileType(mode)
    console.log(extension);

    if (!filename) {
        swal("Debe darle nombre al archivo", {
            buttons: false,
            timer: 3000,
            icon: 'warning'
        });
    } else {
        try {
            console.log('Guardando...');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/create_file', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        console.log(xhr.responseText);
                        if (xhr.responseText === 'File saved successfully') {
                            swal("Guardado correctamente", {
                                buttons: false,
                                timer: 3000,
                                icon: 'success'
                            });
                        } else if (xhr.responseText === 'File created successfully') {
                            swal("Archivo creado correctamente", {
                                buttons: false,
                                timer: 3000,
                                icon: 'success'
                            });
                        } else if (xhr.responseText === 'Has superado el espacio máximo') {
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
                        } else if(xhr.responseText === 'El archivo excede el tamaño máximo permitido'){
                            swal({
                                    title: "Error de almacenamiento",
                                    text: "Este archivo excede el máximo de espacio limitado por archivo según tu cuota",
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
                        } else {
                            swal("Ha ocurrido un error", {
                                buttons: false,
                                timer: 3000,
                                icon: 'error'
                            });
                        }
                    } else {
                        swal("Ha ocurrido un error", {
                            buttons: false,
                            timer: 3000,
                            icon: 'error'
                        });
                    }
                }
            };
            var data = JSON.stringify({
                filename: filename,
                extension: extension,
                content: content
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


// Descarga el documento con su titulo y en su lenguaje correspondiente
function download() {
    var contenido = ace.edit("editor").getValue();
    let filename = document.getElementById('filename').value;
    console.log(filename)
    if (filename == "" || filename == null || !filename) {
        console.log("Error");
        swal("Debe darle nombre al archivo", {
            buttons: false,
            timer: 3000,
            icon: 'warning'
        });
    } else {
        try {
            [fileType, fileExtension] = getFileType()

            // Crear un objeto Blob con el contenido
            var blob = new Blob([contenido], fileType);

            // Crear un objeto URL del blob
            var url = URL.createObjectURL(blob);

            // Crear un elemento <a> para descargar el archivo
            var a = document.createElement("a");
            a.href = url;
            a.download = filename + "." + fileExtension;

            // Agregar el elemento <a> al DOM y hacer clic en él
            document.body.appendChild(a);
            a.click();

            // Liberar el objeto URL
            URL.revokeObjectURL(url);
        } catch (e) {
            console.log(e.message)
        }

    }
}

function aceLangExt(extension) {
    let mode;
    try {
        switch (extension) {
            case 'txt':
                mode = "text";
                return mode;
            case 'js':
                mode = "javascript";
                return mode;
            case 'py':
                mode = "python";
                return mode;
            case 'md':
                mode = "markdown";
                return mode;
            case 'rb':
                mode = "ruby";
                return mode;
            case 'ts':
                mode = "typescript";
                return mode;
            case 'rs':
                mode = "rust";
                return mode;
        }
    } catch (e) {

    }
}

// abre el archivo en el editor y establece su modo por extension
function loadFile(value) {
    var filename = value;
    console.log(filename);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/load_file', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var content = xhr.responseText;
            let name = filename.split('.')
            let extension = name.at(-1);
            let mode = aceLangExt(extension);
            const ModeSelValue = document.getElementById('select-mode');
            ModeSelValue.value = mode;
            editor.session.setMode("ace/mode/" + mode);
            name.pop()
            document.getElementById('filename').value = name;
            editor.setValue(content);
        }
    };
    xhr.send('filename=' + filename);
}

// envia reporte de error
function sendErrorReport() {
    let topic = document.getElementById('error-topic').value;
    let report = document.getElementById('report').value;

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
                    {
                        buttons: false,
                        timer: 3000,
                        icon: 'error'
                    });
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

// guardan las preferencias visuales del usuario
function savePreference() {
    const font = document.getElementById('font-select').value;
    const size = document.getElementById('font-size-select').value;
    const theme = document.getElementById('select-theme').value;
    try {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/save_preferences', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                swal(
                    'Configuración guardada correctamente.',
                    {
                        buttons: false,
                        icon: 'success',
                        timer: 3000
                    }
                )
                editor.setOptions({
                    fontFamily: font
                });
                editor.setFontSize(size);
            } else {
                 swal(
                "Ha ocurrido un error",
                {
                    buttons: false,
                    timer: 3000,
                    icon: 'error'
                });
            }
        };
        var data = JSON.stringify({
            font: font,
            size: size,
            theme: theme,
        });
        xhr.send(data);
    } catch (e) {
        console.log(e);
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

// agrega los eventos a sus botones
document.getElementById('download-btn').addEventListener('click', download);
document.getElementById('save-btn').addEventListener('click', createFile);
document.getElementById('send-report-btn').addEventListener('click', sendErrorReport);
document.getElementById('save-preference-btn').addEventListener('click', savePreference);

document.addEventListener("keydown", function (event) {
    // detecta Ctrl+S (salvar)
    if (event.ctrlKey && event.key === "s") {
        event.preventDefault(); // Prevent the default behavior of the browser
        createFile();
    }

    // detecta Ctrl+O (abrir)
    if (event.ctrlKey && event.key === "o") {
        event.preventDefault(); // Prevent the default behavior of the browser
        // Trigger the file input click event to open the file dialog
        document.getElementById("open-file-btn").click();
    }

    // detecta Ctrl+L (cambiar lenguaje del documento)
    if (event.ctrlKey && event.key === "l") {
        event.preventDefault(); // Prevent the default behavior of the browser
        // Trigger the file input click event to open the file dialog
        document.getElementById("change-lang-btn").click();
    }

    // detecta Ctrl+D (descargar)
    if (event.ctrlKey && event.key === "d") {
        event.preventDefault(); // Prevent the default behavior of the browser
        // Trigger the file input click event to open the file dialog
        document.getElementById("download-btn").click();
    }

    // detecta Ctrl+P (cambiar tema)
    if (event.ctrlKey && event.key === "p") {
        event.preventDefault(); // Prevent the default behavior of the browser
        // Trigger the file input click event to open the file dialog
        document.getElementById("change-theme-btn").click();
    }

    // detecta Ctrl+H (comandos)
    if (event.ctrlKey && event.key === "h") {
        event.preventDefault(); // Prevent the default behavior of the browser
        // Trigger the file input click event to open the file dialog
        document.getElementById("show-commands-btn").click();
    }
});