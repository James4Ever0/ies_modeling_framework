
% :- use_module(library(clpfd)).

port(光伏发电_0_电接口).
port(光伏发电_2_电接口).
port(柴油_4_燃料接口).
port(柴油发电_6_电接口).
port(柴油发电_6_燃料接口).
port(变流器_9_电输入).
port(变流器_9_电输出).
port(变压器_12_电输入).
port(变压器_12_电输出).
port(电负荷_15_电接口).
port(锂电池_17_电接口).
port(双向变流器_22_线路端).
port(双向变流器_22_储能端).

input_port(柴油发电_6_燃料接口).
input_port(变流器_9_电输入).
input_port(变压器_12_电输入).
input_port(变压器_12_电输出).
input_port(电负荷_15_电接口).
input_port(锂电池_17_电接口).
input_port(双向变流器_22_线路端).
input_port(双向变流器_22_储能端).

output_port(光伏发电_0_电接口).
output_port(光伏发电_2_电接口).
output_port(柴油_4_燃料接口).
output_port(柴油发电_6_电接口).
output_port(变流器_9_电输出).
output_port(变压器_12_电输入).
output_port(变压器_12_电输出).
output_port(锂电池_17_电接口).
output_port(双向变流器_22_线路端).
output_port(双向变流器_22_储能端).

idle_port(光伏发电_0_电接口).
idle_port(光伏发电_2_电接口).
idle_port(柴油_4_燃料接口).
idle_port(柴油发电_6_电接口).
idle_port(柴油发电_6_燃料接口).
idle_port(变流器_9_电输入).
idle_port(变流器_9_电输出).
idle_port(变压器_12_电输入).
idle_port(变压器_12_电输出).
idle_port(电负荷_15_电接口).
idle_port(锂电池_17_电接口).
idle_port(双向变流器_22_线路端).
idle_port(双向变流器_22_储能端).


device(锂电池).
device(双向变流器).
device(光伏发电).
device(变流器).
device(柴油发电).
device(变压器).
device(柴油).
device(电负荷).

device(DEVICE_NAME):- device(DEVICE_TYPE), call(DEVICE_TYPE, DEVICE_NAME).

光伏发电(光伏发电_0).
光伏发电(光伏发电_2).

柴油(柴油_4).

柴油发电(柴油发电_6).

变流器(变流器_9).

变压器(变压器_12).

电负荷(电负荷_15).

锂电池(锂电池_17).

双向变流器(双向变流器_22).


port_mapping(光伏发电_0, 光伏发电_0_电接口).
    
port_mapping(光伏发电_2, 光伏发电_2_电接口).
    
port_mapping(柴油_4, 柴油_4_燃料接口).
    
port_mapping(柴油发电_6, 柴油发电_6_电接口).
port_mapping(柴油发电_6, 柴油发电_6_燃料接口).
    
port_mapping(变流器_9, 变流器_9_电输入).
port_mapping(变流器_9, 变流器_9_电输出).
    
port_mapping(变压器_12, 变压器_12_电输入).
port_mapping(变压器_12, 变压器_12_电输出).
    
port_mapping(电负荷_15, 电负荷_15_电接口).
    
port_mapping(锂电池_17, 锂电池_17_电接口).
    
port_mapping(双向变流器_22, 双向变流器_22_线路端).
port_mapping(双向变流器_22, 双向变流器_22_储能端).
    

energy(柴油).
energy(电).

电(光伏发电_0_电接口).
电(光伏发电_2_电接口).
电(柴油发电_6_电接口).
电(变流器_9_电输入).
电(变流器_9_电输出).
电(变压器_12_电输入).
电(变压器_12_电输出).
电(电负荷_15_电接口).
电(锂电池_17_电接口).
电(双向变流器_22_线路端).
电(双向变流器_22_储能端).

柴油(柴油_4_燃料接口).
柴油(柴油发电_6_燃料接口).


list_member(X,[X|_]).
list_member(X,[_|TAIL]) :- list_member(X, TAIL).

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

adder(adder19, [光伏发电_0_电接口, 光伏发电_2_电接口, 柴油发电_6_电接口, 变流器_9_电输入]).
adder(adder21, [变流器_9_电输出, 双向变流器_22_线路端, 变压器_12_电输入]).
adder(adder_1, [双向变流器_22_储能端, 锂电池_17_电接口]).
adder(adder_2, [柴油_4_燃料接口, 柴油发电_6_燃料接口]).
adder(adder_3, [电负荷_15_电接口, 变压器_12_电输出]).

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
