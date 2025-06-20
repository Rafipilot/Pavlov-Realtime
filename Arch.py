
# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/Arch.py (C) 2023 Animo Omnis Corporation. All Rights Reserved.

Thank you for your curiosity!
"""


## //  Pavlov  -- Reference Design #0
# 
#
# For interactive visual representation of this Arch:
#    https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=72701488535
#
# Customize and upload this Arch to our API to create Agents: https://docs.aolabs.ai/reference/kennelcreate
#
import ao_core as ar
import numpy as np
import random 

number_qa_neurons = 5

description = "Basic Pavlov"
arch_i = [1, 3, 1, 3, 1, 1, 1]     # 7 neurons, 1 in each of 6 channels, corresponding to Food, Bell, Tactile, Flash, Chime, Monster, Splash of water
arch_z = [1]           # corresponding to Open=1/Close=0
arch_c = [2]           # adding 1 control neuron which we'll define with the instinct control function below
arch_qa = [number_qa_neurons]
connector_function = "full_conn"



# To maintain compatibility with our API, do not change the variable name "Arch" or the constructor class "ar.Arch" in the line below
Arch = ar.Arch(arch_i, arch_z, arch_c, connector_function, arch_qa=arch_qa, qa_conn="none", description=description)

# set-relative id of neuron; the first 3 neurons (ids 0, 1, 2) are included in all Archs by default (corresponding to LABEL, Cpos, Cneg)

# Adding Instinct Control Neuron for react 
c0 = 3 # neuron number 3
def c0_instinct_rule(INPUT, Agent):
    type = "Pleasure"

    if INPUT[0] == 1    and     Agent.buffer[ -2,  Agent.arch.Z__flat[0]]==1 and type== "Pleasure":        # self.Z__flat[0] needs to be adjusted as per the agent, which output the designer wants the agent to repeat while learning postively or negatively
        instinct_response = [1, "c0 instinct triggered"]
    elif INPUT[10] == 1 and Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]] == 1 and type == "Fear":
        instinct_response = [1, "c0 instinct triggered"]                                                                         
    else:
        instinct_response = [0, "c0 pass"]    
    return instinct_response            
Arch.C__flat_pleasure = np.append(Arch.C__flat_pleasure, Arch.C__flat[c0])
Arch.datamatrix[4, Arch.C[1][0]] = c0_instinct_rule


# adding instinct control neuron for slight neg
c1 = 4 #neuron number 3

def c1_instinct_rule(INPUT, Agent):
    type = "Pleasure"
    if INPUT[10] == 1 and type == "Fear":
        instinct_response = [0, "c1 pass"]
    elif INPUT[0] == 1 and type == "Pleasure":
        instinct_response = [0, "c1 pass"]

    else:
        if Agent.buffer[ -2,  Agent.arch.Z__flat[0]] == 1: #If reacted without Food or Fear 

            if Agent.counter ==0:
                instinct_response = [1, "c1 instinct triggered"]
            else:
                instinct_response = [0, "c1 pass"]            

        else:
            instinct_response = [0, "c1 pass"]
  
    return instinct_response
Arch.C__flat_pain = np.append(Arch.C__flat_pain, Arch.C__flat[c1])
Arch.datamatrix[4, Arch.C[1][1]] = c1_instinct_rule


# Saving the function to the Arch so the Agent can access it


#Adding Aux Action
def qa0_firing_rule(INPUT, Agent): 
    if not hasattr(Agent, 'counter'):
        Agent.__setattr__("counter", 0)

    print("agent counter: ", Agent.counter)
    print("last response: ", Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]])

    if Agent.counter < (number_qa_neurons+1) and INPUT[0] == 1    and Agent.buffer[ -2,  Agent.arch.Z__flat[0]] == 1: #If the agent ate food 

        Agent.counter += 1
        group_response = np.zeros(number_qa_neurons)
        group_response[0 : Agent.counter] = 1

    elif INPUT[0] == 0    and Agent.buffer[ -2,  Agent.arch.Z__flat[0]] == 1:   
        if Agent.counter == 0:
            ## pain signal needed
            
            print("applying pain signal")
            group_response = np.ones(number_qa_neurons)
            group_response[0 : Agent.counter] = 1
            Agent.counter = number_qa_neurons
        else:
            print("reducing counter")
            # random_number = random.randint(0, 5)
            # if random_number == 3:
            if Agent.counter >= 1:
                Agent.counter -= 1
            group_response = np.zeros(number_qa_neurons)
            group_response[0 : Agent.counter] = 1
            

    else:    #If the agent did not react then dont touch the counter
        group_response = np.zeros(number_qa_neurons)
        group_response[0 : Agent.counter] = 1
     

    group_meta = np.ones(number_qa_neurons, dtype="O")
    group_meta[:] = "qa0"
    return group_response, group_meta
# Saving the function to the Arch so the Agent can access it
Arch.datamatrix_aux[2] = qa0_firing_rule

# #Connecting QA neurons to the Q Neurons
#for i in range(len(arch_i)):
#    Arch.datamatrix[1, Arch.Q__flat]+=Arch.datamatrix_aux[1]

# #Connecting QA neurons to the Z Neurons
# Arch.datamatrix[1, Arch.Z__flat] += Arch.datamatrix_aux[1]
