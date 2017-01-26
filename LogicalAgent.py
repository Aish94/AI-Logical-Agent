from LogicalAgentLex import lexical_analyzer
from LogicalAgentLex import build_lexer
from LogicalAgentYacc import parse
from LogicalAgentYacc import build_parser
from LogicalAgentKB import add_clauses_to_kb
from LogicalAgentKB import print_kb
import copy

class Predicate:
	def __init__(self,node):
		self.value = node.value
		self.constants = copy.deepcopy(node.constants)
		self.variables = copy.deepcopy(node.variables)

def constant(arg):
	if(arg[0].isupper()):
		return True
	return False

def printExpression(expr):
	if(expr.value == "V"):
		for child in expr.children:
			printExpression(child)
			print("V"),
		print
	else:
		print(expr.value+"("),
		no_of_args = len(expr.constants) + len(expr.variables)
		for arg_no in range(0,no_of_args):
			if arg_no in expr.constants:
				print(expr.constants[arg_no]+","),
			else:
				print(expr.variables[arg_no]+","),
		print(")"),

def unify(expr1,expr2,sub):
	no_of_args = len(expr1.constants) + len(expr1.variables)

	for arg_no in range(0,no_of_args):
		print("Argument No. : ",arg_no)
		if ((arg_no in expr1.constants) and (arg_no in expr2.constants)): #Both constant
			if(expr1.constants[arg_no] != expr2.constants[arg_no]):	#check if constants are equal
				print("Not possible to unify")
				return False
			continue #if constants are equal move to next argument
		if(arg_no in expr1.constants):
			if(expr2.variables[arg_no] in sub):
				if(sub[expr2.variables[arg_no]] != expr1.constants[arg_no]):
					return False
			sub[expr2.variables[arg_no]] = expr1.constants[arg_no]
		elif(arg_no in expr2.constants):
			if(expr1.variables[arg_no] in sub):
				if(sub[expr1.variables[arg_no]] != expr2.constants[arg_no]):
					return False
			sub[expr1.variables[arg_no]] = expr2.constants[arg_no]
		else:
			if(expr2.variables[arg_no] in sub):
				if(sub[expr2.variables[arg_no]] != expr1.constants[arg_no]):
					return False
			sub[expr2.variables[arg_no]] = expr1.variables[arg_no]
	return sub

def substituite(expr,sub):
	for pred_index,pred in enumerate(expr):	#for all predicates in expression 
		for arg_index in pred.variables.keys():	#for all arguments in the predicate
			arg = pred.variables[arg_index]
			if arg in sub:	#if argument has a substitution
				if constant(sub[arg]):
					expr[pred_index].constants[arg_index] = sub[arg]
					del expr[pred_index].variables[arg_index]
				else:
					expr[pred_index].variables[arg_index] = sub[arg]
	return expr

def getFacts(pred):
	if(pred[0] == "~"):
		pred_name = pred[1:]
		facts = kb[pred_name].pos_facts
	else:
		facts = kb[pred].neg_facts
	return facts

def getResolventClauses(pred):
	if(pred[0] == "~"):
		pred_name = pred[1:]
		resolvent_clauses = kb[pred_name].pos_stmts
	else:
		resolvent_clauses = kb[pred].neg_stmts
	return resolvent_clauses

def getPredicates(node):
	if(node.value == "V"):	#for a disjunction
		predicates = node.children
	else:					#for a single predicate
		predicates = [node]
	return predicates

def removeDuplicates(expr):
	for term in expr:
		flag = 0
		for check_term in expr[expr.index(term)+1:]:
			if(equalTerms(term,check_term)):
				del expr[expr.index(term)]
				break
			if(complimentaryTerms(term,check_term)):
				del expr[expr.index(term)]
				del expr[expr.index(check_term)]
				break
	'''seen = []
	index = 0
	for term in expr:
		flag = 0
		for seen_expr in seen:
			if(compareTerms(term,seen_expr)):
				del expr[expr.index(term)]
				flag = 1
				break
		if flag == 0:
			seen.append(term)'''

def resolve(expr1,expr2,term1,term2,sub):
	print ("Resolving ")
	expr = []
	# Add all terms from both expressions except the resolved ones
	for term in expr2:
		if term != term2:
			expr.append(Predicate(term))

	for term in expr1:
		if(term != term1):
			expr.append(Predicate(term))

	#perform substuition
	expr = substituite(expr, sub)
	removeDuplicates(expr)
	print("Resultant expression: ")
	for term in expr:
		printExpression(term)
	
	return expr

def equalTerms(term1, term2):
	if(term1.value != term2.value):
		return False
	if(term1.constants != term2.constants):
		return False
	if(term1.variables != term2.variables):
		return False
	return True

