import random
import re
from ast import literal_eval
from random import randint


def color_pick():

    """
    random_temp_list = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F"}
    random_color = f"{random_temp_list[rint(1,6)]}"
    random_color += f"{rint(0,9)}"
    random_color += f"{random_temp_list[rint(1,6)]}"
    random_color += f"{rint(0, 9)}"
    random_color += f"{random_temp_list[rint(1,6)]}"
    random_color += f"{rint(0, 9)}"
    """

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

def sequence_parser(document):
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

        # ADD PARTICIPANTS
        if (len(entry) > 2) and (entry[0] in participant_list): participants.append([number+1, entry[3].lower()])
        if (len(entry) < 2) and (entry[0] in participant_list): participants.append([number+1, entry[1].lower()])

        # ADD COMMANDS
        if ("(" in entry_str) and ("(\"" not in entry_str):
            print(entry_str)
            entry_str = entry_str.replace("\']", "")
            entry_new_array = entry_str.split(": ")
            print(entry_str)

            commands.append([number+1, entry_new_array[1]])

        for arrow in sequence_list:

            if arrow in entry_str and [number+1, entry] not in sequences:
                sequences.append([number+1, entry])

    print("\nLine\tParticipants:".upper())
    for line_number, drunks in participants:
        print(f"{line_number}\t\t{drunks}")

    print("\nLine\tCommands:".upper())
    for line_number, command in commands:
       print(f"{line_number}\t\t{command}")

    print("\nLine\tSequence:".upper())

    for line_number, sequence in sequences:

        participant_one = sequence[0]
        sequence_arrow = sequence[1]
        sequence_arrow = sequence_arrow.replace("]:", "]")
        participant_two = sequence[2]
        participant_two = participant_two.replace(":", "")

        if participant_two not in participants:
            participant_two = ""

        print(f"{line_number}\t\t{participant_one} {sequence_arrow} {participant_two}")
    '''
    print(loop_count)
    print(alt_count)
    print(end_count)
    '''
    # GENERATE STATE MACHINE UML
    for state_participant in participants:
        statemachine = ""
        statemachine += "@startuml\n"
        statemachine += f"[*] --> {state_participant[1]}\n"
        statemachine += f"state {state_participant[1]} {color_pick()}{{\n"
        last_state = ""
        print(state_participant)
#        print(f"{sequences}\n")
        for sequence_to_state in sequences:

            for state_command in commands:

                if sequence_to_state[0] == state_command[0]:

                    ext = re.match("^(.*?)\(", str(state_command[1]))
                    ext2 = re.search("\(([^\)]+)\)", str(state_command[1]))

                    if last_state == "":
                        statemachine += f"[*] --> {ext[1]} {color_pick()}: {ext2[0]}\n"
                        last_state = str(ext[1])
                    else:
                        statemachine += f"{last_state} --> {ext[1]} {color_pick()}: {ext2[0]}\n"
                        last_state = str(ext[1])

        statemachine += "}\n"
        statemachine += "@enduml\n"

        with open(f"statemachine_uml_{state_participant[1]}", "w") as f:
            print(state_participant[1])
            f.write(statemachine)


if __name__ == '__main__':

    filepath = 'ob2'
    data = parse_file(filepath)

    sequence_list = ['->', '<-', '-->', '<--', '\[->', '<-\]']
    world_sequence = ['\[->', '<-\]']
    participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']

    match_list, participants, commands, comments, sequences = [], [], [], [], []
    sequence_parser(data)