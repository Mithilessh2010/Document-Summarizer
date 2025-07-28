document.getElementById('summarize-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    const response = await fetch('/summarize', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const summaryDiv = document.getElementById('summary-result');
    if (result.summary) {
        summaryDiv.textContent = result.summary;
    } else {
        summaryDiv.textContent = 'Error: ' + (result.error || 'Unknown error');
    }
});