def complimentaryTerms(term1, term2):
	if(term1.value != negate(term2.value)):
		return False
	if(term1.constants != term2.constants):
		return False
	if(term1.variables != term2.variables):
		return False
	return True

def checkInfiniteLoop(query_terms,explored_terms):
	for query_term in query_terms:
		for explored_term in explored_terms:
			if equalTerms(query_term,explored_term):
				print("In an inifinite loop...")
				return True
	return False

def compare_variable_len(a,b):
	return len(a.variables) < len(b.variables)

def resolution(query_terms, explored_terms):
	if(not query_terms):	#if null set
		return True	

	result = checkInfiniteLoop(query_terms,explored_terms)
	if(result == True):
		return False	

	query_terms.sort(cmp = compare_variable_len)#sort by least no. of variables

	#check with each term in query if it can be resolved
	for query_term in query_terms:	#resolve each term in the predicate whose arguments were changed to constants during substitution
		print("Attempting to resolve term: ")
		printExpression(query_term)

		explored_terms.append(query_term)
		
		#Check with facts first
		facts = getFacts(query_term.value)
		for fact in facts:
			print("Fact to resolve with: ")
			printExpression(fact)
			fact_preds = getPredicates(fact)
			for fact_pred in fact_preds:
				if fact_pred.value == negate(query_term.value):
					sub = {}
					sub = unify(query_term,fact_pred,sub)
					if(sub == False):
						continue	#if it's not possible to unify these predicates try the next one
					print("Unified: ", sub)
					result = resolution(resolve(query_terms,fact_preds,query_term,fact_pred,sub),explored_terms[:])	#No need to unify
					if(result == True):
						return True
			print("Not resolvable")

		#If can't unify with facts check with stmts
		resolvent_clauses = getResolventClauses(query_term.value)
		for resolvent_clause in resolvent_clauses:	#loop through sentences (+ve/-ve list)
			print("Expression to resolve with : ")
			printExpression(resolvent_clause)
			#get all the predicates of the chosen clause
			resolvent_clause_preds = getPredicates(resolvent_clause)
			for resolvent_clause_pred in resolvent_clause_preds:
				if resolvent_clause_pred.value == negate(query_term.value):
					#check if it possible to unify
					sub = {}
					print("Checking if it's possible to unify resolvent terms")
					sub = unify(query_term,resolvent_clause_pred,sub)
					if(sub == False):
						continue	#if it's not possible to unify these predicates try the next one
					print("Unified: ", sub)
					#remove the resolved predicates
					#unify rest of the expression with the substiuition provided only (Don't add to this substiuition)
					#Join both expressions into one disjunction
					#continue resolution
					result = resolution(resolve(query_terms,resolvent_clause_preds,query_term,resolvent_clause_pred,sub),explored_terms[:])
					if(result == True):
						return True
			print("Not resolvable")
		return False
	return False #if none of the query terms can be resolved

def removeWhiteSpaces(str):
	str = str.replace(" ", "")
	str = str.replace("\t", "")
	return str

def negate(string):
	if(string[0] == "~"):
		string = string[1:]
	else:
		string = "~"+string
	return string

def entails(query,expr_no):
	global kb,lexer,parser
	#negate query
	query = negate(query)
	print("Negated Query: "+query)
	old_kb = copy.deepcopy(kb)

	#Add query to KB
	lexical_analyzer(query,lexer)
	query_node = parse(query,parser)
	expr_no = add_clauses_to_kb(kb,query_node,expr_no)

	#check if it is entailed
	query_terms = [query_node]
	explored_terms = []
	result = resolution(query_terms, explored_terms)	

	#remove query from KB
	kb = old_kb	#start with original KB for next query
	return result

#get input
with open("input.txt") as f:
    content = f.read().splitlines()

no_of_queries = int(content[0])
no_of_sentences = int(content[no_of_queries+1])
kb = {}

lexer = build_lexer()
parser = build_parser()
print("Sentences: ",no_of_sentences)
expr_no = 0 #to standardize variables
for i in range(no_of_queries+2,len(content)):
	sent = removeWhiteSpaces(content[i])
	lexical_analyzer(sent,lexer)
	result = parse(sent, parser)
	expr_no = add_clauses_to_kb(kb, result,expr_no)

print("Knowledge Base:")
print_kb(kb)

result = []
print("Queries: ",no_of_queries)
f = open('output.txt', 'w')
for i in range(no_of_queries):
	query = removeWhiteSpaces(content[i + 1])
	print("Query: "+query)
	if(entails(query,expr_no)):
		result.append("TRUE")
	else:
		result.append("FALSE")
	print("**********************")
f.write("\n".join(result))
