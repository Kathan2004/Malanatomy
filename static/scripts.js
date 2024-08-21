
document.querySelector('.upload-area').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        console.log(`File selected: ${file.name}`);
        
        // Create a FormData object to send the file via POST request
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${file.name}_report.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('Scan completed! Downloading report...');
        })
        .catch(error => {
            console.error('Error during file upload:', error);
            alert('An error occurred during the upload. Please try again.');
        });
    }
});
