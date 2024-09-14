import requests
import logging


class OllamaHelper:

    def __init__(self, base_url='http://localhost:11434'):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def _generate(self, prompt):
        try:
            self.logger.info(f"Sending request to Ollama: {prompt[:50]}...")
            response = requests.post(f"{self.base_url}/api/generate",
                                     json={
                                         "model": "codellama",
                                         "prompt": prompt,
                                         "stream": False
                                     })
            response.raise_for_status()
            result = response.json()['response']
            self.logger.info("Received response from Ollama")
            return result
        except requests.RequestException as e:
            self.logger.error(f"Error communicating with Ollama: {str(e)}")
            raise Exception(f"Error communicating with Ollama: {str(e)}")

    def generate_code(self, prompt):
        return self._generate(f"Generate code for: {prompt}")

    def analyze_code(self, code):
        return self._generate(
            f"Analyze the following code and suggest improvements:\n\n{code}")

    def security_check(self, code):
        return self._generate(
            f"Perform a security check on the following code and identify potential issues:\n\n{code}"
        )

    def generate_tests(self, code):
        return self._generate(
            f"Generate unit tests for the following code:\n\n{code}")
