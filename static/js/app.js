document.addEventListener('DOMContentLoaded', () => {
    const previewBtn = document.getElementById('preview-btn');
    const generateBtn = document.getElementById('generate-btn');
    const form = document.getElementById('cert-form');
    const iframe = document.getElementById('preview-frame');
    const loader = document.getElementById('loader');
    const statusMsg = document.getElementById('status-message');
    const dataTableBody = document.querySelector('#data-table tbody');

    const showMessage = (msg, isError = false) => {
        statusMsg.textContent = msg;
        statusMsg.className = `status-message ${isError ? 'error' : 'success'}`;
        statusMsg.classList.remove('hidden');
        setTimeout(() => {
            statusMsg.classList.add('hidden');
        }, 8000);
    };

    const loadPreview = async () => {
        const formData = new FormData(form);
        loader.style.display = 'block';
        iframe.style.opacity = '0.3';
        
        try {
            const response = await fetch('/api/preview', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'Failed to generate preview');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            iframe.src = url;
            iframe.onload = () => {
                loader.style.display = 'none';
                iframe.style.opacity = '1';
            };
        } catch (error) {
            loader.style.display = 'none';
            iframe.style.opacity = '1';
            showMessage(error.message, true);
        }
    };

    const loadDataPreview = async () => {
        const fileInput = document.getElementById('data_file');
        if (!fileInput.files.length) return;

        const formData = new FormData();
        formData.append('data_file', fileInput.files[0]);

        try {
            const response = await fetch('/api/parse_csv', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (response.ok && result.participants) {
                dataTableBody.innerHTML = '';
                result.participants.forEach(p => {
                    const row = document.createElement('tr');
                    const nameCell = document.createElement('td');
                    nameCell.textContent = p.Name || 'N/A';
                    const emailCell = document.createElement('td');
                    emailCell.textContent = p.Email || 'N/A';
                    row.appendChild(nameCell);
                    row.appendChild(emailCell);
                    dataTableBody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error loading data preview:', error);
        }
    };

    // Debounce wrapper for preview
    let timeout;
    const debouncedLoadPreview = () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            loadPreview();
        }, 400); // 400ms delay
    };

    // Listen to input changes for live update
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.type === 'file' || input.type === 'color' || input.tagName === 'SELECT') {
            input.addEventListener('change', (e) => {
                debouncedLoadPreview();
                if (e.target.id === 'data_file') {
                    loadDataPreview();
                }
            });
        } else {
            input.addEventListener('input', debouncedLoadPreview);
        }
    });

    // Hide manual preview button
    if (previewBtn) previewBtn.style.display = 'none';

    generateBtn.addEventListener('click', async () => {
        const formData = new FormData(form);
        const demoMode = document.getElementById('demo_mode').checked;
        formData.append('demo_mode', demoMode);

        const originalText = generateBtn.textContent;
        generateBtn.textContent = 'Processing...';
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const result = await response.json();
                throw new Error(result.error || 'Failed to start generation');
            }

            if (demoMode) {
                // Handle ZIP download
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'certificates.zip';
                document.body.appendChild(a);
                a.click();
                a.remove();
                showMessage('Success: Certificates generated and downloaded as a ZIP archive.');
            } else {
                const result = await response.json();
                showMessage(`Success: ${result.message} Processed ${result.total} participants.`);
            }

        } catch (error) {
            showMessage(error.message, true);
        } finally {
            generateBtn.textContent = originalText;
            generateBtn.disabled = false;
        }
    });

    // Drag and Drop styling
    const fileUploads = document.querySelectorAll('.file-upload');
    fileUploads.forEach(upload => {
        const input = upload.querySelector('input[type="file"]');
        upload.addEventListener('dragover', e => {
            e.preventDefault();
            upload.classList.add('drag-over');
        });
        upload.addEventListener('dragleave', e => {
            upload.classList.remove('drag-over');
        });
        upload.addEventListener('drop', e => {
            upload.classList.remove('drag-over');
        });
        input.addEventListener('change', () => {
            upload.classList.remove('drag-over');
        });
    });

    // Initial preview on load
    loadPreview();

    // Tab Navigation Logic
    const navTabs = document.querySelectorAll('.nav-tab');
    const viewSections = document.querySelectorAll('.view-section');

    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and views
            navTabs.forEach(t => t.classList.remove('active'));
            viewSections.forEach(v => v.classList.remove('active'));
            viewSections.forEach(v => v.classList.add('hidden'));

            // Add active class to clicked tab
            tab.classList.add('active');

            // Show corresponding view
            const targetId = tab.getAttribute('data-target');
            const targetView = document.getElementById(targetId);
            if (targetView) {
                targetView.classList.remove('hidden');
                targetView.classList.add('active');
            }
        });
    });
});
