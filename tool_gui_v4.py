import os
import sys
from time import sleep
import re
from plantweb.render import render_file
from random import randint
import state_tracer_v3 as state_tracer
import sequence_tracer_v3 as sequence
import PyQt5.uic
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel

'''
class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        PyQt5.uic.loadUi('cps_app.ui', self)

        self.display_seq = QLabel(self)
        self.display_state = QLabel(self)

        self.btn_seq.clicked.connect(self.browse_seq)
        self.btn_state.clicked.connect(self.browse_state)
        #self.btn_check.clicked.connect(self.display_state)

    def browse_seq(self):
        fname = QFileDialog.getOpenFileName(self, 'Open sequence file')
        self.line_seq.setText(fname[0])
        self.sequence_path = fname[0]


    def browse_state(self):
        fname = QFileDialog.getOpenFileName(self, 'Open state file')
        self.line_state.setText(fname[0])
        self.state_path = fname[0]

    def display_state(self):
        run_main()
        self.display_seq.setPixmap(QtGui.QPixmap("pim_state.png"))
        self.display_state.setPixmap(QtGui.QPixmap("pim_sequence.png"))
'''


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


def choose_lifeline():
    for choice, lifeline in enumerate(lifelines):
        print(choice + 1, lifeline[1])
    try:
        input_lifeline = int(input("Choose a lifeline:\t"))
        main_parse(lifelines[input_lifeline - 1][1])

    except Exception:
        print("\nInvalid choice. Try again.\n")
        choose_lifeline()


def main_parse(lifeline):

    global sequence_text

    modified_output = False

    matched_trigger, matched_effect = [], []
    unmatched_trigger, unmatched_effect = [], []

    for sequence_diagram_line, tx_rx in transitions.items():

        tx = tx_rx[0]
        rx = tx_rx[1]

        if lifeline == rx:

            state_active = False

            sequence_trigger_match = re.search(r"\w+",
                                               str(sequence_trigger_effect[sequence_diagram_line][-1:]))

            for line_number, trigger in state_trigger.items():
                state_trigger_match = re.search(fr"\b{trigger[1:]}",
                                                str(sequence_data[sequence_diagram_line - 1]))

                if state_trigger_match is not None:

                    state_active = True

                    matched_trigger.append(trigger[1:])

            if not state_active and sequence_trigger_match[0] not in matched_trigger:

                unmatched_trigger.append(sequence_trigger_match[0])

        if lifeline == tx:

            state_active = False

            sequence_effect_match = re.search(r"\w+",
                                              str(sequence_trigger_effect[sequence_diagram_line][-1:]))

            for line_number, effect in state_effect.items():
                state_effect_match = re.search(fr"\b{effect[1:]}",
                                               str(sequence_data[sequence_diagram_line - 1]))

                if state_effect_match is not None:

                    state_active = True

                    matched_effect.append(effect[1:])

            if not state_active:
                unmatched_effect.append([lifeline, sequence_effect_match[0]])

    for key, element in individual_state.items():

        state = key.strip("state ").lower()
        state = state.strip("{")

        trigger_ok, effect_ok = False, False
        counter = 0

        if lifeline in state:
            pass
        else:
            print(state, element[0], element[1])

            for i in range(element[0], element[1]):

                for key, line in sequence_trigger_effect.items():

                    line_stripped = re.search(r"\w+", line[0])

                    if f"?{line_stripped[0]}" in state_data[i]:
                        trigger_ok = True
                    if f"!{line_stripped[0]}" in state_data[i]:
                        effect_ok = True

            if trigger_ok and effect_ok:
                for j in range(element[0] - 1, element[1]):
                    state_data[j] = state_data[j].replace("{", " #00B4AA {")


    for line_number, trigger in state_trigger.items():

        if trigger[1:] not in matched_trigger and len(unmatched_trigger) > 0:

            print("Unmatched trigger(s) in sequence diagram:")

            for unmatched in unmatched_trigger:

                print(unmatched)

                print(f"\nReplace with:\n")
                n = 1
                input_dictionary = {}
                for key, value in state_trigger.items():
                    print(n, value[1:])
                    input_dictionary[n] = value[1:]
                    n += 1

                print(n, "none of the above")

                user_input = int(input("Number: "))

                if 0 < user_input < n:

                    modified_output = True
                    sequence_text = sequence_text.replace(unmatched, input_dictionary[user_input])
                    matched_trigger.append(unmatched)
                    print()
                    print(f"Replaced {unmatched} with {input_dictionary[user_input]}\n")
                    unmatched_trigger.remove(unmatched)

                else:

                    matched_trigger.append(unmatched)
                    unmatched_trigger.remove(unmatched)

    if modified_output:
        with open("mod_sequence.plantuml", "w+") as f:
            f.write(sequence_text)

# Filepaths are hardcoded for demo purposes.
state_filepath = 'example_state_machine'
sequence_filepath = 'example_sequence_diagram'

state_data = parse_file(state_filepath)
sequence_data = parse_file(sequence_filepath)

sequence_text, sequence_dict, lifelines, transitions, sequence_trigger_effect = sequence.sequence_tracer(sequence_data)
states, state_trigger, state_effect, individual_state = state_tracer.state_tracer(state_data, True)


choose_lifeline()

for lin in state_data:
    print(lin)

'''
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(MainWindow())
widget.show()
sys.exit(app.exec_())
'''