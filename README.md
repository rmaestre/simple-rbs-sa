A simple Rule based system to a sentiment analysis
=============================

This rule based system provides a simple BNF grammar to parse sentiment analysis rules.
When match succes, no more rules are checked.

The simple BNF Grammar:
```
rule : BEGINRULE expression THEN SCORE ENDRULE
expression : QUALIFICATOR ENTITY
expression : ENTITY QUALIFICATOR
expression : SWAP QUALIFICATOR ENTITY
expression : ENTITY SWAP QUALIFICATOR
expression : ENTITY IDENTIFICATOR
expression : IDENTIFICATOR ENTITY
```

A simple execution of the whole system, loading dicts and rules, parsing the rules and checking the kb.
```
host$ python sentiment_service.py -l spanish -p 8080
Loading dicts:
	0 positives terms loaded
	0 negatives terms loaded
	3 entities terms loaded
	1 inverters terms loaded
	6 chunks loaded

Loading rules:
	Rule parsed succesfully: #1 slow.a ENTITY > -0.9;
	Rule parsed succesfully: #2 ENTITY slow.a > -0.9;
	Rule parsed succesfully: #3 amazing.a ENTITY > 0.9;
	Rule parsed succesfully: #4 ENTITY amazing.a > 0.9;
	Rule parsed succesfully: #10 NOT + ENTITY > -0.3 ;
	Rule parsed succesfully: #11 ENTITY NOT + > -0.3 ;
	Rule parsed succesfully: #12 NOT - ENTITY > 0.3 ;
	Rule parsed succesfully: #13 ENTITY NOT - > 0.3 ;
	Rule parsed succesfully: #14 + ENTITY > 0.3 ;
	Rule parsed succesfully: #15 ENTITY + > 0.3 ;
	Rule parsed succesfully: #16 - ENTITY > -0.3 ;
	Rule parsed succesfully: #17 ENTITY - > -0.3 ;


Response:
{
	matches: {
		0: {
			rule_triggered: 10,
			score: -0.3,
			match: "not love.v+0.5 movistar"
		},
		1: {
			rule_triggered: 4,
			score: 0.9,
			match: "orange an.None amazing.a"
		},
		2: {
			rule_triggered: 1,
			score: -0.9,
			match: "slow.a connection.n-0.125 of.None vodafone"
		}
	},
	text: "i.n do.v not love.v+0.5 movistar #.None orange an.None amazing.a+0.25 company.n #.None BTW.r #.None #.None #.None i.None hate.v-0.75 the.None slow.a connection.n-0.125 of.None vodafone ",
	raw_text: "i do not love movistar but orange an amazing company. BTW ... i hate the slow connection of vodafone",
	elipsed_time: 0.25530195236206055
}

```
