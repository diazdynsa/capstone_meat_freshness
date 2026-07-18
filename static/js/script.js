const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const uploadSection = document.querySelector('.upload-section');
const loadingSection = document.getElementById('loading-area');
const resultSection = document.getElementById('result-area');
const previewImg = document.getElementById('preview-img');
const statusBadge = document.getElementById('status-badge');
const confidenceVal = document.getElementById('confidence-val');
const confidenceBar = document.getElementById('confidence-bar');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) { dropArea.classList.add('dragover'); }
function unhighlight(e) { dropArea.classList.remove('dragover'); }

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Handle file input change
fileInput.addEventListener('change', function() {
    handleFiles(this.files);
});

function handleFiles(files) {
    if (files.length === 0) return;
    const file = files[0];
    
    // Validasi file image
    if (!file.type.startsWith('image/')) {
        alert('Mohon unggah file gambar yang valid (JPG, PNG).');
        return;
    }

    uploadImage(file);
}

function uploadImage(file) {
    // UI Transitions
    uploadSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    // Kirim secara asynchronous menggunakan Fetch API (AJAX)
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            resetApp();
            return;
        }
        showResult(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Terjadi kesalahan saat menghubungi server.');
        resetApp();
    });
}

function showResult(data) {
    loadingSection.classList.add('hidden');
    resultSection.classList.remove('hidden');

    // Set Image (add timestamp to prevent caching)
    previewImg.src = data.image_url + "?t=" + new Date().getTime();

    // Set Data
    const label = data.class;
    statusBadge.textContent = label;
    
    // Style Badge based on result
    statusBadge.className = 'status-badge'; // reset
    let colorHex = '#2a9d8f';
    if (label === 'Fresh') {
        statusBadge.classList.add('fresh');
        colorHex = '#2a9d8f';
    } else if (label === 'Half-Fresh') {
        statusBadge.classList.add('half');
        colorHex = '#e9c46a';
    } else {
        statusBadge.classList.add('spoiled');
        colorHex = '#e76f51';
    }

    // Set Confidence
    confidenceVal.textContent = data.confidence + '%';
    
    // Animate Progress Bar
    setTimeout(() => {
        confidenceBar.style.width = data.confidence + '%';
        confidenceBar.style.backgroundColor = colorHex;
    }, 150);
}

function resetApp() {
    resultSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
    confidenceBar.style.width = '0%';
    fileInput.value = '';
}
