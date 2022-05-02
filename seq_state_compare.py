import re
from ast import literal_eval
from random import randint
import state_tracer as state
import sequence_tracer as sequence




def color_pick():

    hex_digits = "0123456789ABCDEF"
    random_color = "#"
    for i in range(6):
        if i % 2 != 0:
            random_color += hex_digits[randint(0, 9)]
        else:
            random_color += hex_digits[randint(9, 15)]

    return random_color


def parse_file(filepath):

    document_data = []

    with open(filepath, 'r') as file_object:
        lines = file_object.readlines()

        for line in lines:
            if line != "\n":
                line.lower()
                document_data.append(line)

    return document_data


def sequence_tracer(document):

    loop_count, alt_count, end_count = [], [], []
    sequence_dict = {}

    for n, lines in enumerate(document):
        seq_match_list.append(lines.split())
        sequence_dict[n+1] = lines

    for number, entry in enumerate(seq_match_list):

        entry_str = str(entry)
        entry_str = entry_str.replace("\', \'", " ")

        if "loop" in entry_str:
            loop_count.append([number, entry_str])
        if "alt" in entry_str:
            alt_count.append([number, entry_str])
        if re.search("(?<![\w\d])end(?![\w\d])", entry_str):
            end_count.append([number, entry_str])

        # ADD PARTICIPANTS
        if (len(entry) > 2) and (entry[0] in participant_list):
            participants.append([number+1, entry[3].lower()])

        if (len(entry) < 2) and (entry[0] in participant_list):
            participants.append([number+1, entry[1].lower()])

        # ADD COMMANDS
        if ("(" in entry_str):

            # (temp1)'] => (temp1)
            entry_str = entry_str.replace("\']", "")
            entry_new_array = entry_str.split(": ")

            seq_event.append([number+1, entry_new_array[1]])

        for arrow in sequence_list:

            if arrow in entry_str and [number+1, entry] not in sequences:
                sequences.append([number+1, entry])

    # print("\nLine\tParticipants:".upper())

    #f or line_number, seq_participants in participants:
        # print(f"{line_number}\t\t{seq_participants}")

    # print("\nLine\tEvents:".upper())
    # for line_number, event in seq_event:
       # print(f"{line_number}\t\t{event}")

    # print("\nLine\tTransitions:".upper())


    transmissions = {}
    for line_number, sequence in sequences:
        # print("One", sequence[0])
        #print("Two", sequence[2])
        participant_one = sequence[0].strip(":")
        sequence_arrow = sequence[1]
        sequence_arrow = sequence_arrow.replace("]:", "]")
        participant_two = sequence[2].strip(":")



        if participant_two not in str(participants) or participant_two == "":
            participant_two = "gate"

        # print(f"{line_number}\t\t{participant_one: <6} {sequence_arrow: <6} {participant_two}")

        if sequence_arrow in ['[->', '->', '-->']:
            tx_participant = participant_one
            rx_participant = participant_two
            transmissions[line_number] = [tx_participant, rx_participant]

        if sequence_arrow in ['<-]', '<-', '<--']:
            tx_participant = participant_two
            rx_participant = participant_one
            transmissions[line_number] = [tx_participant, rx_participant]

    # print("\nLine\tTransmission:".upper())
    # for line_n, transmission in transmissions.items():

        # print(f"{line_n}\t\t{transmission[0]: <6} to {transmission[1]: >6}")

    """
    print(loop_count)
    print(alt_count)
    print(end_count)
    """

    for state_participant in participants:
        statemachine = ""
        statemachine += "@startuml\n"
        statemachine += f"[*] --> {state_participant[1]}\n"
        statemachine += f"state {state_participant[1]} {color_pick()}{{\n"
        last_state = ""

        for sequence_to_state in sequences:

            for state_event in seq_event:

                if sequence_to_state[0] == state_event[0]:

                    ext = re.match("^(.*?)\(", str(state_event[1]))
                    ext2 = re.search("\(([^\)]+)\)", str(state_event[1]))

                    if last_state == "":
                        statemachine += f"[*] --> {ext[1]} {color_pick()}: {ext2[0]}\n"
                        last_state = str(ext[1])
                    else:
                        statemachine += f"{last_state} --> {ext[1]} {color_pick()}: {ext2[0]}\n"
                        last_state = str(ext[1])

        statemachine += "}\n"
        statemachine += "@enduml\n"

