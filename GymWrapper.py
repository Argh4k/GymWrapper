from gym import envs
import gym
from gymhttperror import InvalidUsage

class GymWrapper():

    def __init__(self):
        self.env = None

    def getAvailableEnviornments(self):
        atariEnvs = []
        for env in envs.registry.all():
            if("Atari" in env._entry_point):
                atariEnvs.append(env.id)
        return atariEnvs
            
    def createEnvironment(self, envID):
        if(self.env != None):
            raise InvalidUsage("Environment already created")
        try: 
            self.env = gym.make(envID)
            self.env.reset()
        except gym.error.Error:
            raise InvalidUsage("Could not create environment")

    def getObservationSpace(self):
        if(self.env != None):
            obSpace = {}
            obSpace["low"] =  self.env.observation_space.low.tolist()
            obSpace["high"] =  self.env.observation_space.high.tolist()
            obSpace["shape"] = self.env.observation_space.shape
            return obSpace
        else:
            raise InvalidUsage("Environment not created")

    def step(self, stepValue):
        if(self.env != None):
            try:
                retVal = {}
                observation, reward, done, info =  self.env.step(stepValue)
                retVal["observation"] = observation.tolist()
                retVal["reward"] = reward
                retVal["done"] = done
                return retVal
            except gym.error.Error:
                raise InvalidUsage("Wrong step value")
        else:
            raise InvalidUsage("Environment not created")

    def reset(self):
        if(self.env != None):
            self.env.reset()
        else:
            raise InvalidUsage("Environment not created")

    def getActionSpace(self):
        if(self.env != None):
            space = self.env.action_space
            actions = []
            for x in range(space.n):
                actions.append(x)
            return actions
        else:
            raise InvalidUsage("Environment not created")

    def clearEnvironment(self):
        self.env = None


    def resetEnvironment(self):
        if(self.env != None):
            self.env.reset()
        else:
            raise InvalidUsage("Environment not created")

# gymWrapper = GymWrapper()
# gymWrapper.createEnvironment("AirRaid-ram-v0")
# print(gymWrapper.getActionSpace())
# print(gymWrapper.getObservationSpace())
# print(gymWrapper.step(0))