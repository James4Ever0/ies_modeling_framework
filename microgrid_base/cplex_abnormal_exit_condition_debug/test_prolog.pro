:- use_module(library(clpfd)). % for transpose/2.

port(bat_port1).
port(generator_port1).
port(load_port1).

idle_port(bat_port1).
idle_port(generator_port1).
idle_port(load_port1).

input_port(bat_port1).
input_port(load_port1).

output_port(bat_port1).
output_port(generator_port1).

device(battery).
device(load).
device(generator).

device(DEVICE_NAME):- device(DEVICE_TYPE), call(DEVICE_TYPE, DEVICE_NAME).

battery(battery1).
generator(generator1).
load(load1).

port_mapping(battery1, bat_port1).
port_mapping(generator1, generator_port1).
port_mapping(load1, load_port1).

energy(electricity).

electricity(bat_port1).
electricity(generator_port1).
electricity(load_port1).

list_member(X,[X|_]).
list_member(X,[_|TAIL]) :- list_member(X, TAIL).

% port_list_member(X, LIST):- list_member(X, LIST), port(X).

all_satisfy_constraint([], _).
all_satisfy_constraint([H|T], Constraint) :-
    call(Constraint, H),
    all_satisfy_constraint(T, Constraint).

all_with_same_type(PORT_LIST, ENERGY_TYPE) :- energy(ENERGY_TYPE), all_satisfy_constraint(PORT_LIST, ENERGY_TYPE).

port_status(PORT, input) :- input_port(PORT).
port_status(PORT, output):- output_port(PORT).
port_status(PORT, idle):- idle_port(PORT).

input_status(STATUS) :- STATUS = input.
output_status(STATUS) :- STATUS = output.
idle_status(STATUS) :- STATUS = idle.

apply_list([], [], _).
apply_list([INP], [RET], FUNC) :- call(FUNC, INP, RET).
apply_list([INP|INP_TAIL], [RET|RET_TAIL], FUNC) :- apply_list(INP_TAIL, RET_TAIL, FUNC), call(FUNC, INP, RET).

port_status_list(PORT, STATUS) :- apply_list(PORT, STATUS, port_status).

adder(adder1, [bat_port1, generator_port1, load_port1]).

% battery port must have input state.
% load port must have input state.

adder_port_status(ADDER, [ENERGY_TYPE|[STATUS_LIST]]) :- 
    adder(ADDER, PORT_LIST),
    all_satisfy_constraint(PORT_LIST, port),
    all_with_same_type(PORT_LIST, ENERGY_TYPE),
    port_status_list(PORT_LIST, STATUS_LIST),
    (
        list_member(STATUS_X, STATUS_LIST), list_member(STATUS_Y, STATUS_LIST),STATUS_X=input, STATUS_Y = output;
        all_satisfy_constraint(STATUS_LIST, idle_status)
    ).

adder_port_all_status(ADDER, ALL_STATUS):-
    findall(STATUS, adder_port_status(ADDER, STATUS), ALL_STATUS).

adder_port_status_list(ADDER_LIST, ADDER_STATUS_LIST) :- apply_list(ADDER_LIST, ADDER_STATUS_LIST, adder_port_status).

% had better not to go any further.
% topology_status(ADDER_LIST, E, P) :- adder_port_status_list(ADDER_LIST, ADDER_STATUS_LIST), transpose(ADDER_STATUS_LIST, [E|P]), P=[[bat_port1_status, generator_port1_status, ]].