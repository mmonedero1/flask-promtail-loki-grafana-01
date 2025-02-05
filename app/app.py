import logging
from flask import Flask, request, jsonify, make_response
from logging.config import dictConfig

app = Flask(__name__)

# Configura el logging para que escriba en un archivo
# logging.basicConfig(filename='logs/app.log', level=logging.INFO)


logging.basicConfig(level=logging.INFO)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
        "file": {
                "class": "logging.FileHandler",
                "filename": "logs/app.log",
                "formatter": "default",
            },            
        },
        "root": {"level": "DEBUG", "handlers": ["console","file"]},
    }
)

@app.route('/')
def main():
    app.logger.info("*--> Este es un log INFO")
    return "Test logger"

@app.route('/hello', methods=['POST'])
def hello():
   data = request.get_json()
   if "name" in data:
       name = data["name"]
   else:
       name = None

   if name:
    #    print('Request for hello page received with name=%s' % name)
       app.logger.info(f"*--> Nombre informado: {name}")
       return make_response(f'Buenos días {name}.', 200)
   else:
    #    print('Request for hello page received with no name or blank name -- redirecting')
       app.logger.info(f"*--> Sin nombre informado.")
       return make_response('No me has dicho tu nombre', 200)
   
@app.route('/error')
def error():
    response = {
        "error": "Bad Request",
        "message": "There was an error with your request."
    }
    return make_response(jsonify(response), 400)
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
