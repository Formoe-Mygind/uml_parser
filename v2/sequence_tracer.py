# KEYWORDS AND SPECIAL CHARACTERS USED IN PlantUML FOR SEQUENCE DIAGRAMS
participant_list = ['participant', 'actor', 'boundry', 'control', 'entitiy', 'database', 'queue']
arrow_list = ['<', '>']
gate_list = ['[', ']']
transitions = {}


def sequence_tracer(document):

    document_dict = {}
    sequence_events_and_triggers = {}
    seq_event_trig = {}
    life_line = []

    for n, lines in enumerate(document):

        document_dict[n + 1] = lines.split()
        sequence_events_and_triggers[n + 1] = lines.split(":")

    for key, value in document_dict.items():

        # ADD PARTICIPANTS
        if (len(value) > 2) and (value[0] in participant_list):
            life_line.append([key, value[3].lower()])

        if (len(value) < 3) and (value[0] in participant_list):
            life_line.append([key, value[1].lower()])

        # CHECKS EACH LINE FOR KEYWORDS
        traced_sequence = str(value)
        for arrow in arrow_list:

            if arrow in traced_sequence:

                # SETS GATE AS THE TRANSMITTER OF THE TRANSITION
                if "<-]" in traced_sequence:
                    transitions[key] = ["gate", value[0]]
                    continue

                # ... OR THE RECEIVER
                if "->]" in traced_sequence:
                    transitions[key] = [value[0], "gate"]
                    continue

                # SAME GOES FOR PARTICIPANTS / LIFE LINES
                if "<" in traced_sequence:
                    transitions[key] = [value[2].strip(":"), value[0]]

                if ">" in traced_sequence:
                    transitions[key] = [value[0], value[2].strip(":")]

    for key, value in transitions.items():
        seq_event_trig[key] = sequence_events_and_triggers[key]

    return document_dict, life_line, transitions, seq_event_trig
