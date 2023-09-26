% % use our dictionary.
% % Define a dynamic fact to represent a key-value pair
% :- dynamic pair/2.

% % Define a predicate to add a key-value pair to the dictionary
% add_pair(Key, Value) :-
%    \+ pair(Key, _), % Check if the key already exists
%    assert(pair(Key, Value)).

% % Define a predicate to remove a key-value pair from the dictionary
% remove_pair(Key) :-
%    retract(pair(Key, _)).

% % Define a predicate to look up a value by key
% get_value(Key, Value) :-
%    pair(Key, Value).

:- use_module(library(dicts)).
:- A = point{a:1}, B = point{b:1}, print(A), print(B), dicts_same_tag([A, B], Tag), print(Tag), dicts_same_tag([A], Tag), print(Tag).