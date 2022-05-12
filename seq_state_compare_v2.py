import re
from random import randint
import state_tracer
import sequence_tracer as sequence


EXTAB = 8  # Makes the print to terminal a bit prettier
# FILEPATHS ARE HARDCODED FOR DEMO PURPOSES.


def color_pick():

    hex_digits = "0123456789ABCDEF"
    random_color = "#"
    for i in range(6):
        if i % 2 != 0:
            random_color += hex_digits[randint(0, 9)]
        else:
            random_color += hex_digits[randint(9, 15)]

    return random_color


# READS THE PASSED DOCUMENT LINE BY LINE AND PUTS EACH LINE IN AN ARRAY WHICH IS THEN RETURNED
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

    state_filepath = 'example_state_machine'
    #state_filepath = 'generated_statemachine.plantuml'
    sequence_filepath = 'example_sequence_diagram'

    state_data = parse_file(state_filepath)
    sequence_data = parse_file(sequence_filepath)


    def main_parse():

        states, state_trigger, state_effect, state_lines_index = state_tracer.state_tracer(state_data, True)
        sequence_dict, life_line, transitions, seq_trig_effect = sequence.sequence_tracer(sequence_data)


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
        for state_name, from_line_to_line in state_lines_index.items():
            print(f"{str(state_name).strip('state ').strip('{')}\t{from_line_to_line[0]}"
                  f"\t{from_line_to_line[1]}".expandtabs(
                EXTAB*2))
        print("\n\tLife line".upper().expandtabs(EXTAB))
        for line, lifeline in life_line:
            print(f"{line}\t{lifeline}".expandtabs(EXTAB))
        print()
        print("\tfrom\tto\ttransition".upper().expandtabs(EXTAB))
        for line, transition in transitions.items():
            print(f"{line}\t{transition[0]}\t{transition[1]}\t{seq_trig_effect[line][-1:]}".expandtabs(EXTAB))
        '''
        def life_line_check(life_line, state_trigger):


            print()



            life_line_triggers = ""
            life_line_effects = ""

            if life_line in str(states).lower():

                for sequence_line, tx_rx in transitions.items():
                    tx = tx_rx[0]
                    rx = tx_rx[1]

                    # IF LIFE LINE IS RECEIVING
                    if life_line == rx:
                        sequence_trigger_match = re.search(r"\w+", str(seq_trig_effect[sequence_line][-1:]))
                        state_flag = False

                        for _, trigger in state_trigger.items():

                            trigger_match = re.search(fr"\b{trigger[1:]}", str(sequence_data[sequence_line - 1]))

                            if trigger_match is not None:
                                state_flag = True

                                #print(f"STATE MATCH:\t{trigger_match}".expandtabs(EXTAB))

                                color = color_pick()

                                # FOR FINAL PRINTOUT OF INFORMATION REGARDING TRIGGERS
                                life_line_triggers += \
                                    f"TRIGGER:\t{trigger[1:]}\nSEQUENCE\t{sequence_line}" \
                                    f" {sequence_data[sequence_line]}" \
                                    f"STATE\t\t{_} {state_data[_ - 1]}\n"

                                found_triggers.append(trigger[1:])
                                gen_seq_rx[sequence_line] = [sequence_data[sequence_line - 1],
                                                             f"note right {life_line} "
                                                             f"{color}: TRIGGER"]
                                #print(f"TRIGGER:\t{trigger[1:]}\t{color}".expandtabs(EXTAB))
                                print()

                                for state, lines in state_lines_index.items():

                                    if life_line in str(state).lower():
                                        continue
                                    if _ in range(lines[0], lines[1]):
                                        gen_state_rx[state] = color

                        if not state_flag and sequence_trigger_match[0] not in found_triggers:
                            print(f"NOT FOUND!\nSEQ MATCH:\t{sequence_trigger_match}".expandtabs(EXTAB))
                            gen_seq_rx[sequence_line] = [sequence_data[sequence_line - 1], f"note right {life_line} "
                                                                                           f"#EB6060: "
                                                                                           f"{sequence_trigger_match[0]} not "
                                                                                           f"found in state"]
                            print()
                            found_sequence.append(sequence_trigger_match[0])
                            print("FOUND SEQ: ", found_sequence)

                    # IF LIFE LINE IS SENDING
                    if life_line == tx:
                        sequence_effect_match = re.search(r"\w+", str(seq_trig_effect[sequence_line][-1:]))
                        state_flag = False

                        for _, effect in state_effect.items():

                            eff_match = re.search(fr"\b{effect[1:]}", str(sequence_data[sequence_line - 1]))

                            if eff_match is not None:
                                state_flag = True
                                # print("SEQ MATCH:\t", sequence_effect_match)
                                #print(f"STATE MATCH:\t{eff_match}".expandtabs(EXTAB))

                                found_effects.append(effect[1:])

                                # FOR FINAL PRINTOUT OF INFORMATION REGARDING EFFECTS
                                life_line_effects += f"EFFECT:\t\t{effect[1:]}\nSEQUENCE\t{sequence_line}" \
                                                     f" {sequence_data[sequence_line - 1]}" \
                                                     f"STATE\t\t{_} {state_data[_ - 1]}\n"

                                gen_seq_tx[sequence_line] = [sequence_data[sequence_line - 1], f"note left {life_line} "
                                                                                               f"{color}: EFFECT"]
                                #print(f"EFFECT:\t\t{effect[1:]}\t{color}".expandtabs(EXTAB))
                                #print()

                                for state, lines in state_lines_index.items():

                                    if life_line in str(state).lower():
                                        continue
                                    if _ in range(lines[0], lines[1]):
                                        gen_state_tx[state] = color

                        if not state_flag:
                            print("SEQ MATCH:\t", sequence_effect_match)
                '''
                print(f"{life_line} triggers\n".upper())
                print(life_line_triggers)
                print()
                print(f"{life_line} effects\n".upper())
                print(life_line_effects)
                '''

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

                        print(replacement)
                        for num, entry in enumerate(state_data):
                            state_data[num] = state_data[num].replace(f"{trigger[1:]}", replacement)
                        found_triggers.append(replacement)
                        state_trigger = state_tracer.state_tracer(state_data, False)
                        life_line_check(life_line, state_trigger)


                for line_n, trigger in state_trigger.items():

                    if trigger[1:] not in found_triggers:
                        print(trigger[1:], found_triggers)
                        print(f"----------\nSTATE TRIGGER {trigger[1:]}\n\n"
                              f"{line_n} {state_data[line_n - 1]}\nwas not found in sequence diagram life line for"
                              f" {life_line}\nDid you mean:\n")
                        counter = 1
                        for n, entry in enumerate(found_sequence):
                            print(f"{n + 1}\t{entry}")
                            counter += 1
                        print(f"{counter}\tNone of the above\n")

                        user_input()


        for n, life_line in life_line:
            gen_seq_rx, gen_seq_tx = {}, {}
            gen_state_rx, gen_state_tx = {}, {}
            found_triggers, found_effects, found_sequence = [], [], []
            life_line_check(life_line, state_trigger)

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

    main_parse()