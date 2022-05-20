@startuml
mainframe sd CPS_oblig2_test
participant "Multisensor" as temp
participant "Switch" as switch
participant "psm:PSM" as psm
participant "pim:PIM" as pim #aqua
participant "Human" as human

pim <-human : add_thermometer(1,"t")
pim-[#blue]> psm: add_thermometer(1,"t")
pim <-human : add_device(1)
pim-[#blue]>  psm: add_device(1)

pim <-human : set_temperature(20.0)
hnote over pim
too cold since last_temp is 0
end note
pim-[#blue]>  psm : SwitchOn(1)
psm [#green]-> switch : SwitchOn(1)
switch [#orange]-> temp : next_temp
pim [#green]-> human : prompt("Now entering thermostat")

temp -[#black]> psm: temperature(1,"t",20.0)
psm -[#salmon]> pim: temperature(1,"t",20.0)
hnote over pim
comfort, no change
end note

temp -[#black]> psm: temperature(1,"t",23)
psm -[#salmon]> pim: temperature(1,"t",23)
hnote over pim
too warm
end note
pim-[#blue]> psm: SwitchOff(1)
psm [#green]-> switch: SwitchOff(1)
temp <-[#orange]switch : next_temp

temp [#orange]->human : next_human

pim <- human: SwitchOn(1)
pim-[#blue]>  psm: SwitchOn(1)
psm [#green]-> switch: SwitchOn(1)
pim <-human: SwitchOff(1)
pim-[#blue]>  psm: SwitchOff(1)
psm [#green]-> switch: SwitchOff(1)

switch [#orange]->human : next_human

pim <-human : show_current_power(1)
pim-[#blue]> psm: show_current_power(1)
switch -[#purple]>psm : current_power(1, 1500)
psm -[#salmon]> pim: current_power(1, 1500)
pim [#green]->human : prompt("Current power usage in Watt: 1500")


switch [#orange]->human : next_human

pim <-human : show_total_energy(1)
pim-[#blue]> psm: show_total_energy(1)
switch -[#purple]> psm : total_energy(1, 2.4)
psm -[#salmon]> pim: total_energy(1, 2.4)
pim [#green]->human : prompt("Current total energy usage in kWh: 2.4")


@enduml