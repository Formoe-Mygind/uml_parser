import os
import re
from plantweb.render import render_file
from random import randint
import state_tracer_v3 as state_tracer
import sequence_tracer_v3 as sequence


EXTAB = 8  # Makes the print to terminal a bit prettier


def color_pick():
    hex_digits = "0123456789ABCDEF"
    random_color = "#"

    for i in range(6):
        if i % 2 != 0:
            random_color += hex_digits[randint(0, 9)]
        else:
            random_color += hex_digits[randint(9, 15)]

    return random_color


# Reads the passed document line by line and returns a list
def parse_file(filepath):
    document_data = []

    with open(filepath, 'r') as plantuml_file:
        lines = plantuml_file.readlines()

        for line in lines:
            if line != "\n":
                line.lower()
                document_data.append(line)

    return document_data


def save_png(uml_source, uml_type):

    infile = f'{uml_type}.dot'
    with open(infile, 'wb') as fd:
        fd.write(uml_source.encode('utf-8'))

    render_file(
        infile,
        renderopts={
            'engine': 'plantuml',
            'format': 'png'
        },
        cacheopts={
            'use_cache': False
        }
    )

    os.remove(infile)


if __name__ == '__main__':

    error_msg = []

    # Filepaths are hardcoded for demo purposes.
    state_filepath = 'example_state_machine'
    sequence_filepath = 'example_sequence_diagram'

    state_data = parse_file(state_filepath)
    sequence_data = parse_file(sequence_filepath)

    def main_parse():

        sequence_dict, lifelines, transitions, sequence_trigger_effect = sequence.sequence_tracer(sequence_data)
        states, state_trigger, state_effect, individual_state = state_tracer.state_tracer(state_data, True)

        for key, value in state_trigger.items():
            print(key, value)

        # PRINTS INFO ABOUT TRIGGERS, EFFECTS, LIFE LIFES AND TRANSITIONS TO TERMINAL.
        '''
        print("\tTRIGGER".expandtabs(EXTAB))
        for line, trigger in state_trigger.items():
            print(f"{line}\t{trigger}".expandtabs(EXTAB))
        print("\n\tEFFECT".expandtabs(EXTAB))
        for line, effect in state_effect.items():
            print(f"{line}\t{effect}".expandtabs(EXTAB))
        print()
        print(f"State\t\tStartline\tEndline".upper().expandtabs(EXTAB))
        for state_name, from_line_to_line in individual_state.items():
            print(f"{str(state_name).strip('state ').strip('{')}\t{from_line_to_line[0]}"
                  f"\t{from_line_to_line[1]}".expandtabs(
                EXTAB*2))
        print("\n\tLife line".upper().expandtabs(EXTAB))
        for line, lifeline in lifeline:
            print(f"{line}\t{lifeline}".expandtabs(EXTAB))
        print()
        print("\tfrom\tto\ttransition".upper().expandtabs(EXTAB))
        for line, transition in transitions.items():
            print(f"{line}\t{transition[0]}\t{transition[1]}\t{sequence_trigger_effect[line][-1:]}".expandtabs(EXTAB))
        '''
        def lifeline_tracer(lifeline, state_trigger):

            if lifeline in str(states).lower():

                for sequence_diagram_line, tx_rx in transitions.items():
                    tx = tx_rx[0]
                    rx = tx_rx[1]

                    # If lifeline is receiving
                    if lifeline == rx:
                        sequence_trigger_match = re.search(r"\w+", str(sequence_trigger_effect[sequence_diagram_line][
                                                                       -1:]))
                        state_flag = False

                        for line_number, trigger in state_trigger.items():

                            trigger_match = re.search(fr"\b{trigger[1:]}", str(sequence_data[sequence_diagram_line -
                                                                                             1]))

                            if trigger_match is not None:
                                state_flag = True

                                color = color_pick()

                                found_triggers.append(trigger[1:])

                                gen_seq_rx[sequence_diagram_line] = [sequence_data[sequence_diagram_line - 1],
                                                             f"note right {lifeline} "
                                                             f"{color}: TRIGGER"]

                                print()

                                for state, lines in individual_state.items():

                                    if lifeline in str(state).lower():
                                        continue

                                    if line_number in range(lines[0], lines[1]):
                                        gen_state_rx[state] = color

                        if not state_flag and sequence_trigger_match[0] not in found_triggers:
                            print(f"NOT FOUND!\nSEQ MATCH:\t{sequence_trigger_match}".expandtabs(EXTAB))
                            gen_seq_rx[sequence_diagram_line] = [sequence_data[sequence_diagram_line - 1],
                                                                 f"note right {lifeline} "
                                                                   f"#EB6060: "
                                                                   f"{sequence_trigger_match[0]} not "
                                                                   f"found in state"]

                            found_sequence.append(sequence_trigger_match[0])

                    # If lifeline is transmitting
                    if lifeline == tx:
                        sequence_effect_match = re.search(r"\w+", str(sequence_trigger_effect[sequence_diagram_line][
                                                                      -1:]))
                        state_flag = False

                        for _, effect in state_effect.items():

                            effect_match = re.search(fr"\b{effect[1:]}", str(sequence_data[sequence_diagram_line - 1]))

                            if effect_match is not None:
                                state_flag = True

                                # print("SEQ MATCH:\t", sequence_effect_match)
                                #print(f"STATE MATCH:\t{effect_match}".expandtabs(EXTAB))

                                found_effects.append(effect[1:])

                                gen_seq_tx[sequence_diagram_line] = [sequence_data[sequence_diagram_line - 1],
                                                                        f"note left {lifeline} "
                                                                        f"{color}: EFFECT"]

                                for state, lines in individual_state.items():

                                    if lifeline in str(state).lower():
                                        continue
                                    if _ in range(lines[0], lines[1]):
                                        gen_state_tx[state] = color

                        if not state_flag:
                            print("SEQ MATCH:\t", sequence_effect_match)

                def user_input():
                    user_correction = int(input("Correction: \n"))

                    if user_correction == counter:
                        try:
                            found_triggers.append(trigger[1:])
                        except Exception as e:
                            print(e)

                    if user_correction > counter or counter <= 0:
                        print("Not a valid option.")
                        user_input()

                    if 0 < user_correction < counter:
                        replacement = found_sequence[user_correction - 1]

                        for num, entry in enumerate(sequence_data):
                            state_data[num] = state_data[num].replace(f"{trigger[1:]}", replacement)

                        if replacement not in found_triggers:
                            found_triggers.append(replacement)

                        state_trigger = state_tracer.state_tracer(state_data, False)
                        lifeline_tracer(lifeline, state_trigger)

                for line_n, trigger in state_trigger.items():

                    if trigger[1:] not in found_triggers:
                        print(trigger[1:], found_triggers)
                        print(f"----------\nSTATE TRIGGER {trigger[1:]}\n\n"
                              f"{line_n} {state_data[line_n - 1]}\nwas not found in sequence diagram life line for"
                              f" {lifeline}\nDid you mean:\n")
                        counter = 1
                        for n, entry in enumerate(found_sequence):
                            print(f"{n + 1}\t{entry}")
                            counter += 1
                        print(f"{counter}\tNone of the above\n")

                        #user_input()

        for n, lifeline in lifelines:
            gen_seq_rx, gen_seq_tx = {}, {}
            gen_state_rx, gen_state_tx = {}, {}
            found_triggers, found_effects, found_sequence = [], [], []

            lifeline_tracer(lifeline, state_trigger)

        sequence_test = ""

        for num, line in enumerate(sequence_data):
            num += 1

            if gen_seq_rx.get(num):
                sequence_test += gen_seq_rx.get(num)[1] + "\n"
                sequence_test += gen_seq_rx.get(num)[0]
            elif gen_seq_tx.get(num):
                sequence_test += gen_seq_tx.get(num)[1] + "\n"
                sequence_test += gen_seq_tx.get(num)[0]
            else:
                sequence_test += line

        '''
        with open("generated_sequence.plantuml", "w") as generated_sequence:
            generated_sequence.write(sequence_test)

        state_text = ""

        for num, line in enumerate(state_data):
            text_line = str(line.strip())
            if gen_state_rx.get(text_line):
                state_text += line.replace("{", f" {gen_state_rx.get(text_line)} {{")
            else:
                state_text += line

        with open("generated_statemachine.plantuml", "w") as generated_stat:
            generated_stat.write(state_text)
        
        try:
            save_png(state_text, f"{lifeline}_state")
            save_png(sequence_test, f"{lifeline}_sequence")
        except Exception as e:
            print(e)
        '''

    main_parse()
