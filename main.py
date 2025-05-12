import ao_core as ao
from Arch import Arch
import time 
import keyboard

agent = ao.Agent(Arch=Arch)


Run = True

#TUNABLE PARAMETERS
delay = 0.5
trials_at_time = 10

#RANDOM PRETRAINING
for i in range(4):
    agent.reset_state(training=True)

#MAIN LOOP
while Run == True:
    time.sleep(delay)
    input_to_agent = [0] * 11

    if keyboard.is_pressed('f'):  
        input_to_agent[0] = 1  # Food

    if keyboard.is_pressed("b"):
        input_to_agent[1:4] = [1,1,1]

    if keyboard.is_pressed("t"):
        input_to_agent[4] = 1

    if keyboard.is_pressed("l"):
        input_to_agent[5:8] = [1,1,1]

    if keyboard.is_pressed("c"):
        input_to_agent[8] = 1

    if keyboard.is_pressed("m"):
        input_to_agent[9] = 1

    if keyboard.is_pressed("w"):
        input_to_agent[10] = 1

    if keyboard.is_pressed("q"):
        Run = False


    print("Input to agent: ", input_to_agent)
    responses = 0


    for i in range(trials_at_time):
        response = agent.next_state(input_to_agent, INSTINCTS=True)
        agent.reset_state()
        if response == [1]:
            responses +=1


    print("Agent response: ", (responses/trials_at_time) *100, "%")

## TODO return responses list similar to current pavlov




