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

Analizing 6 chunks
	Chunk "movistar no funciona muy bien pero nada bien"
	Rule triggered:#2
	Score: -0.3
	Match: [('movistar', 'no', 'bien')]


	Chunk " pero vodafone es muy buena"
	Rule triggered:#6
	Score: 0.3
	Match: [('vodafone', 'buena')]


	Chunk " orange no es muy buena"
	Rule triggered:#2
	Score: -0.3
	Match: [('orange', 'no', 'buena')]


	Chunk "algunas veces vodafone no me gusta nada"
	Rule triggered:#2
	Score: -0.3
	Match: [('vodafone', 'no', 'gusta')]


	Chunk " por otro lado"


	Chunk " otras veces vodafone si me gusta"
	Rule triggered:#6
	Score: 0.3
	Match: [('vodafone', 'gusta')]
```
