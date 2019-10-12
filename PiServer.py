import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')



@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/exec', methods=['POST'])
def execute():
    data = request.get_json(force=True)
    print(data['code'])
    f = open("run.py", "w")
    f.write(data['code'])
    f.close()
    x = None
    try:
        output = subprocess.check_output(
        ["python", "run.py"], stderr=subprocess.STDOUT, shell=True, timeout=30,
        universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        return jsonify(success=True, data=exc.output)
    else:
        return jsonify(success=True, data="{}\n".format(output))
    

if __name__ == "__main__":
    app.run(port=9000, debug='True')