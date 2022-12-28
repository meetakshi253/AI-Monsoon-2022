%Meetakshi Setiya, 2019253
%AI Assignment 1
%Electives Advisory System

:- dynamic grade/2. %for improvement courses
:- dynamic queried/1.
:- dynamic inadequate/1.
:- dynamic type/2.
:- dynamic priority/1.

stream_code(1, 'CSE').
stream_code(2, 'ECE').
stream_code(3, 'CSAM').
stream_code(4, 'CSD').
stream_code(5, 'CSAI').
stream_code(6, 'CSB').
stream_code(7, 'CSSS').

colourmap('Department Mandatory', 'blue').
colourmap('Available for Improvement', 'yellow').
colourmap('Elective per Interest', 'green').
colourmap('Suggested Specialization Elective', 'cyan').
colourmap('Research', 'green').

electives_code(1, 'AI and ML').
electives_code(2, 'Security and Cryptography').
electives_code(3, 'Algorithms').
electives_code(4, 'Theoretical Computer Science').
electives_code(5, 'Systems and Software Development').
electives_code(6, 'Mathematics').
electives_code(7, 'Computational Biology').
electives_code(8, 'Hardware and Electronics').
electives_code(9, 'Design').
electives_code(10, 'Humanities and Social Science').

%map electives to X stream so these can also be considered
related(2, 8).
related(3, 6).
related(4, 9).
related(5, 1).
related(6, 7).
related(7, 10).

% at least 12 cse and 12 X
mandatory(1, ['Computer Networks', 'Technical Communication', 'Environmental Science']).
mandatory(2, ['Digital Communication Systems', 'Digital Signal Processig', 
              'Technical Communication', 'Environmental Science']).
mandatory(3, ['Scientific Computing', 'Probability and Random Processes', 'Linear Optimization', 
              'Statistical Inference', 'Technical Communication', 'Environmental Science']).
mandatory(4, ['Computer Networks', 'Research Methods in Social Science and Design', 
              'Design of Interactive Systems', 'Technical Communication', 'Environmental Science']).
mandatory(5, ['Machine Learning', 'Computer Networks', 'Artificial Intelligence', 'Ethics in AI', 
              'Technical Communication', 'Environmental Science']).
mandatory(6, ['Biophysics', 'Algorithms in Computational Biology', 'Technical Communication', 
              'Environmental Science']).
mandatory(7, ['Computer Networks', 'Technical Communication', 'Environmental Science']).


electives(1, ['Artificial Intelligence', 'Machine Learning', 'Natural Language Processing',
              'Reinforcement Learning', 'Data Mining', 'Meta Learning', 'Edge AI',
              'Computer Vision', 'Deep Learning']).
electives(2, ['Foundations Of Computer Security', 'Network Anonymity & Privacy', 'Applied Cryptography', 
              'Topics In Adaptive Cybersecurity', 'Topics In Cryptanalysis', 'Networks And System Security II',
              'Advanced Biometrics']).
electives(3, ['Modern Algorithm Design', 'Advanced Algorithms', 'Introdiction to Graduate Algorithms',
              'Randomised Algorithms', 'Concurrent and Learned Data Structures', 'Approximation Algorithms',
              'Network Science']).
electives(4, ['Introduction to Quantum Computing', 'Theory of Computation', 'Program Verification',
              'Complexity Theory', 'Program Analysis', 'Decision Procedures']).
electives(5, ['Distributed Systems: Concepts & Design', 'Parallel Runtimes For Modern Processors',
              'Compilers', 'Advanced Operating Systems', 'Programmable Networking', 'Mobile Computing',
              'Software Development Using Open-Source', 'Multimedia Computing & Applications',
              'Systems Analysis, Design & Requirements Engineering']).
electives(6, ['Linear Optimization', 'Advanced Linear Algebra', 'Calculus in R^N', 'Scientific Computing',
              'Complex Analysis', 'Algebraic Number Theory', 'Finite & Spectral Element Methods',
              'Categorical Data Analysis']).
electives(7, ['Computational Gastronomy', 'Algorithms in Bioinformatics', 'Foundations of Modern Biology',
              'Biomedical Image Processing', 'Introduction to Mathematical Biology', 'Biophysics',
              'Data Science for Genomics', 'Systems and Synthetic Biology']).
electives(8, ['Memory Testing and Design', 'Digital Image Processing', 'Wireless System Implementation',
              'Statistical Signal Processing', 'Digital VLSI Design', 'Computer Architecture', 
              'Introduction to Nanoelectronics', 'Control Theory', 'Robotics', 'Autonomous Driving']).
electives(9, ['Design of Interactive Systems', 'Human Centred AI', 'Introduction To Motion Graphics',
              'Introduction To Animation And Graphics', 'Game Design & Development', 'Introduction To 3D Animation',
              'Fundamentals Of Audio For Engineers', 'Advanced Topics In Human Centered Computing']).
electives(10, ['Game Theory', 'Foundations Of Finance', 'Industrial Organization', 'Ethics in AI',
               'Learning and Memory', 'Social Psychology', 'Entrepreneurial Kichadi', 'Philosophy of Mind',
               'Intersectionality Studies', 'Advanced Ethnographic Research Methods']).
electives(11, ['BTech. Project', 'Independent Project', 'Independent Study']). %allocate only when GPA>8 and credits are correctly managed by the student.


improvement(X) :- grade(X, G), G<7.
done(X) :- not(improvement(X)).


clear_db() :-
    retractall(inadequate(_)),
    retractall(queried(_)),
    retractall(type(_,_)),
    retractall(priority(_)),
    retractall(grade(_,_)).

