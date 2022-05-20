import re


def state_tracer(document, type_of_trace):
    full_document = ""
    document_dict = {}
    states, state_trigger, state_effect = {}, {}, {}
    current_state = []
    state_lines, state_lines_dict = [], {}

    for n, lines in enumerate(document):
        n += 1
        document_dict[n] = lines.split()
        full_document += lines

        # INDEXES STATES AND THEIR CORRESPONDING LINES
        # DEFINED IN THE PlantUML STATE MACHINE DIAGRAM
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

    # SORTS THE STATES IN ORDER OF APPEARANCE
    state_lines.sort(key=lambda state: state[1])

    for entry in state_lines:
        if entry[0][0] in state_lines_dict:
            state_lines_dict[entry[0][0]] = [state_lines_dict[entry[0][0]], entry[1]]
        else:
            state_lines_dict[entry[0][0]] = entry[1]

    for key, value in document_dict.items():

        if value[0] == "state":

            states[key] = value[1].strip("{")

        trigger_search = re.search("(\?)\w+", str(value))
        effect_search = re.search("(!)\w+", str(value))

        if trigger_search is not None:
            state_trigger[key] = trigger_search[0]

        if effect_search is not None:
            state_effect[key] = effect_search[0]
    if type_of_trace:
        return states, state_trigger, state_effect, state_lines_dict
    else:
        return state_trigger