import re

participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']
arrow_list = ['<', '>']
gate_list = ['[', ']']
transitions = {}


def sequence_tracer(document):

    document_dict = {}
    life_line = []

    for n, lines in enumerate(document):

        document_dict[n + 1] = lines.split()

    for key, value in document_dict.items():

        # ADD PARTICIPANTS
        if (len(value) > 2) and (value[0] in participant_list):
            life_line.append([key, value[3].lower()])

        if (len(value) < 3) and (value[0] in participant_list):
            life_line.append([key, value[1].lower()])

        traced_sequence = str(value)
        for arrow in arrow_list:

            if arrow in traced_sequence:

                if "<-]" in traced_sequence:
                    transitions[key] = ["gate", value[0]]
                    continue

                if "->]" in traced_sequence:
                    transitions[key] = [value[0], "gate"]
                    continue

                if "<" in traced_sequence:
                    print(traced_sequence)
                    print(value[2].strip(":"), value[0])
                    transitions[key] = [value[2].strip(":"), value[0]]

                if ">" in traced_sequence:
                    transitions[key] = [value[0], value[2].strip(":")]

    return document_dict, life_line, transitions