import ply.yacc as yacc
import itertools
# Get the token map from the lexer.
from LogicalAgentLex import tokens

def constant(arg):
	if(arg[0].isupper()):
		return True
	return False

class Node:
    def __init__(self,type,value,children):
         self.value = value
         self.type = type
         if type == "Operator":
         	self.children = children
         else:
         	self.constants = {}
         	self.variables = {}
         	for arg_no,arg in enumerate(children):
         		if(constant(arg)):
         			self.constants[arg_no] = arg
         		else:
         			self.variables[arg_no] = arg
              

def print_node(obj):
	print("Type")
	print(obj.type)
	print("Value")
	print(obj.value)
	if(obj.type == "Predicate"):
		print("Arguments")
		print("Constants")
		for key, value in obj.constants.iteritems() :
			print key, value
		print("Variables")
		for key, value in obj.variables.iteritems() :
			print key, value
	else:
		print("Children")
		print(len(obj.children))

def tree_traversal(root):
	level = 1
	queue = []
	root.level = level
	root.parent = None
	queue.append(root)
	for node in queue:
		print("Level: "+str(node.level))
		print_node(node)
		if(node.type == "Operator"):
			for child in node.children:
				child.level = node.level + 1
				child.parent = node.value
				queue.append(child)
		print("***********************")
'''
def Distribute(and_children,other_children):
	children = []
	for and_child in and_children:
		subchildren = []
		subchildren.append(and_child)
		subchildren.extend(other_children)
		new_node = Node("Operator","V",subchildren)
		children.append(new_node)
	return Node("Operator","&",children)

def Distribution(operator,left_operand,right_operand):
	if((left_operand.value == "&") and (right_operand.value == "&")):
		children = []
		for and1_child in left_operand.children:
			for and2_child in right_operand.children:
				subchildren = []
				subchildren.append(and1_child)
				subchildren.append(and2_child)
				new_node = Node("Operator","V",subchildren)
				children.append(new_node)
		return Node("Operator","&",children)

	other_children = []
	if(left_operand.value == "&"):
		if(right_operand.type == "Operator"):
			other_children = right_operand.children
		else:
			other_children.append(right_operand)
		return Distribute(left_operand.children,other_children)

	if(right_operand.value == "&"):
		if(left_operand.type == "Operator"):
			other_children = left_operand.children
		else:
			other_children.append(left_operand)
		return Distribute(right_operand.children,other_children)

def getNode(operator,left_operand,right_operand):
	children = []
	if(left_operand.type == "Predicate"):
		children.append(left_operand)
	if(right_operand.type == "Predicate"):
		children.append(right_operand)

	if(left_operand.value == operator):
		children.extend(left_operand.children)
	if(right_operand.value == operator):
		children.extend(right_operand.children)
			

	if(operator == "V"):
		if(left_operand.value == "&"):
			return Distribution(operator,left_operand,right_operand)
		elif(right_operand.value == "&"):
			return Distribution(operator,left_operand,right_operand)

	if(operator == "&"):
		if(left_operand.value == "V"):
			children.append(left_operand)
		if(right_operand.value == "V"):
			children.append(right_operand)

	return Node("Operator",operator,children)
'''

def X(root):
	and_children = []
	other_children = []
	final_children = []
	for child in root.children:
		if(child.value == "&"):
			and_children.append(child.children)
		elif(child.value == "V"):
			other_children.extend(child.children)
		else:
			other_children.append(child)
	children = list(itertools.product(*and_children))
	for child in children:
		child_x = []
		child_x.extend(child)
		child_x.extend(other_children)
		new_node = Node("Operator","V",child_x)
		final_children.append(new_node)
	return Node("Operator","&",final_children)

def checkDistribute(node):
	if((node.value == "V") and (any(x.value == "&" for x in node.children))):
		return X(node)
	else:
		return node

def negate(node):
	if(node.type == "Predicate"):
		if(node.value[0] == "~"):
			node.value = node.value[1:len(node.value)]
		else:
			node.value = "~"+node.value
		return node

	else:
		if(node.value == "V"):
			node.value = "&"
		elif(node.value == "&"):
			node.value = "V"
		for child in node.children:
			negate(child)
		return checkDistribute(node)

#Or Operator
#******************
def distribute(left_operand,right_operand,left_children,right_children):
	#Or operator
	children = []
	if((left_operand == "&") and (right_operand == "&")):
		for left_child in left_children:
			for right_child in right_children:
				new_or_node = Node("Operator","V",[left_child,right_child]);
				children.append(new_or_node)
		return Node("Operator","&",children)
	elif(left_operand == "&"): #right operand can be V or a predicate
		for left_child in left_children:
			new_or_node = Node("Operator","V",right_children + [left_child]);
			children.append(new_or_node)
		return Node("Operator","&",children)
	elif(right_operand == "&"): #left operand can be V or a predicate
		for right_child in right_children:
			new_or_node = Node("Operator","V",left_children + [right_child]);
			children.append(new_or_node)
		return Node("Operator","&",children)
	else:
		return Node("Operator","V",left_children + right_children)

def orOperator(left_operand,right_operand):
	left_children = []
	right_children = []

	if(left_operand.type == "Operator"):
		left_children.extend(left_operand.children)
	else:
		left_children.append(left_operand)

	if(right_operand.type == "Operator"):
		right_children.extend(right_operand.children)
	else:
		right_children.append(right_operand)

	return distribute(left_operand.value,right_operand.value,left_children,right_children)
#************************

#and operation***************
def andOperator(left_operand,right_operand):
	children = []
	if(left_operand.value == "&"):
		children.extend(left_operand.children)
	else:
		children.append(left_operand)
	if(right_operand.value == "&"):
		children.extend(right_operand.children)
	else:
		children.append(right_operand)

	return Node("Operator","&",children)
#*****************************

precedence = (
	('left', 'IMPLIES'),
	('left', 'OR'),
	('left', 'AND'),
	('left', 'NOT'),
	('left', 'LPAREN')
)

def p_implies(p):
	'expression : expression IMPLIES expression'
	negate(p[1])
	p[0] = orOperator(p[1],p[3])

def p_and(p):
	'expression : expression AND expression'
	p[0] = andOperator(p[1],p[3])

def p_or(p):
    'expression : expression OR expression'
    p[0] = orOperator(p[1],p[3])
	
def p_paran(p):
	'expression : LPAREN expression RPAREN'
	p[0] = p[2]

def p_not(p):
	'expression : NOT expression'
	p[0] = negate(p[2])

def p_pred(p):
	'expression : CONST LPAREN args'
	p[0] = Node("Predicate",p[1],p[3])

def p_args(p):
	'args : arg COMMA args'
	p[0] = p[3]
	p[0].insert(0,p[1])

def p_arg(p):
	'args : arg RPAREN'
	p[0] = []
	p[0].append(p[1])

def p_const(p):
	'arg : CONST'
	p[0] = p[1]

def p_var(p):
	'arg : VAR'
	p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

def build_parser():
	# Build the parser
	parser = yacc.yacc()
	return parser
	
def parse(data,parser):
	# Test it out
	result = parser.parse(data)
	tree_traversal(result)
	return result

#1. Convert Implication
#2. Move negation inwards (De Morgans Law)
#3. Distribution
#4. Seperation