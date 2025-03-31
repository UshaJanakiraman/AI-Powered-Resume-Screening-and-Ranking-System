document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("resumeInput");
    const dropArea = document.getElementById("drop-area");
    const fileNameDisplay = document.getElementById("file-name");

    // File selection event
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileNameDisplay.innerHTML = `<strong>Selected File:</strong> ${fileInput.files[0].name}`;
        }
    });

    // Drag and Drop events
    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.style.backgroundColor = "#d6e4f0";
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.style.backgroundColor = "#e9ecef";
    });

    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.style.backgroundColor = "#e9ecef";

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileNameDisplay.innerHTML = `<strong>Selected File:</strong> ${files[0].name}`;
        }
    });
});
