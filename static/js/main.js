document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    const generateBtn = document.getElementById('generateBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const securityBtn = document.getElementById('securityBtn');
    const testBtn = document.getElementById('testBtn');
    const outputArea = document.getElementById('outputArea');

    function sendRequest(endpoint, data) {
        outputArea.textContent = 'Processing...';
        return fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            return data.result || JSON.stringify(data);
        })
        .catch(error => {
            console.error('Error:', error);
            return `An error occurred: ${error.message}. Please check the server logs for more details.`;
        });
    }

    function handleButtonClick(endpoint, inputKey) {
        return () => {
            const input = codeInput.value.trim();
            if (!input) {
                outputArea.textContent = `Please enter ${inputKey === 'prompt' ? 'a prompt' : 'code'}.`;
                return;
            }
            sendRequest(endpoint, { [inputKey]: input })
                .then(result => {
                    outputArea.textContent = result;
                });
        };
    }

    generateBtn.addEventListener('click', handleButtonClick('/generate_code', 'prompt'));
    analyzeBtn.addEventListener('click', handleButtonClick('/analyze_code', 'code'));
    securityBtn.addEventListener('click', handleButtonClick('/security_check', 'code'));
    testBtn.addEventListener('click', handleButtonClick('/generate_tests', 'code'));
});