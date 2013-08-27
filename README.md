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
```

A simple execution of the whole system, loading dicts and rules, parsing the rules and checking the kb.
```
host$ python sa_grammar.py 
Loading dicts:
	6 positives terms loaded
	4 negatives terms loaded
	3 entities terms loaded

Loading RULES:
	Rule parsed succesfully: #1 NOT + ENTITY > -0.3 ;
	Rule parsed succesfully: #2 ENTITY NOT + > -0.3 ;
	Rule parsed succesfully: #3 NOT - ENTITY > 0.3 ;
	Rule parsed succesfully: #4 ENTITY NOT - > 0.3 ;
	Rule parsed succesfully: #5 + ENTITY > 0.3 ;
	Rule parsed succesfully: #6 ENTITY + > 0.3 ;
	Rule parsed succesfully: #7 - ENTITY > -0.3 ;
	Rule parsed succesfully: #8 ENTITY - > -0.3 ;


Response:
{
	matches: {
		0: {
			rule_triggered: "#6",
			score: 0.3,
			match: "movistar yo.None gustar.verb"
		},
		1: {
			rule_triggered: "#8",
			score: -0.3,
			match: "orange que.None ser.None lento.adj"
		},
		2: {
			rule_triggered: "#7",
			score: -0.3,
			match: "lento.adj vodafone"
		}
	},
	text: "movistar yo.None gustar.verb bastante.adv #.None no decir.verb el.None mismo.adj para.None orange que.None ser.None lento.adj #.None lento.adj vodafone ",
	raw_text: "movistar me gusta bastante, no digo lo mismo para orange que es lento, lento vodafone",
	elipsed_time: 0.09892916679382324
}

```
