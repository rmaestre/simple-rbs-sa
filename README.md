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
	5 positives terms loaded
	4 negatives terms loaded
	3 entities terms loaded
	1 inverters terms loaded
	5 chunks loaded

Loading RULES:
	Rule parsed succesfully: #1 NOT + ENTITY > -0.3 ;
	Rule parsed succesfully: #2 ENTITY NOT + > -0.3 ;
	Rule parsed succesfully: #3 NOT - ENTITY > 0.3 ;
	Rule parsed succesfully: #4 ENTITY NOT - > 0.3 ;
	Rule parsed succesfully: #5 + ENTITY > 0.3 ;
	Rule parsed succesfully: #6 ENTITY + > 0.3 ;
	Rule parsed succesfully: #7 - ENTITY > -0.3 ;
	Rule parsed succesfully: #8 ENTITY - > -0.3 ;
	Rule parsed succesfully: #9 ENTITY penoso.adj > -0.4;
	Rule parsed succesfully: #10 ENTITY competitivo.adj > 0.4;
	Rule parsed succesfully: #11 lento.adj ENTITY > -0.4;


Response:
{
	matches: {
		0: {
			rule_triggered: "#2",
			score: -0.3,
			match: "vodafone no yo.None gustar.verb"
		},
		1: {
			rule_triggered: "#6",
			score: 0.3,
			match: "movistar ser.None bueno.adj"
		},
		2: {
			rule_triggered: "#10",
			score: 0.4,
			match: "vodafone ser.None muy.adv competitivo.adj"
		}
	},
	text: "movistar ser.None bueno.adj aunque.None vodafone no yo.None gustar.verb #.None #.None vodafone ser.None muy.adv competitivo.adj ",
	raw_text: "movistar es bueno aunque vodafone no me gusta, pero vodafone es muy competitivo",
	elipsed_time: 0.10001611709594727
}

```
