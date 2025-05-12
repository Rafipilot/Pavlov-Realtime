import ao_core as ao
from Arch import Arch
import time 
import keyboard
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")
st.title("Realtime Pavlov App")

if not st.session_state:
    st.session_state.agent = ao.Agent(Arch=Arch)
    st.session_state.Run = False
    st.session_state.trial_number = 0
    st.session_state.results = []

#TUNABLE PARAMETERS
if st.slider("delay", max_value=10):
    st.session_state.delay = 1
if st.slider("trials", max_value=10):
    st.session_state.trials_at_time = 10

#RANDOM PRETRAINING
for i in range(4):
    st.session_state.agent.reset_state(training=True)

if st.button("Start/ Stop"):

    if st.session_state.Run:
        st.session_state.Run = False
    else:
        st.session_state.Run = True

result = st.empty()

#MAIN LOOP
while st.session_state.Run == True:
    time.sleep(st.session_state.delay)
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
        st.session_state.Run = False


    #st.write("Input to agent: ", input_to_agent)
    responses = 0


    for i in range(st.session_state.trials_at_time):
        response = st.session_state.agent.next_state(input_to_agent, INSTINCTS=True)
        st.session_state.agent.reset_state()
        if response == [1]:
            responses +=1

    trial_result = {"Trial number ": st.session_state.trial_number , "Input:": input_to_agent, "Agent response:":  (responses/st.session_state.trials_at_time) *100}
    result.text(trial_result)
    st.session_state.trial_number +=1
    st.session_state.results.append(trial_result)

st.text(f"Results: {st.session_state.results}")
results_df = pd.DataFrame(st.session_state.results)

csv = results_df.to_csv(index=False)


st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="pavlov_experiment_results.csv",
    mime="text/csv"
)


## TODO downloaad for results
## Multiple agents
## Intensity : B1 , b2 etc

# Trial number Input Result Average(for multiple agents) 




