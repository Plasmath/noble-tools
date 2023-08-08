#!/usr/bin/env wolframscript

Off[General::stop]

precision = 20 (* Desired numerical precision of solutions. *)

Print["Importing..."]

cubicsdata = Import["output/cubics.txt", "Table"]

Print["Converting..."]

cubics = {}
For[i = 1, i < Length[cubicsdata]+1, i++,
	AppendTo[cubics, ToExpression[ cubicsdata[[i]][[2]] ] ] ]

startval = Input["Input index to start at (0 if from beginning): "]
endval = Length[cubics] - 1

Print["Solving..."]

solves = {}
For[i = startval, i <= endval, i++,
	
	If[ Mod[i, 250] == 0, Print["Completed cubic"+i] ];
	
	poly1 = cubics[[ i+1 ]];

	solutions = Check[ NSolve[poly1 == 0, a, PositiveReals, precision],
				i >>> output/errors.txt]; (* add to errors.txt if an error is encountered *)

	If[ Length[solutions] > 0,
		AppendTo[solves, a/.solutions],
		AppendTo[solves, {}] ]
	]

Export["output/solutions.txt", solves]

Print["Finished"]

Pause[6]