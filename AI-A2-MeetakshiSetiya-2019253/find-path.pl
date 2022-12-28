%Meetakshi Setiya, 2019253
%AI Assignment 2
%Best First Search and Depth First Search

:- consult(distances).
:- consult(heuristics).
:- dynamic path/3.
:- dynamic flag/1.

printPath([Stop|[]]) :- 
    ansi_format([fg(blue)], '~w', [Stop]).
printPath([Stop|Path]) :-
    ansi_format([fg(blue)], '~w ~w ', [Stop, '->']),
    printPath(Path).

setLinks(_, []) :- !.       %add path and distance from current to each neighbour
setLinks(CurrentNode, [ChildNode|Neighbours]) :-
    road(CurrentNode, ChildNode, Distance),
    path(PathtoCurrent, CurrentNode, DistancetoCurrent),
    DistancetoChild is Distance + DistancetoCurrent,
    assert(path([ChildNode|PathtoCurrent], ChildNode, DistancetoChild)), 
    setLinks(CurrentNode, Neighbours).

appendHeuristics(_, _, [], PQueue, PQueue).         %add heuristic to the priority queue
appendHeuristics(Destination, CurrentNode, [ChildNode|Neighbours], PQueue, FinalPQueue) :-
    (ChildNode == Destination -> 
        (assert(flag(1)), appendHeuristics(Destination, CurrentNode, [], PQueue, FinalPQueue), !); 
        (heuristic(Destination, ChildNode, DirectDistance),
        add_to_heap(PQueue, DirectDistance, ChildNode, NewPQueue),
        appendHeuristics(Destination, CurrentNode, Neighbours, NewPQueue, FinalPQueue))
        ).


%---------

performDfs(_, [], _) :-
    nl, ansi_format([bold, fg(red)], '~w', ['No path found.']), nl.

performDfs(Destination, [Destination|_], _) :- 
    path(Path, Destination, Distance), 
    reverse(Path, ActualPath), nl,
    ansi_format([bold, fg(green)], '~w', ['Path found!']),nl,
    printPath(ActualPath), nl,
    ansi_format([fg(blue)], '~w ~w ', ['Distance:', Distance]), !.

performDfs(Destination, [Current|Stack], Visited) :- 
    findall(Next, (road(Next, Current, _ ), \+ (member(Next, Visited))), Neighbours),
    append(Neighbours, Stack, NewStack),
    setLinks(Current, Neighbours),
    performDfs(Destination, NewStack, [Current|Visited]).


%---------

performBestfs(_, PQueue, _) :-
    empty_heap(PQueue),
    nl, ansi_format([bold, fg(red)], '~w', ['No path found.']), nl.

performBestfs(Destination, _, _) :-
    (flag(X), X==1),
    path(Path, Destination, Distance),
    reverse(Path, ActualPath), nl,
    ansi_format([bold, fg(green)], '~w', ['Path found!']),nl,
    printPath(ActualPath), nl,
    ansi_format([fg(blue)], '~w ~w ', ['Distance:', Distance]), !.

performBestfs(Destination, PQueue, Visited) :- 
    get_from_heap(PQueue, _, Current, NewPQueue),
    findall(Next, (road(Next, Current, _), \+ (member(Next, Visited))), Neighbours),
    appendHeuristics(Destination, Current, Neighbours, NewPQueue, FinalPQueue),
    setLinks(Current, Neighbours),
    performBestfs(Destination, FinalPQueue, [Current|Visited]).
    

%----------

depthFirstSearch(Start, Destination) :- 
    performDfs(Destination, [Start], []).

bestFirstSearch(Start, Destination) :-
    empty_heap(Init),
    (heuristic(Start, Destination, Distance) -> (
        add_to_heap(Init, Distance, Start, PQueue), performBestfs(Destination, PQueue, [])); 
        nl, ansi_format([bold, fg(red)], '~w', ['Heuristic does not exist. Exiting.']), nl).

handleSearch(Start, Destination, Choice) :- 
    assert(path([Start], Start, 0)), % path going to Start using path [Start] of distance=0
    (Choice==1 -> 
        depthFirstSearch(Start, Destination);
        Choice==2 -> 
            bestFirstSearch(Start, Destination);
        write("Wrong choice")).

start:- 
    retractall(path(_,_,_)),
    retractall(flag(_)),
    write("Enter the origin: "), read(Start),
    write("Enter the destination: "), read(Destination),
    write("Which algorithm would you like to use to get the path?\n1. Depth First Search\n2. Best First Search\n"), read(Choice),
    handleSearch(Start, Destination, Choice), nl.