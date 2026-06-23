document.addEventListener('DOMContentLoaded', () => {
    const previewBtn = document.getElementById('preview-btn');
    const generateBtn = document.getElementById('generate-btn');
    const form = document.getElementById('cert-form');
    const iframe = document.getElementById('preview-frame');
    const loader = document.getElementById('loader');
    const statusMsg = document.getElementById('status-message');

    // Debounce function for live preview (optional, but manual click is more robust with files)
    const showMessage = (msg, isError = false) => {
        statusMsg.textContent = msg;
        statusMsg.className = `status-message ${isError ? 'error' : 'success'}`;
        statusMsg.classList.remove('hidden');
        setTimeout(() => {
            statusMsg.classList.add('hidden');
        }, 5000);
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

    previewBtn.addEventListener('click', loadPreview);

    generateBtn.addEventListener('click', async () => {
        const formData = new FormData(form);
        const demoMode = document.getElementById('demo_mode').checked;
        formData.append('demo_mode', demoMode);

        const dataFile = document.getElementById('data_file').files[0];
        if (!dataFile && !demoMode) {
            // If they haven't selected a file, maybe we check if demo mode handles it?
            // Actually our backend falls back to data/sample_participants.csv if not provided.
        }

        const originalText = generateBtn.textContent;
        generateBtn.textContent = 'Processing...';
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to start generation');
            }

            showMessage(`Success: ${result.message} Processing ${result.total} certificates in the background.`);
        } catch (error) {
            showMessage(error.message, true);
        } finally {
            generateBtn.textContent = originalText;
            generateBtn.disabled = false;
        }
    });

    // Initial preview on load
    loadPreview();
});