%cut used here
create_list(L) :- read(X), create_list(X, L).
create_list(-1, []) :- !.
create_list(X, [X|L]) :- read(NextX), create_list(NextX, L).


get_suggestions() :- \+type(_, _), !.
get_suggestions() :- 
    type(Type, Course),
    (improvement(Course) -> 
        Colour = 'yellow', ansi_format([fg(Colour)], '~w   |   ~w, ~w~n', [Course, Type, 'Available for Improvement']);
        colourmap(Type, Colour), ansi_format([fg(Colour)], '~w   |   ~w~n', [Course, Type])),
    retractall(type(Type, Course)).


inadequacy() :-
    nl,
    (inadequate('core') -> 
        ansi_format([fg('red')], '~n~w ~w', ['I noticed that you are behind on your core credits.',
        'Take care to balance your workload so that you complete the graduation requirements.']); 
        \+inadequate('core')),
    (inadequate('specialization') -> 
        ansi_format([fg('red')], '~n~w~w', ['I noticed that you are behind on your specialization credits.',
        'I have added some courses in your suggestions to help you achieve these.']); 
        \+inadequate('specialization')).


classify_courses([], _).
classify_courses([Course|CourseList], Type) :-  
    (\+(queried(Course)) -> 
    assert(queried(Course)), format('~w ~w ~w', ['Have you done', Course, '? (y/n) ']), 
    read(CourseDone), (CourseDone = 'y' -> 
        write('What was your grade? '), read(Grade), assert(grade(Course, Grade)), (done(Course) -> queried(Course); assert(type(Type, Course))); 
        assert(type(Type, Course))); queried(Course)),
    classify_courses(CourseList, Type).



recommend_all_courses(Semester, CGPA, Stream, CoreCredits, SpecCredits, []) :-
    Semester=<8, SemestersRemaining is 9-Semester,
    %check the number of X credits remaining.
    (Stream > 2 ->
        (((12-SpecCredits)/SemestersRemaining >= 6, SpecCredits<12) -> 
            assert(inadequate('specialization')); nl), %inadequate, 
        (((12-CoreCredits)/SemestersRemaining >= 6, CoreCredits<12) -> 
            assert(inadequate('core')); nl), %adequatde. here not init
        ((inadequate('specialization')) -> 
            related(Stream, X), electives(X, Elec), classify_courses(Elec, 'Suggested Specialization Elective'); 
            (CGPA>=8 ->  
                electives(11, Elec), classify_courses(Elec, 'Research')); nl);
        (((32-CoreCredits)/SemestersRemaining >= 12, CoreCredits<32) -> 
            assert(inadequate('core')); 
            (CGPA>=8 ->  
                electives(11, Elec), classify_courses(Elec, 'Research')); nl)),
    mandatory(Stream, CoreCourses), classify_courses(CoreCourses, 'Department Mandatory').


recommend_all_courses(Semester, CGPA, Stream, CoreCredits, SpecCredits, [Interest|InterestList]) :-
    electives(Interest, ElecCourses),
    classify_courses(ElecCourses, 'Elective per Interest'),
    recommend_all_courses(Semester, CGPA, Stream, CoreCredits, SpecCredits, InterestList).


start() :- 
    clear_db(), nl,
    assert(priority(1)),
    ansi_format([bold,fg(blue)], '~w', ['-- ELECTIVES ADVISORY SYSTEM FOR 3RD & 4TH YEAR IIITD UNDERGRADUATES --']),nl,nl,

    ansi_format([fg(magenta)], '~w', ['Hi! Please enter your information.']), nl,
    write("Name: "), read(Name),

    write('Current semester of study (5 to 8): '), read(Semester),  %assume rising __ semesterer
    ((5=<Semester, Semester=<8) -> 
        assert(semester(Semester)); 
        ansi_format([fg(red)], '~w', ['You may use the system but the suggestions might not include core courses.']), assert(semester(5)), nl),

    write('Enter the code corresponding to your branch: '), nl,
    format('~w~n~w~n~w~n~w~n~w~n~w~n~w', ['1. CSE', '2. ECE', '3. CSAM', '4. CSD', '5. CSAI', '6. CSB', '7. CSSS']), 
    nl, read(Stream), assert(stream(Stream)),
    write('Enter your CGPA so far: '), read(CGPA),

    write('Enter number of core level 3XX+ credits done since 3rd year: '), read(CoreCredits),
    (Stream > 2 -> 
        write('Enter number of specialization credits done since 3rd year: '), 
        read(SpecCredits); nl),

    ansi_format([fg(magenta)], '~n~w ~w. ~w', ['Great!', Name, 'Now, let me know your interests.']), nl,

    write('Enter all the codes corresponding to your interests, enter -1 when done: '), nl,
    format('~w~n~w~n~w~n~w~n~w~n~w~n~w~n~w~n~w~n~w', 
        ['1. AI and ML', '2. Security and Cryptography', '3. Algorithms', '4. Theoretical Computer Science', '5. Systems and Software Development', 
        '6. Pure Mathematics', '7. Computational Biology', '8. Hardware and Electronics', '9. Design', '10. Humanities and Social Sciences']), nl,
    create_list(InterestList),

    ansi_format([fg(magenta)], '~n~n~w~n', ['Let\'s narrow down your options.']),
    recommend_all_courses(Semester, CGPA, Stream, CoreCredits, SpecCredits, InterestList),
    nl,nl,inadequacy,
    ansi_format([fg(magenta)], '~n~n~w', ['Your course suggestions are ready, type get_suggestions.']), nl.