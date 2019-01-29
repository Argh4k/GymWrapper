from flask import Flask, request, jsonify
from gymhttperror import InvalidUsage
from gymwrapper import GymWrapper

server = Flask(__name__)
gymWrapper = GymWrapper()

def getJsonParam(jsonData, parameter, defaultValue):
    if jsonData is None:
        return defaultValue
    value = jsonData.get(parameter, defaultValue)
    return value

@server.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.toDict())
    response.status_code = error.statusCode
    return response

@server.route('/env', methods=['POST'])
def createEnv():
    requestData = request.get_json()
    envID = getJsonParam(requestData, "envID", None)
    if(envID == None):
        raise InvalidUsage("Request does not have envID")
    gymWrapper.createEnvironment(envID)
    return "Succesfuly created environment"

@server.route('/env/available_environments', methods=['GET'])
def listAvailableEnv():
    envs = gymWrapper.getAvailableEnviornments()
    return jsonify(envs)

@server.route('/env/action_space', methods=['GET'])
def listActionSpace():
    actionSpace = gymWrapper.getActionSpace()
    return jsonify(actionSpace)

@server.route('/env/observation_space', methods=['GET'])
def listObservationSpace():
    observationSpace = gymWrapper.getObservationSpace()
    return jsonify(observationSpace)

@server.route('/env/step', methods=['POST'])
def step():
    requestData = request.get_json()
    step = getJsonParam(requestData, "step", -1)
    if(step == -1):
        raise InvalidUsage("Invalid step value")
    gameData = gymWrapper.step(step)
    return jsonify(gameData)

@server.route('/env/reset', methods=['GET'])
def resetEnvironment():
    initialState = gymWrapper.resetEnvironment()
    return jsonify(initialState)

@server.route('/env/clear', methods=['GET'])
def clearEnvironment():
    gymWrapper.clearEnvironment()
    return "Successfully cleared environment"

server.run("127.0.0.1", 8002)