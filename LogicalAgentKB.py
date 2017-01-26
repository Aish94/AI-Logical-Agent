class row():
	def __init__(self):
		self.pos_facts = []
		self.pos_stmts = []
		self.neg_facts = []
		self.neg_stmts = []
	def add_positive_fact(self,node):
		self.pos_facts.append(node)
	def add_positive_stmt(self,node):
		self.pos_stmts.append(node)
	def add_negative_fact(self,node):
		self.neg_facts.append(node)
	def add_negative_stmt(self,node):
		self.neg_stmts.append(node)

def standardize(node, expr_no):
	args = node.variables
	for key,arg in args.iteritems():
		node.variables[key] = arg + str(expr_no)

def add_to_kb(table, literal, node):
	if(literal.value[0] == '~'):
		predicate = literal.value[1:].split('(',1)[0]
	else:
		predicate = literal.value.split('(',1)[0]

	if predicate not in table:
		table[predicate] = row()
	if(literal.value[0] != '~'):
		if(len(literal.variables) == 0): #fact
			if(node not in table[predicate].pos_facts):
				table[predicate].add_positive_fact(node)
		else:
			if(node not in table[predicate].pos_stmts):
				table[predicate].add_positive_stmt(node)
	else:
		if(len(literal.variables) == 0): #fact
			if(node not in table[predicate].neg_facts):
				table[predicate].add_negative_fact(node)
		else:
			if(node not in table[predicate].neg_stmts):
				table[predicate].add_negative_stmt(node)

def add_clauses_to_kb(table, node, expr_no):
	if(node.value == "&"):
		e = expr_no
		for child in node.children:
			add_clauses_to_kb(table, child, e)
			e += 1
			print("and",e)
		expr_no = e
	elif(node.value == "V"):
		for child in node.children:
			standardize(child, expr_no)
			add_to_kb(table, child, node)
		expr_no += 1
		print("or",expr_no)
	else:
		standardize(node, expr_no)
		add_to_kb(table, node, node)
		expr_no += 1
		print("else",expr_no)
	return expr_no


def print_kb(table):
	for key in table.keys():
		print("Key: "+key)
		print("Positive Facts:")
		for exp in table[key].pos_facts:
			if(exp.value == "V"):
				for child in exp.children:
					print(child.value,child.constants,child.variables),
				print
			else:
				print(exp.value,exp.constants,exp.variables)
		print("Positive Statements:")
		for exp in table[key].pos_stmts:
			if(exp.value == "V"):
				for child in exp.children:
					print(child.value,child.constants,child.variables),
				print
			else:
				print(exp.value,exp.constants,exp.variables)
		print("Negative Facts:")
		for exp in table[key].neg_facts:
			if(exp.value == "V"):
				for child in exp.children:
					print(child.value,child.constants,child.variables),
				print
			else:
				print(exp.value,exp.constants,exp.variables)
		print("Negative Statements:")
		for exp in table[key].neg_stmts:
			if(exp.value == "V"):
				for child in exp.children:
					print(child.value,child.constants,child.variables),
				print
			else:
				print(exp.value,exp.constants,exp.variables)
		print("**************************")

#result should be a tree with a sinle pos/neg predicate
#or multiple pos/neg predicates rooted at or
#or multiple pos/neg predicates rooted at or and these multiple ors rooted at and
#or multiple pos/neg predicates rooted at and

