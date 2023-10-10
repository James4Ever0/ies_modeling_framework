% not useable.
% :- use_module(library(clpfd)).
:- use_module(library(clpr)).

% need separation.
% Y < -1 instead of Y<-1

solve(X) :- 
    {Y > 0, Y < 1.5}, {(Y > 0.5, Y =< 1, X = 0.5 + Y; Y>1, X = 2*Y ; Y =< 0.5, X = 0.5 - Y)} , {X>1}.

solve_false(X) :-
    {X > 0, X < -1}.

% solve(X) :-
%     Y is random_float, (Y > 0.5, X = 0.5+Y; Y =< 0.5, X = 0.5-Y), X>1.

% :- use_module(library(random)).

% % Generate N random numbers and count the number of times a number less than 0.5 is generated
% count_probability(N, Prob) :-
%     count_probability(N, 0, Count),
%     Prob is Count / N.

% count_probability(0, Count, Count).
% count_probability(N, Acc, Count) :-
%     random(R),
%     ( R < 0.5 ->
%         Acc1 is Acc + 1
%     ; Acc1 is Acc
%     ),
%     N1 is N - 1,
%     count_probability(N1, Acc1, Count).

% % count_probability(1000000, Prob).