import ao_core as ao
from Arch import Arch
import time 
import keyboard

agent = ao.Agent(Arch=Arch)


Run = True
delay = 0.5
while Run == True:
    time.sleep(delay)
    input_to_agent = [0] * 11

    if keyboard.is_pressed('f'):  
        input_to_agent[0] = [1]  # Food

    if keyboard.is_pressed("b"):
        input_to_agent[1:4] = [1,1,1]

    if keyboard.is_pressed("q"):
        Run = False


    print("Input to agent: ", input_to_agent)
    response = agent.next_state(input_to_agent, INSTINCTS=True)
    # agent.reset_state()

    print("Agent response: ", response)








