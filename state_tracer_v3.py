import re


def state_tracer(plantuml_file, type_of_trace):
    state_dictionary = {}
    states, state_trigger, state_effect = {}, {}, {}
    current_state = []
    state_index, individual_state = [], {}

    for n, lines in enumerate(plantuml_file):
        n += 1
        state_dictionary[n] = lines.split()

        # Index states and their corresponding lines
        # defined in the PlantUML state diagram
        state_start = re.search(r"(?:state)?.*{", lines)
        state_end = re.search("}", lines)

        if state_start is not None:
            current_state.append(state_start[0])
            state_index.append([current_state[-1:], n])
            continue

        if state_end is not None:
            state_index.append([current_state[-1:], n])
            current_state.pop()
            continue

    # Sorts the states in order of appearance
    state_index.sort(key=lambda state: state[1])

    for entry in state_index:
        if entry[0][0] in individual_state:
            individual_state[entry[0][0]] = [individual_state[entry[0][0]], entry[1]]
        else:
            individual_state[entry[0][0]] = entry[1]

    for line_number, line in state_dictionary.items():

        if line[0] == "state":

            states[line_number] = line[1].strip("{")

        trigger_search = re.search("(\?)\w+", str(line))
        effect_search = re.search("(!)\w+", str(line))

        if trigger_search is not None:
            state_trigger[line_number] = trigger_search[0]

        if effect_search is not None:
            state_effect[line_number] = effect_search[0]


    if type_of_trace:
        return states, state_trigger, state_effect, individual_state
    else:
        return state_trigger
