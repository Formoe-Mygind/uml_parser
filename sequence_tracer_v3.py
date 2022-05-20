import sys

# Keywords and special characters used in PlantUML for sequence diagrams.
participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']
arrow_list = ['<', '>']
gate_list = ['[', ']']

global error_msg
error_msg = []


def sequence_tracer(plantuml_file):

    transitions = {}
    sequence_dictionary = {}
    tmp_dictionary = {}
    triggers_and_effects = {}
    lifelines = []
    sequence_text = ""

    for n, lines in enumerate(plantuml_file):

        sequence_dictionary[n + 1] = lines.split()
        tmp_dictionary[n + 1] = lines
        sequence_text += lines


    for line_number, line in sequence_dictionary.items():

        # Add lifelines
        if (len(line) > 2) and (line[0] in participant_list):
            lifelines.append([line_number, line[3].lower()])

        if (len(line) < 3) and (line[0] in participant_list):
            lifelines.append([line_number, line[1].lower()])

        # Checks for keywords
        traced_sequence = str(line)
        for arrow in arrow_list:

            if arrow in traced_sequence:

                # Sets gate as the transmitter of the transition ...
                if "<-]" in traced_sequence or "[->" in traced_sequence:
                    transitions[line_number] = ["gate", line[0]]
                    continue

                # ... or the receiver.
                if "->]" in traced_sequence or "[<-" in traced_sequence:
                    transitions[line_number] = [line[0], "gate"]
                    continue

                # Same goes for lifelines (participants).
                try:
                    if "<" in traced_sequence:
                        transitions[line_number] = [line[2].strip(":"), line[0]]

                    if ">" in traced_sequence:
                        transitions[line_number] = [line[0], line[2].strip(":")]
                except Exception as e:
                    error_msg.append([sys.argv[0], e])
    for line_number, line in transitions.items():
        triggers_and_effects[line_number] = str(tmp_dictionary[line_number]).split(":")[-1:]

    return sequence_text, sequence_dictionary, lifelines, transitions, triggers_and_effects
