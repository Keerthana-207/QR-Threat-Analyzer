document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const filenameSpan = document.getElementById('filename-span');
    const previewWrapper = document.getElementById('preview-wrapper');
    const uploadIcon = document.getElementById('upload-icon');
    const uploadText = document.getElementById('upload-text');

    const analyzerForm = document.getElementById('analyzer-form');
    const uploadCard = document.getElementById('upload-card');
    const loadingCard = document.getElementById('loading-card');

    // Live Change Listener for Selected Image Detection
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (fileInput.files.length > 0) {
                const name = fileInput.files[0].name;
                filenameSpan.innerText = name;
                previewWrapper.classList.remove('d-none');
                uploadIcon.className = "fa-solid fa-file-circle-check fa-3x text-success mb-3";
                uploadText.innerText = "Target locked. Ready to run diagnosis.";
            }
        });
    }

    // Interactive Drag Styling toggles
    if (dropZone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
        });
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
        });
    }

    // Intercepts submit submission to play out an advanced simulated pipeline timeline sequence
    if (analyzerForm) {
        analyzerForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Pause form to run UI animations first
            
            uploadCard.classList.add('d-none');
            loadingCard.classList.remove('d-none');

            // Timeline Sequence Delays
            setTimeout(() => {
                document.getElementById('step-2').classList.add('active');
                document.getElementById('icon-1').innerHTML = '<i class="fa-solid fa-check"></i>';
                document.getElementById('icon-1').style.background = '#198754';
            }, 1200); // Activate step 2 at 1.2 seconds

            setTimeout(() => {
                document.getElementById('step-3').classList.add('active');
                document.getElementById('icon-2').innerHTML = '<i class="fa-solid fa-check"></i>';
                document.getElementById('icon-2').style.background = '#198754';
            }, 2600); // Activate step 3 at 2.6 seconds

            setTimeout(() => {
                // Submit the form data to the actual Python Flask backend view route
                analyzerForm.submit();
            }, 3800); // Complete processing hand-off at 3.8 seconds
        });
    }
});

function copyUrl() {
    const urlText = document.getElementById('decodedUrl').innerText;
    navigator.clipboard.writeText(urlText);
    alert('URL copied to clipboard!');
}