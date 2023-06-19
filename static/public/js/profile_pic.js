// (no google) carga la foto de perfil del usuario
function loadImage() {
    fetch('/get_profile_pic')
    .then(response => response.json())
    .then(data => {
        // Obtener la imagen base64 de la respuesta
        const imageBase64 = data.image;

        // Crear un elemento de imagen y asignar la imagen base64 como su fuente
        const img = document.querySelector('#profile-picture');
        const img2 = document.querySelector('#profile-picture-display');
        img.src = `data:image/png;base64, ${imageBase64}`;
        if (img2) {
            img2.src = `data:image/png;base64, ${imageBase64}`;
        }
    }).catch(error => {});
}

// Llamar a la función para cargar la imagen cuando sea necesario
document.addEventListener('DOMContentLoaded', loadImage);