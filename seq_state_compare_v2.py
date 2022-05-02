import re

import state_tracer as state
import sequence_tracer as sequence


def parse_file(filepath):

    document_data = []

    with open(filepath, 'r') as file_object:
        lines = file_object.readlines()

        for line in lines:
            if line != "\n":
                line.lower()
                document_data.append(line)

    return document_data


if __name__ == '__main__':

    sequence_list = ['->', '<-', '-->', '<--', '\[->', '<-\]']
    gate_sequence = ['\[->', '<-\]']
    arrow_list = ['<', '>']

    '''
    stateflag = False
    while not stateflag:
        try:
            state_filepath = input("state machine diagram filepath:\t")
            state_data = parse_file(state_filepath)
            if "@startuml" not in str(state_data):
                print("Error:\tNot a plantuml-file")
                pass
            if "state" not in str(state_data).lower():
                print("Error:\tNot a state machine diagram")
                pass
            else:
                stateflag = True
        except Exception:
            print("File not found, please try again.")31t3
    '''

    state_filepath = 'example_state_machine'
    state_data = parse_file(state_filepath)

    seq_filepath = 'example_sequence_diagram'
    seq_data = parse_file(seq_filepath)

    states, state_trigger = state.state_tracer(state_data)
    sequence_dict, life_line = sequence.sequence_tracer(seq_data)

    check_list, state_check_list = [], []

    str_trigger_matches = "*** MATCH ***\n"
    str_possible_matches = "*** POSSIBLE MATCH ***\n"
    str_no_match = "*** NO MATCH ***\n"

    for line_no_sequence, value in sequence_dict.items():

        sequence_line = str(value)

        for line_state, trigger in state_trigger.items():

            trigger_match = re.search(fr"\b{trigger}\b", sequence_line)
            possible_match = re.search(f"({trigger})", sequence_line)

            if trigger_match is not None:

                if trigger_match[0] in sequence_line:

                    str_trigger_matches += f"STATE\t{line_state: >8}\t{trigger_match[0]: >10}\n" \
                                           f"SEQ\t\t{line_no_sequence: >8}\t{sequence_line: >10}\n\n"

                    check_list.append([line_state, line_no_sequence])

            if possible_match is not None:

                if possible_match[0] in sequence_line and [line_state, line_no_sequence] not in check_list:

                    str_possible_matches += f"STATE\t{line_state: >8}\t{possible_match[0]: >10}\n" \
                                            f"SEQ\t\t{line_no_sequence: >8}\t{sequence_line: >10}\n\n"

                    check_list.append([line_state, line_no_sequence])

    for state, sequence in check_list:
        state_check_list.append(state)

    for line_state, trigger in state_trigger.items():
        if line_state not in state_check_list:
            str_no_match += f"SEQ\t\t{line_state: >8}\t{trigger}\n"

    #print(str_trigger_matches)
    #print(str_possible_matches)
    #rint(str_no_match)

    with open("state_sequence_trace.txt", "w") as f:
        f.write(str_trigger_matches)
        f.write(str_possible_matches)
        f.write(str_no_match)