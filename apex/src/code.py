from stateMachine import diagnostic, state

curr_state: state | None = diagnostic()
try: 
    while curr_state is not None:
       curr_state = curr_state.run()
except Exception as e:
    file = open("error.txt", "w")
    file.write(str(e))
    file.close() 
    raise e