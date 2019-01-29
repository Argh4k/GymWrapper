from gym import envs
import gym
from gymhttperror import InvalidUsage
from imageSimplify import simplifyAtariOutput

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
            if("-ram" in envID):
                print("Setting ram to true")
                self.isRam = True
            else:
                self.isRam = False
            if("LunarLander-v2" in envID):
                self.isRam = True
                self.env.reset()
                self.noAction = 0
                return
            acitonMeanings = self.env.unwrapped.get_action_meanings()
            self.noAction = -1
            try:
                self.noAction = acitonMeanings.index("NOOP")
            except ValueError:
                self.noAction = 0
            self.env.reset()
        except gym.error.Error:
            raise InvalidUsage("Could not create environment")

    def getObservationSpace(self):
        if(self.env != None):
            obSpace = {}
            if self.isRam:
                # obSpace["low"] =  self.env.observation_space.low.tolist()
                # obSpace["high"] =  self.env.observation_space.high.tolist()
                obSpace["shape"] = self.env.observation_space.shape
            else:
                obSpace["shape"] = [16*21]
            return obSpace
        else:
            raise InvalidUsage("Environment not created")

    def step(self, stepValue):
        if(self.env != None):
            try:
                retVal = {}
                
                observation, reward, done, info =  self.env.step(stepValue)
                totalReward = 0
                if(done):
                    if self.isRam:
                        retVal["observation"] = observation.tolist()
                    else:
                        retVal["observation"] = simplifyAtariOutput(observation)
                    retVal["reward"] = reward
                    retVal["done"] = done
                    retVal["info"] = info
                    return retVal
                for x in range(3):
                    observation, reward, done, info =  self.env.step(stepValue)
                    totalReward += reward
                    if(done or x == 2):
                        if self.isRam:
                            retVal["observation"] = observation.tolist()
                        else:
                            retVal["observation"] = simplifyAtariOutput(observation)
                        retVal["reward"] = totalReward
                        retVal["done"] = done
                        retVal["info"] = info
                        return retVal
            except gym.error.Error:
                raise InvalidUsage("Wrong step value")
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
            retVal = {}
            observation = self.env.reset()
            if self.isRam:
                retVal["observation"] = observation.tolist()
            else:
                retVal["observation"] = simplifyAtariOutput(observation)
            return retVal
        else:
            raise InvalidUsage("Environment not created")
