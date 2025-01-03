from flask import Flask, jsonify
from pypeekr.pypeekr_server import linux_server_data

# flask app to handle http request for data from linux server
app = Flask(__name__)

# start the server
data_obj = linux_server_data.LinuxDataServer()


# single data endpoint
@app.route('/data', methods=['GET'])
def return_data():
    data_obj.update_linux_data_server()
    print(jsonify(data_obj.server_data))
    return jsonify(data_obj.server_data)


# add a fxn that to run so poetry can create a scrip to call it
def run_linux_server_app():
    app.run(host='0.0.0.0', port=8000)


# start if run from cmd line
if __name__ == '__main__':
    run_linux_server_app()
