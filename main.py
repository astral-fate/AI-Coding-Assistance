from flask import Flask, render_template, request, jsonify
from ollama_helper import OllamaHelper
import traceback
import logging
import sys
import os

app = Flask(__name__)
ollama_url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
ollama = OllamaHelper(ollama_url)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An unhandled exception occurred: {str(e)}")
    app.logger.error(traceback.format_exc())
    return jsonify(error=str(e), stacktrace=traceback.format_exc()), 500


def log_request(route):
    app.logger.info(f"Received request for {route}")
    app.logger.debug(f"Request data: {request.json}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_code', methods=['POST'])
def generate_code():
    log_request('/generate_code')
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        app.logger.info(f"Generating code for prompt: {prompt}")
        generated_code = ollama.generate_code(prompt)
        app.logger.info("Code generation successful")
        return jsonify({'result': generated_code})
    except Exception as e:
        app.logger.error(f"Error in generate_code: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'stacktrace': traceback.format_exc()
        }), 500


@app.route('/analyze_code', methods=['POST'])
def analyze_code():
    log_request('/analyze_code')
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        app.logger.info("Analyzing code")
        analysis = ollama.analyze_code(code)
        app.logger.info("Code analysis successful")
        return jsonify({'result': analysis})
    except Exception as e:
        app.logger.error(f"Error in analyze_code: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'stacktrace': traceback.format_exc()
        }), 500


@app.route('/security_check', methods=['POST'])
def security_check():
    log_request('/security_check')
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        app.logger.info("Performing security check")
        security_issues = ollama.security_check(code)
        app.logger.info("Security check successful")
        return jsonify({'result': security_issues})
    except Exception as e:
        app.logger.error(f"Error in security_check: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'stacktrace': traceback.format_exc()
        }), 500


@app.route('/generate_tests', methods=['POST'])
def generate_tests():
    log_request('/generate_tests')
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        app.logger.info("Generating tests")
        tests = ollama.generate_tests(code)
        app.logger.info("Test generation successful")
        return jsonify({'result': tests})
    except Exception as e:
        app.logger.error(f"Error in generate_tests: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'stacktrace': traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.logger.info(
        f"Starting the Flask application. Ollama URL: {ollama_url}")
    app.run(host='0.0.0.0', port=5000, debug=True)
