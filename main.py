from flask import Flask, render_template, redirect, url_for
from random import randint

app = Flask(__name__)

def readData(filename):
    content = open(filename, "r").readlines()
    content = [line.split("#$") for line in content]

    for line in content:
        vars = line[3].split("_")
        vars = [x.split(":") for x in vars]
        line[3] = vars

    return content

def addProblem():
    name        = input("name: ")
    question    = input("question: ")
    formula     = input("formula: ")

    variables = []
    newVar = input("var ('n' to end): ")
    while newVar != 'n':

        min = input("min: ")
        max = input("max: ")

        variables.append([newVar, min, max])

        newVar = input("var ('n' to end): ")

    problem = [name, question, formula, variables]
    return problem

def saveProblem(filename, problem):

    data = open(filename, "a")

    variables = ""
    for var in problem[3]:
        variables += ":".join(var) + "_"
    line = problem[0] + "#$" + problem[1] + "#$" + problem[2] + "#$" + variables + "\n"
    print("saving: " + line)
    data.write(line)

    data.close()

def genProblem(problem):

    varSetup = problem[3]
    variables = []
    for var in varSetup:
        if len(var) == 3:
            variables.append([var[0], randint(int(var[1]), int(var[2]))])

    text = problem[1]

    for var in variables:
        text = text.replace(var[0], str(var[1]))

    equation = problem[2]
    for var in variables:
        equation = equation.replace(var[0], str(var[1]))

    equation.replace(" ", "")
    answer = solve0(equation)

    return [text, answer]

def solve0(equation):
    # 5 * 4 + 20 * 6
    answer = 0
    start = 0
    sign = "+"
    end = 0
    for char in equation:
        if char == "+" or char == "-":
            if sign == "+":
                answer += solve1(equation[start:end])
            else:
                answer -= solve1(equation[start:end])

            start = end + 1

            sign = char
        end += 1

    if sign == "+":
        answer += solve1(equation[start:end])
    else:
        answer -= solve1(equation[start:end])

    return answer

def solve1(equation):
    answer = None
    start = 0
    sign = "+"
    end = 0
    for char in equation:
        if char == "*" or char == "/":
            if answer == None:
                answer = int(equation[0:end])
            else:
                if sign == "*":
                    answer = answer * int(equation[start:end])
                else:
                    answer = answer / int(equation[start:end])
            sign = char
            start = end + 1
        end += 1

    if answer == None:
        answer = int(equation[0:end])
    else:
        if sign == "*":
            answer = answer * int(equation[start:end])
        else:
            answer = answer / int(equation[start:end])

    return answer

@app.route('/', methods=["POST", "GET"])
def index():
    data = readData("data.csv")

    return render_template('index.html', data=data)

@app.route('/problem/<name>', methods=["POST", "GET"])
def p(name):
    data = readData("data.csv")

    problem = None
    for line in data:
        if line[0] == name:
            problem = line
            break

    generated = genProblem(problem)

    text = generated[0]
    answer = generated[1]

    return render_template('problem.html', name=name, text=text, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)