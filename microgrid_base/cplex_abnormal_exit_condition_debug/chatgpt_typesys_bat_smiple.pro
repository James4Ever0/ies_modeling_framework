% Define the devices and their ports
device(battery, [port1]).
device(generator, [port1]).

% Define the working conditions for each device
working_condition(battery, [port1, charging]).
working_condition(generator, [port1, output]).

% Define the rules for using the devices
rule_battery(port1, charging).
rule_generator(port1, output).

% Define the adder device and its rules
device(adder, [port1, port2, port3]).
working_condition(adder, [port1, port2, port3, input, output]).
rule_adder(port1, input).
rule_adder(port2, input).
rule_adder(port3, output).

% Define a predicate to enumerate all working conditions
enumerate_working_conditions(Conditions) :-
    findall(Device-Ports-Conditions, (
        device(Device, Ports),
        working_condition(Device, Conditions),
        apply_rules(Ports, Conditions),
        check_adder(Conditions)
    ), Conditions).

% Define a predicate to apply the rules to a set of ports and conditions
apply_rules(Ports, Conditions) :-
    forall((member(Port, Ports), rule(Device, Port, Condition)),
           member(Device-Condition, Conditions)).

% Define a predicate to check the adder device
check_adder(Conditions) :-
    member(adder-[P1, P2, P3, input, output]-C1, Conditions),
    member(battery-[P1, C2]-C2, Conditions),
    member(generator-[P2, C3]-C3, Conditions),
    (member(adder-[P3, input, output]-C4, Conditions) ; C4 = C1).
