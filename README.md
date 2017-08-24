# AI-Logical-Agent

An assignment done as a requirment for **CSCI 561 - Artificial Intelligence**  
A logical agent that takes in a knowledge base of statements and queries in First Order Logic and returns True/False based on if the query can be entailed by the Knowledge Base or not.

**Input File:**  
<NQ = NUMBEROFQUERIES>  
<QUERY 1>  
...  
\<QUERY NQ>  
<NS = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>  
<SENTENCE 1>  
...  
\<SENTENCE NS>  

where each query is of the form Predicate(constant) or ~Predicate(constant)

**Output File:**  
<ANSWER 1>  
...  
\<ANSWER NQ>  

where each answer is either True or False

## How it works:
First each Knowledge Base sentence is taken and tokenized using the lexer  
The statement is then parsed using yacc and converted from first order logic to a Conjunctive Normal Form Tree  
Each Statement is stored in a table of the form:  
Predicate | Positive Statements | Negative Statements

So for each predicate we can pull out the statements in which it is positive and negative.  

Finally, each query is taken and converted to it's conjunctive Normal Form Tree  
The resolution algorithm is used to check if the Knowledge Base entails the query

**Example Input:**  
6  
F(Bob)  
H(John)  
~H(Alice)  
~H(John)  
G(Bob)  
G(Alice)  
14  
A(x)=>H(x)  
D(x,y)=>~H(y)  
B(x,y)&C(x,y)=>A(x)  
B(John,Alice)  
B(John,Bob)  
(D(x,y)&F(y))=>C(x,y)  
F(Bob)  
D(John,Bob)  
F(x)=>G(x)  
G(x)=>H(x)  
H(x)=>F(x)  
R(x)=>H(x)  
R(Alice)  

**Example output:**  
TRUE  
TRUE  
TRUE  
FALSE  
FALSE  
TRUE  

Used ply for parsing: http://www.dabeaz.com/ply/
