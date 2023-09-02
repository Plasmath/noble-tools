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

startval = Input["Input index to start at (1 if from beginning): "]
endval = Length[pairsdata]

Print["Solving..."]

Print[ endval "pairs." ]

solves = {}
For[i = startval, i <= endval, i++,

	If[ Mod[i, 1000] == 0, Print[i] ];

	t = pairsdata[[i]];

	poly1 = cubics[[ t[[1]]+1 ]];
	poly2 = cubics[[ t[[2]]+1 ]];
	
	reduceSolutions = Check[ Reduce[poly1 == 0 && poly2 == 0, {a,b}, PositiveReals],
				{poly1, poly2} >>> output/errors.txt
				];
	solutions = {ToRules[reduceSolutions]};
	
	(* Make solutions numeric rather than symbolic*)


	If[ Length[solutions] > 0,
		sols = {a,b} /. solutions;

		For[j = 1, j <= Length[sols], j++,
			sols[[j]] = {N[sols[[j]][[1]]],
						 N[sols[[j]][[2]]] /. a -> N[sols[[j]][[1]]]}
		];

		AppendTo[solves, sols],

		AppendTo[solves, {}] ]
	
	If[ Mod[i, 30000] == 0,  (* Export in case of crashing *)
		Export[ ToString[i] <> ".txt", solves];
		solves = {} ];
	]


Export["output/solutions.txt", solves]

Print["Finished"]

Pause[6]