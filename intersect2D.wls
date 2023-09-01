#!/usr/bin/env wolframscript

Off[General::stop]

precision = 20 (* Desired numerical precision of solutions. *)

Print["Importing..."]

cubicsdata = Import["output/cubics.txt", "Table"]
pairsdata = Import["output/pairs.txt", "Table"]

Print["Converting..."]

cubics = {}
For[i = 1, i < Length[cubicsdata]+1, i++,
	AppendTo[cubics, ToExpression[ cubicsdata[[i]][[2]] ] ] ]

startval = Input["Input index to start at (0 if from beginning): "]
endval = Length[pairsdata] - 1

Print["Solving..."]

solves = {}
For[i = startval, i <= endval, i++,
	
	If[ Mod[i, 250] == 0, Print[i] ];

	t = pairsdata[[i + 1]];

	poly1 = cubics[[ t[[1]]+1 ]];
	poly2 = cubics[[ t[[2]]+1 ]];
	
	solutions = Check[ NSolve[{poly1 == 0, poly2 == 0}, {a,b}, PositiveReals, 20],
				poly1 >>> errors.txt; poly2 >>> errors.txt
				];

	If[ Length[solutions] > 0,
		AppendTo[solves, {a,b}/.solutions],
		AppendTo[solves, {}] ]
	]
	
	If[ Mod[i, 30000] == 0, 
		Export[ ToString[i] <> ".txt", solves];
		solves = {} ];

Export["output.txt", solves]

Print["Finished"]

Pause[6]