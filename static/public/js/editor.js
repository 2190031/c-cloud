var editor = ace.edit("editor");

// Lista de lenguajes
const languages = [
    { "type": "text/plain" },  // 0 txt
    { "type": "text/html" },  // 1 html
    { "type": "text/javascript" },  // 2 js
    { "type": "text/css" },  // 3 css
    { "type": "text/x-python" },  // 4 py
    { "type": "application/x-httpd-php" },  // 5 php
    { "type": "text/x-csrc" },  // 6 C
    { "type": "text/x-c++src" },  // 7 C++
    { "type": "text/x-java" },  // 8 java
    { "type": "application/sql" },  // 9 sql
    { "type": "application/json" },  // 10 json
    { "type": "application/xml" },  // 11 xml
    { "type": "text/csv" },  // 12 csv
    { "type": "text/yaml" },  // 13 yaml
    { "type": "text/markdown" },  // 14 md, markdown
    { "type": "text/x-ruby" },  // 15 ruby
    { "type": "text/x-swift" },  // 16 swift
    { "type": "application/typescript" },  // 17 typescript
    { "type": "text/x-go" },  // 18 go
    { "type": "text/x-rustsrc" }, // 19 rust
    { "type": "application/vnd.dart" } // 20 dart
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
    let ModeSelValue = document.getElementById('select-mode');
    let mode = ModeSelValue.options[ModeSelValue.selectedIndex].value;
    let ThemeSelValue = document.getElementById('select-theme');
    let theme = ThemeSelValue.options[ThemeSelValue.selectedIndex].value;
    console.log(mode);
    if (mode != "") {
        editor.session.setMode("ace/mode/" + mode);
    }
    if (theme != "") {
        editor.setTheme("ace/theme/" + theme);
    }
});

// Cambia el modo de lenguaje de la pagina al cambiar el select
document.getElementById('select-mode').addEventListener('change', function () {
    let ModeSelValue = document.getElementById('select-mode');
    let mode = ModeSelValue.options[ModeSelValue.selectedIndex].value;
    if (mode != "") {
        editor.session.setMode("ace/mode/" + mode);
    }
});

// Cambia el tema de la pagina al cambiar el select
document.getElementById('select-theme').addEventListener('change', function () {
    let ThemeSelValue = document.getElementById('select-theme');
    let theme = ThemeSelValue.options[ThemeSelValue.selectedIndex].value;
    if (theme != "") {
        editor.setTheme("ace/theme/" + theme);
    }
});

// Descarga el documento con su titulo y en su lenguaje correspondiente
// document.getElementById('download-btn').addEventListener('click', download());

function download() {
    var contenido = ace.edit("editor").getValue();
    let ModeSelValue = document.getElementById('select-mode');
    console.log(ModeSelValue)
    let mode = ModeSelValue.options[ModeSelValue.selectedIndex].value;
    console.log()
    let filename = document.getElementById('filename').value;
    console.log(filename)
    if (filename == "" || filename == null || !filename) {
        console.log("Error")
    } else {
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

        var contenido = ace.edit("editor").getValue();

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
    }
}
