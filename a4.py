from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None

    if request.method == 'POST':
        param1 = request.form['param1']
        param2 = request.form['param2']
        output = run_shell_script(param1, param2)

    return render_template('index.html', output=output)

def run_shell_script(param1, param2):
    try:
        result = subprocess.check_output(['/path/to/your/script.sh', param1, param2], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.returncode}, {e.output}"

if __name__ == '__main__':
    app.run(debug=True)
