from controller import Controller

class player_controller(Controller):
    def __init__(self,nothing='nothing'):
        self.nothing=nothing
    def control(self,inputs, controller):
        #inputs = (inputs - min(inputs)) / float((max(inputs) - min(inputs)))
        #print(inputs)
        #for i in range(len(inputs)-1):

        #closing up the distance without bullet
        if inputs[0] >= 100:
            left = 1
        else:
            left = 0

        if inputs[0] <= -100:
            right = 1
        else:
            right = 0
        #if player is below enemy or
        if inputs[1] >0:
            jump = 1
        else:
            jump = 0

        #dodge vertical bullet
        for i in range(8):
            #vertical bullet
            if inputs[4+i*2] != 0 : #and inputs[5+i*2] == 0 :
                if inputs[0] <= -100:
                    left = 0
                    right = 1
                elif inputs[0] >= 100:
                    right = 0
                    left = 1
                else :
                    if inputs[0] > 0:
                        right = 1
                        left = 0
                    else :
                        right = 0
                        left = 1

            #horizontal bullet
            if inputs[5+i*2] != 0 :
                if inputs[4+i*2]>0:
                    jump = 1
                    release = 0
                else:
                    jump = 0
                    release = 1
        #if both are at the same horizontal pos then shoot
        #if inputs[1] == inputs[3]:
        #    shoot = 1
        #else:
        #    shoot = 0

        if inputs[4] > 0.5:
            release = 1
        else:
            release = 0

        shoot = 1
        print([left, right, jump, shoot, release])
        return [left, right, jump, shoot, release]

class enemy_controller(Controller):

    def control(self,inputs,Controller):
        #inputs = (inputs - min(inputs)) / float((max(inputs) - min(inputs)))
        if inputs[0] >= 0:
            attack1 = 1
        else:
            attack1 = 0

        if inputs[0] < 0:
            attack2 = 1
        else:
            attack2 = 0

        if inputs[1] >= 0:
            attack3 = 1
        else:
            attack3 = 0

        if inputs[1] < 0:
            attack4 = 1
        else:
            attack4 = 0

        return [attack1, attack2, attack3, attack4]

#function for both