#!/usr/bin/env wolframscript

Off[General::stop]

precision = 20 (* Desired numerical precision of solutions. *)

Print["Importing..."]

cubicsdata = Import["output/cubics.txt", "Table"]

Print["Converting..."]

cubics = {}
For[i = 1, i < Length[cubicsdata]+1, i++,
	AppendTo[cubics, ToExpression[ cubicsdata[[i]][[2]] ] ] ]

startval = Input["Input index to start at (1 if from beginning): "]
endval = Length[cubics]

Print["Solving..."]

solves = {}
For[i = startval, i <= endval, i++,
	
	If[ Mod[i, 250] == 0, Print["Completed cubic"+i] ];
	
	poly1 = cubics[[ i ]];

	reduceSolutions = Check[ Reduce[poly1 == 0, a, PositiveReals],
				i >>> output/errors.txt]; (* add to errors.txt if an error is encountered *)
	solutions = {ToRules[reduceSolutions]};

	If[ Length[solutions] > 0,
		sols = a /. solutions;
		For[j = 1, j <= Length[sols], j++,
			sols[[j]] = N[sols[[j]], 25]
		];

		AppendTo[solves, sols],

		AppendTo[solves, {}] ]
	]

Export["output/solutions.txt", solves]

Print["Finished"]

Pause[6]