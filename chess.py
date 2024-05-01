from textx import metamodel_from_file
chess_mm = metamodel_from_file('chess.tx')
chess_model = chess_mm.model_from_file('sample2.chess')


def varmap(targetVar, state):
    # Checking if target variable is in the dictionary
    if targetVar in state:
        # Returning corresponding value
        return state[targetVar]
    else:
        raise ValueError("Error: Variable not found")

class Chess:

    def __init__(self):
        self.state = dict()

    def interpret(self, model):
        # model is an instance of Program
        end = False
        for statement in model.statements:
            if statement.__class__.__name__ == "Stop" or end == True:
                end = True
                break
            elif statement.__class__.__name__ == "IfEqual" or statement.__class__.__name__ == "IfNotEqual":
                self.interpretIf(statement)
            elif statement.__class__.__name__ == "IfElse":
                self.interpretIfElse(statement, model)
            elif statement.__class__.__name__ == "ElseIf":
                self.interpretElseIf(statement, model)
            elif statement.__class__.__name__ == "While" or statement.__class__.__name__ == "WhileNot":
                self.interpretWhile(statement)
            else:
                self.interpretLine(statement) 

    def interpretIf(self, s):
        var1 = s.var1.replace('B', '')
        if s.__class__.__name__ == "IfEqual":
            if self.state[var1] == self.state[s.var2]:
                self.interpret(s.newProgram)
        elif s.__class__.__name__ == "IfNotEqual":
            var2 = s.var2.replace('N', '')
            if self.state[var1] != self.state[var2]:
                self.interpret(s.newProgram)

    def interpretIfElse(self, s, m):
        previousStatement=self.Analyze(m, s)
        if previousStatement == False:
            self.interpret(s.newProgram)

    def interpretElseIf(self, s, m):
        previousStatement=self.Analyze(m, s)
        if previousStatement == False:
            var1 = s.var1.replace('R', '')
            if self.state[var1] == self.state[s.var2]:
                self.interpret(s.newProgram)

    def Analyze(self, model, statement):
            move = statement.moveNum
            for s in model.statements:
                if s.moveNum == move - 1:
                    prevStatement = s
                    break
            var1 = prevStatement.var1.replace('B', '')
            if s.__class__.__name__ == "IfEqual":
                if self.state[var1] == self.state[prevStatement.var2]:
                    return True
                else:
                    return False
            if s.__class__.__name__ == "IfNotEqual":
                var2 = prevStatement.var2.replace('N', '')
                if self.state[var1] != self.state[var2]:
                    return True
                else:
                    return False 
            if s.__class__.__name__ == "ElseIf":
                var1 = prevStatement.var1.replace('R', '')
                if self.state[var1] == self.state[prevStatement.var2]:
                    return True
                else:
                    return False 
                              
    def interpretWhile(self, s):
        var1 = s.var1.replace('K', '')
        if s.__class__.__name__ == "While":
            while self.state[var1] != self.state[s.var2]:
                self.interpret(s.newProgram)
        if s.__class__.__name__ == "WhileNot":
            var2 = s.var2.replace('N', '')
            while self.state[var1] != self.state[var2]:
                self.interpret(s.newProgram)

    def interpretLine(self, c):
            if c.__class__.__name__ == "Assignment":
                try:
                    self.state[c.var1] = varmap(c.var2, self.state)
                except:
                    var, val = list(c.var2) 
                    self.state[c.var1] = val
            elif c.__class__.__name__ == "Print":
                try:
                    print(varmap(c.var1, self.state))
                except:
                    print("Variable not found.")
            # Modified for the sake of showing FizzBuzz, not final product
            elif c.__class__.__name__ == "PrintLetter":
                l, n = list(c.var1)
                if l == 'a':
                    print ("FizzBuzz")
                elif l == 'f':
                    print("Fizz")
                elif l == 'b':
                    print("Buzz")
            elif c.__class__.__name__ == "Add":
                op1, op2 = c.var1.split('x')
                try:
                    result = int(self.state[op1]) + int(self.state[op2])
                    self.state[c.var2] = result
                except:
                    print("One or more variables undefined.")
            elif c.__class__.__name__ == "Subtract":
                op1, op2 = c.var1.split('x')
                op3 = op1.replace('B', '')
                try:
                    result = int(self.state[op3]) - int(self.state[op2])
                    self.state[c.var2] = result
                except:
                    print("One or more variables undefined.")
            elif c.__class__.__name__ == "Divide":
                op1, op2 = c.var1.split('x')
                op3 = op1.replace('N', '')
                try:
                    result = int(self.state[op3]) / int(self.state[op2])
                    self.state[c.var2] = result
                except:
                    print("One or more variables undefined.")
            elif c.__class__.__name__ == "Multiply":
                op1, op2 = c.var1.split('x')
                op3 = op1.replace('R', '')
                try:
                    result = int(self.state[op3]) * int(self.state[op2])
                    self.state[c.var2] = result
                except:
                    print("One or more variables undefined.")
            elif c.__class__.__name__ == "Mod":
                op1, op2 = c.var1.split('x')
                op3 = op1.replace('K', '')
                try:
                    result = int(self.state[op3]) % int(self.state[op2])
                    self.state[c.var2] = result
                except:
                    print("One or more variables undefined.")
            else:
                None


chess = Chess()
chess.interpret(chess_model)