#        with open(f"generated_statechart_{state_participant[1]}", "w") as f:
#            f.write(statemachine)
        #print(f"\n{sequence_dict}")
        return seq_event


def seq_state_compare(document, seq_event):
    temp_str = ""
    document_dict, event_dict = {}, {}
    temp_array_processed = []

    for i in range(len(document)):
        document_dict[i + 1] = document[i]

    #print(f"\n{document_dict}\n")

    for n, seq_event in enumerate(seq_event):
        seq_events = re.match("^(.*?)\(", seq_event[1])
        event_dict[seq_events[1]] = [seq_events[1], n]

    #print(f"{event_dict}\n")
    # print(f"\nTRIGGERS AND EFFECTS\n")
    for dkey, ditem in document_dict.items():

        event = re.search("(\?)", ditem)

        for ckey, citem in event_dict.items():

            find_trigger = re.search(f"(\?{ckey})", ditem)
            find_event = re.search(f"(\!{ckey})", ditem)

            if find_trigger is not None:
                # print(f"Trigger:\t{find_trigger[0]}")

                if (find_trigger[0] in ditem) and (dkey not in temp_array_processed):

                    temp_str += ditem
                    temp_str += f"note on link #limegreen: Trigger:\t{find_trigger[0][1:]}\n"
                    temp_array_processed.append(dkey)

            #if find_event is not None:
                # print(f"Effect:\t\t{find_event[0]}\n")



        if event is not None:

            if dkey not in temp_array_processed:


                not_found_event = re.search("(\?)(.*?)(\W)", ditem)
                #print(f"Effect:\t\t{not_found_event[2]} not found\n")

                temp_str += ditem
                temp_str += f"note on link #F05000: {not_found_event[2]} not found\n"
                temp_array_processed.append(dkey)

        if dkey not in temp_array_processed:
            temp_str += ditem
            temp_array_processed.append(dkey)

        else:
            pass

    with open(f"seq_state_comparison", "w") as f:
        f.write(temp_str)


if __name__ == '__main__':

    state_filepath = 'example_state_machine'
    state_data = parse_file(state_filepath)



    transition_list = ['->', '-->', '--->']

    state_match_list, states, state_events, state_comments, transitions = [], [], [], [], []

    seq_filepath = 'example_sequence_diagram'
    seq_data = parse_file(seq_filepath)

    sequence_list = ['->', '<-', '-->', '<--', '\[->', '<-\]']
    world_sequence = ['\[->', '<-\]']
    participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']

    seq_match_list, participants, seq_event, state_comments, sequences = [], [], [], [], []
    seq_event = sequence_tracer(seq_data)
    seq_state_compare(state_data, seq_event)

    states, state_trigger = state.state_tracer(state_data)
    sequence_dict, life_line = sequence.sequence_tracer(seq_data)
    check_list, state_check_list = [], []

    str_trigger_matches = "MATCH\n"
    str_possible_matches = "POSSIBLE MATCH\n"
    str_no_match = "NO MATCH\n"

    for line_sequence, value in sequence_dict.items():

        sequence_line = str(value)

        for line_state, trigger in state_trigger.items():

            trigger_match = re.search(fr"\b{trigger}\b", sequence_line)
            possible_match = re.search(f"({trigger})", sequence_line)

            if trigger_match is not None:

                if trigger_match[0] in sequence_line:

                    str_trigger_matches += f"STATE:\t{line_state}\t{trigger_match[0]}\n" \
                                           f"SEQ:\t{line_sequence}\t{sequence_line}\n\n"

                    check_list.append([line_state, line_sequence])

            if possible_match is not None:

                if possible_match[0] in sequence_line and [line_state, line_sequence] not in check_list:

                    str_possible_matches += f"STATE:\t{line_state}\t{possible_match[0]}\n" \
                                            f"SEQ:\t{line_sequence}\t{sequence_line}\n\n"

                    check_list.append([line_state, line_sequence])

    for state, sequence in check_list:
        state_check_list.append(state)

    for line_state, trigger in state_trigger.items():
        if line_state not in state_check_list:
            str_no_match += f"SEQ:\t{line_state}\t{trigger}\n"

    print(str_trigger_matches)
    print(str_possible_matches)
    print(str_no_match)