function updateButton() {
    const file = document.querySelector('.upload-input').files[0];
    const button = document.querySelector(".btn");
    const result = document.querySelector('span');

    var file_format = "";

    if (file) {
        file_format = file.name.split('.').pop();
    }

    if (file && file.name.length != 0 && file_format == 'h5') {
        result.innerHTML = file.name;
        result.classList.remove("text-danger");
        result.classList.add("text-success");
        button.disabled = false;
    } else {
        button.disabled = true;
        result.innerHTML = "No file";
        result.classList.remove("text-success");
        result.classList.add("text-danger");
    }
}
