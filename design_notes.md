Order of operations

(), []
!
^
*, /
+, -



14 + -5
-5 + 14
-5(14)
(14)-5
(-5)+14


Affordances I'm trying to provide

negative numbers
factorials
exponents
multiple bracket characters
whitespace flexible
implied multiplication



    Accommodate negative groups by changing [+-*/]-\( to (0-1)*(

'1+1',                       2
'1 + 1',                     2
' 1 + 1 ',                   2
'   1+ 1',                   2
'1+2',                       3
'1 + 2',                     3
 '1+2',                      3
'1+-2',                      -1
'-1+2',                      1
'1*2',                       2
'1/2',                       0.5
'1/-2',                      -0.5
'(1+2)+3',                   6
'1 + (2+3)',                 6
'(1+2)3',                    9
'3*(1+2)',                   9
'3(1+2)',                    9
'(3)(1+2)',                  9
'14 + -5',                   9
'-5 + 14',                   9
'-5(14)',                    -70
'(14)-5',                    9
'(-5)+14',                   9
'-(5+4)/[(4/4)+3]*-(9)10.0',  202.5
'(52000/12+100)+-40',        4393.33333333
'4 + 5 - 3 * 2 / 4!',        8.75
'-5+-31*(-6/-2)',            -98


0   1   2   (   4   5   )



    [[<built-in function add>, [[<built-in function add>, [<built-in function div>, 52000.0, 12.0], 100.0]], []], [<built-in function sub>, 0.0, 40.0], ')']

    [[<built-in function div>,
        [<built-in function mul>, 
            [[<built-in function sub>, 0.0, 1.0]], 
            [[<built-in function add>, 5.0, 4.0]]], 
        [<built-in function mul>, 
            [<built-in function mul>, 
                [<built-in function mul>, 
                    [[<built-in function add>, 
                        [[<built-in function div>, 4.0, 4.0]],
                        3.0]], 
                    [[<built-in function sub>, 0.0, 1.0]]], 
                [9.0]], 
            10.0]]]