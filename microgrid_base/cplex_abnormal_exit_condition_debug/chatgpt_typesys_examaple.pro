% Define the devices and their ports
device(solar_panel, [port1]).
device(battery, [port1, port2]).
device(wind_turbine, [port1]).

% Define the working conditions for each device
working_condition(solar_panel, [port1, day]).
working_condition(battery, [port1, port2, day, night]).
working_condition(wind_turbine, [port1, wind_speed]).

% Define the rules for using the devices
rule_solar_panel(port1, day).
rule_battery(_).
rule_wind_turbine(port1, WindSpeed) :- WindSpeed > 5.

% Define a predicate to enumerate all working conditions
enumerate_working_conditions(Conditions) :-
    findall(Device-Ports-Conditions, (
        device(Device, Ports),
        working_condition(Device, Conditions),
        apply_rules(Ports, Conditions)
    ), Conditions).

% Define a predicate to apply the rules to a set of ports and conditions
apply_rules(Ports, Conditions) :-
    forall((member(Port, Ports), rule(Device, Port, Condition)),
           member(Device-Condition, Conditions)).
