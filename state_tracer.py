import re


def state_tracer(document):
    full_document = ""
    document_dict = {}
    states, state_trigger, state_effect = {}, {}, {}
    nested_start_index, nested_end_index = [], []
    nested_counter = 0
    current_state = []
    state_lines, state_lines_dict = [], {}

    for n, lines in enumerate(document):
        n += 1
        document_dict[n] = lines.split()
        full_document += lines
        state_start_search = re.search(r"(?:state)?.*{", lines)
        state_end_search = re.search("}", lines)

        if state_start_search is not None:
            current_state.append(state_start_search[0])
            state_lines.append([current_state[-1:], n])
            continue

        if state_end_search is not None:
            state_lines.append([current_state[-1:], n])
            current_state.pop()
            continue

    state_lines.sort(key=lambda state: state[0])

    for entry in state_lines:
        if entry[0][0] in state_lines_dict:
            state_lines_dict[entry[0][0]] = [state_lines_dict[entry[0][0]], entry[1]]
        else:
            state_lines_dict[entry[0][0]] = entry[1]

    #print(state_lines_dict)

    for key, value in state_lines_dict.items():
        print(key.strip("state ").strip("{").upper())

        for i in range(value[0] - 1, value[1]):
            print(document[i])

    for key, value in document_dict.items():
        # print(key, value)

        if value[0] == "state":

            states[key] = value[1].strip("{")

        trigger_search = re.search("(\?)\w+", str(value))
        effect_search = re.search("(!)\w+", str(value))

        if trigger_search is not None:
            state_trigger[key] = trigger_search[0][1:]

        if effect_search is not None:
            state_effect[key] = effect_search[0]

    #print(nested_end_index)
#    for lines in range(nested_start_index[1][0], nested_end_index[1][0] - 1):
#        print(document_dict[lines])
    #print(states)
    #print(state_trigger)
    #print(state_effect)
    return states, state_trigger
