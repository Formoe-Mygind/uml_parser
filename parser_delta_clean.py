import re
import sys

def parse_uml(document):

    loop_count, alt_count, end_count = [], [], []

    for lines in document:
        match_list.append(lines.split())

    for number, entry in enumerate(match_list):

        entry_str = str(entry)
        entry_str = entry_str.replace("\', \'", " ")

        if "loop" in entry_str:
            loop_count.append([number, entry_str])
        if "alt" in entry_str:
            alt_count.append([number, entry_str])
        if re.search("(?<![\w\d])end(?![\w\d])", entry_str):
            end_count.append([number, entry_str])

        if (len(entry) > 2) and (entry[0] in participant_list): participants.append([number+1, entry[3].lower()])
        if (len(entry) < 2) and (entry[0] in participant_list): participants.append([number+1, entry[1].lower()])

        if ("(" in entry_str) and ("(\"" not in entry_str):
            print(entry_str)
            entry_str = entry_str.replace("\']", "")
            entry_new_array = entry_str.split(": ")
            print(entry_str)

            commands.append([number+1, entry_new_array[1]])

        for arrow in sequence_list:

            if arrow in entry_str and [number+1, entry] not in sequences:
                sequences.append([number+1, entry])

    for state_participant in participants:
        statemachine = ""
        statemachine += "@startuml\n"
        statemachine += f"[*] --> {state_participant[1]}\n"
        statemachine += f"state {state_participant[1]}{{\n"
        last_state = ""

        for sequence_to_state in sequences:

            for state_command in commands:

                if sequence_to_state[0] == state_command[0]:

                    ext_line_num_a = re.match("^(.*?)\(", str(state_command[1]))
                    ext_line_num_b = re.search("\(([^\)]+)\)", str(state_command[1]))


                    if last_state == "":
                        statemachine += f"[*] --> {ext_line_num_a[1]}: {ext_line_num_b[0]}\n"
                        last_state = str(ext_line_num_a[1])
                    else:
                        statemachine += f"{last_state} --> {ext_line_num_a[1]}: {ext_line_num_b[0]}\n"
                        last_state = str(ext_line_num_a[1])

        statemachine += "}\n"
        statemachine += "@enduml\n"
        with open(f"statemachine_uml_{state_participant[1]}", "w") as f:
            print(state_participant[1])
            f.write(statemachine)


if __name__ == '__main__':

    sequence_list = ['->', '<-', '-->', '<--', '\[->', '<-\]']
    world_sequence = ['\[->', '<-\]']
    participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']
    match_list, participants, commands, comments, sequences = [], [], [], [], []

    data = []
    filepath = sys.argv[1]

    with open(filepath, "r") as f:
        for line in f.readlines():
            data.append(line)

    parse_uml(data)