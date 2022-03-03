import re
#installer pyCharm plantUML modul
rx_dict = {
    'mainframe': re.compile(r"mainframe\s*(?P<mainframe>.*)"),
    'participant': re.compile(r"as\s*(?P<participant>.*)"),
    'human_to_pim': re.compile(r"pim\s*<-]\s*:\s*(?P<human_to_pim>.*(?=[(]))"),
    'pim_to_psm': re.compile(r"pim\s*->\s*psm:\s*(?P<pim_to_psm>.*(?=[(]))"),
    'pim_to_human': re.compile(r"pim\s*->]\s*:\s*(?P<pim_to_human>.*(?=[(]))"),
    'loop': re.compile(r"loop(?P<loop>)"),
    'psm_to_pim': re.compile(r"psm\s*->\s*pim:\s*(?P<psm_to_pim>.*(?=[(]))"),
    'alt': re.compile(r"alt(?P<alt>)"),
    'else': re.compile(r"else(?P<else>.*)"),
    'end': re.compile(r"end\n(?P<end>)"),
    'startuml': re.compile(r"@startuml(?P<startuml>)"),
    'enduml': re.compile(r"@enduml(?P<enduml>)")
}

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_file(filepath):
    data = []
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            key, match = _parse_line(line)
            #print(match)

            def structure(group_key, gr_name):
                if key == str(gr_name):
                    group_key = match.group(str(gr_name))
                    row = {str(gr_name).upper(): group_key}
                    data.append(row)

            for gr_name,_ in rx_dict.items():
                structure(key, gr_name)

            line = file_object.readline()

    return data

def mapping(data):
    new_dict = {
        'STARTUML': '@startuml\nskinparam defaultTextAlignment left',

        'PARTICIPANT': '[*] --> {participant}\nstate {participant} ##[bold]brown{clamp}\n',

        'HUMAN_TO_PIM': '{prev_state} --> {next_state}',

        'LOOP': 'Thermostat --> Thermostat',

        'ENDUML': '}\n@enduml'
    }


    state_machine = []
    for key in new_dict:
        #print(keys)
        #print(new_dict[keys])
        for rx_keys in data:
            #print(rx_keys)
            for keys in rx_keys:
                if key == keys:
                 state_machine.append([keys, new_dict[key], rx_keys[keys]])
                 #print(rx_keys[keys])

    print(state_machine)
    for element in state_machine:
        if "PARTICIPANT" in element:
            try:
                f = open(str(element[2])+"_behavior", "x")
                f.close
            except:
                continue
            finally:
                count = 0
                prev_val = ''
                for elements in state_machine:
                    if "PARTICIPANT" not in elements:
                        if count == 1:
                            f = open(str(element[2]) + "_behavior", "a")
                            f.write("[*] ---> " + elements[2] + "\n")

                        elif count > 1 and count < (len(state_machine)-6):
                            f = open(str(element[2]) + "_behavior", "a")
                            f.write((elements[1]+ "\n").format(prev_state = str(prev_val), next_state = elements[2]))


                        else:
                            f = open(str(element[2]) + "_behavior", "a")
                            f.write(elements[1] + elements[2] + "\n")
                        count += 1
                        prev_val = elements[2]

                    elif element[2] == elements[2]:
                        f = open(str(element[2]) + "_behavior", "a")
                        f.write(str(elements[1]).format(participant=str(elements[2]) + "_behavior", clamp="{"))

if __name__ == '__main__':
    filepath = 'sequence_diagram'
    data = parse_file(filepath)
    mapping(data)
    #print(data)