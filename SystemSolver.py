from tkinter import *
import os

def augmentedMatrixSolver(augmented_matrix, variables_names_array):
    for pivot_row in range(len(augmented_matrix)-1): #Pivot selected
        if augmented_matrix[pivot_row][pivot_row]==0: #If an exchange is needed
            for interchange_index in range(pivot_row, len(augmented_matrix)):
                if augmented_matrix[interchange_index][pivot_row]!=0:
                    augmented_matrix[pivot_row], augmented_matrix[interchange_index]=\
                        augmented_matrix[interchange_index], augmented_matrix[pivot_row]
                    break
        for target_row in range(pivot_row + 1, len(augmented_matrix)):
            if (augmented_matrix[target_row][pivot_row] == 0):
                continue

            pivot_multiplier = augmented_matrix[target_row][pivot_row]
            target_multiplier = augmented_matrix[pivot_row][pivot_row]

            for column_of_rows in range(len(augmented_matrix[0])):
                augmented_matrix[pivot_row][column_of_rows] *= pivot_multiplier
                augmented_matrix[target_row][column_of_rows] *= target_multiplier
                augmented_matrix[target_row][column_of_rows] -= augmented_matrix[pivot_row][column_of_rows]

    #Checking if the system has no solutions
    numbers_saw = False
    for row in range(len(augmented_matrix)-1, -1, -1):
        numbers_saw=False
        numbers_saw_counter=0
        for column_of_rows in range(len(augmented_matrix[0])-1):
            if augmented_matrix[row][column_of_rows]!=0:
                numbers_saw=True
                numbers_saw_counter+=1
        if numbers_saw==False:
            if augmented_matrix[row][-1]!=0:
                return "The system has no solutions..."
            else:
                augmented_matrix=augmented_matrix[:row]+augmented_matrix[row+1:]

    #Checking if the system has multiple solutions
    if len(augmented_matrix)!=len(variables_names_array):
        return "The system has multiple solutions..."

    #Triangular form
    result=""
    for column in range(len(augmented_matrix[0])-2, -1, -1):
        if (augmented_matrix[column][column] != 1):
            augmented_matrix[column][-1] /= augmented_matrix[column][column]
            augmented_matrix[column][column] = 1
        result+=variables_names_array[column]+" = "+str(float(augmented_matrix[column][-1]))+"\n"
        for row in range(column-1, -1, -1):
            if augmented_matrix[row][column]!=0:
                augmented_matrix[row][-1]-=augmented_matrix[row][column]*augmented_matrix[column][-1]
                augmented_matrix[row][column]=0

    return result

def dictionaryTo2dArray(variables_dictionary): #Building augmented matrix
    multidimensional_array=[[] for row in range(len(variables_dictionary["constant"]))]
    variables_array=list(variables_dictionary.keys())

    for row in range(len(variables_dictionary["constant"])):
        for variable_index in range(len(variables_array)):
            variable_name=variables_array[variable_index]
            multidimensional_array[row].append(variables_dictionary[variable_name][row])

    return multidimensional_array


def splitTheEquations(equations, variables_dictionary): #Each coefficient of each variable in each equation will be
                                                        #saved in the dictionary already prepared
    equations_array=equations.split(",")
    constants_characters=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "/", "."] #characters that a
                                                                                           #coefficient can contain
    pause_characters=["+", "-", "="] #To the left of these symbols there will always be a coefficient or a variable

    for equation_index in range(len(equations_array)): #Each equation index
        equation=equations_array[equation_index]
        equal_index=equation.find("=") #Bir denklemi parça parça ayırtmak için belirlendi.
        constant="" #The coefficients will be stored in this variable

        for positive_number in equation[0:equal_index]: #Positive side of the equation
            if positive_number in constants_characters: #If the character is a number or a pharantesis
                constant+=positive_number

            elif positive_number in pause_characters: #at this point a coefficient should already have been saved
                                                      #to a variable, or a coefficient of a constant in our variable
                                                      #may be
                if len(constant)==0: #If constant variablie is empty, the symbol belonging to the next expected
                                     #coefficient will be saved
                    constant = positive_number if positive_number != "=" else ""
                    continue

                #Having a coefficient in hand and not having seen a variable, it is known that then this coefficient
                #will be a constant
                variables_dictionary["constant"] = variables_dictionary["constant"] + [-eval(constant)]
                constant = positive_number if positive_number != "=" else ""

            elif positive_number==" ": #Insignificant character
                continue

            else: #At this point (accepting that we will be seeing a variable name),
                  #its coefficient will be saved to the dictionary
                variables_dictionary[positive_number]=variables_dictionary[positive_number]+\
                                                      [eval(constant) if constant not in ["", "+", "-"] else
                                                       (-1 if constant=="-" else 1)]
                constant=""

        if len(constant)!=0: #If a coefficient has remained, it will belong to a constant
            variables_dictionary["constant"] = variables_dictionary["constant"] +[-eval(constant)]
            constant = ""

        for negative_number in equation[equal_index+1:]: #Negative side of the equation
            if negative_number in constants_characters: #If the character is a number or a pharantesis
                constant+=negative_number

            elif negative_number in pause_characters: #at this point a coefficient should already have been saved
                                                      #to a variable, or a coefficient of a constant in our variable
                                                      #may be
                if len(constant)==0: #If constant variablie is empty, the symbol belonging to the next expected
                                     #coefficient will be saved
                    constant = negative_number if negative_number != "=" else ""
                    continue

                # Having a coefficient in hand and not having seen a variable, it is known that then this coefficient
                # will be a constant
                variables_dictionary["constant"] = variables_dictionary["constant"] + [eval(constant)]
                constant = negative_number if negative_number != "=" else ""

            elif negative_number==" ": #Insignificant character
                continue

            else:#At this point (accepting that we will be seeing a variable name),
                  #its coefficient will be saved to the dictionary
                variables_dictionary[negative_number]=variables_dictionary[negative_number]+ \
                                                                    [-eval(constant) if constant not in ["", "+", "-"]
                                                                    else (1 if constant=="-" else -1)]
                constant=""

        if len(constant)!=0: #If a coefficient has remained, it will belong to a constant
            variables_dictionary["constant"] = variables_dictionary["constant"] +[eval(constant)]

        for variable_that_did_not_appear in variables_dictionary.keys():
            if(len(variables_dictionary[variable_that_did_not_appear]))!=equation_index+1:
                variables_dictionary[variable_that_did_not_appear]=\
                    variables_dictionary[variable_that_did_not_appear]+[0]

    return dictionaryTo2dArray(variables_dictionary)

def findVariablesNamesAtAllEquations(equation):
    insignificant_expressions = [str(x) for x in range(10)]
    insignificant_expressions += ["+", " ", "(", ")", "/", "=", "-", ",", "."] #Numbers and arithmetic symbols will be
                                                                          #eliminated
    for insignificant_expression in insignificant_expressions:
        equation = equation.replace(insignificant_expression, "")

    return equation #Return only variables names in a string type

def systemSolver(equation):
    only_variables=findVariablesNamesAtAllEquations(equation)
    only_variables=list(set(only_variables))

    variables_dictionary={y:[] for y in only_variables} #Each value of each variable at each row will recorded in arrays
    variables_dictionary["constant"]=[] #Constant too

    augmented_matrix=splitTheEquations(equation, variables_dictionary)
    return augmentedMatrixSolver(augmented_matrix, list(variables_dictionary.keys())[0:-1])

def calculateInputEquation():
    equation_info=equation.get()

    try:
        r=systemSolver(equation_info)
        result_label.config(text=r)
    except:
        result_label.config(text="The system has no solutions...")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

screen=Tk()
screen.geometry("500x700")
screen.resizable(width=False, height=False)
screen.title("Solver of System of Equations Using Gaussian Elimination")

heading = Label(text = "Solver of System of Equations", fg = "black", width = "40", height = "5", font=('italic', 15))
heading.place(x = 15, y = -25)

img=PhotoImage(file=resource_path("matrix.png"))
img=img
img_label=Label(image=img).place(x=140, y=60)

warning_text="* Equations must be separated by commas (,)  \n\n" \
             "* Variables that appear in an equation can only\n" \
              "appear in it once (also with the constants) \n\n" \
              "Example:                                                      \n" \
              "         2x+2y=15, x=5 ----------> Correct       \n" \
              "        x+x+2y+1=16, x=5 -----> Incorrect    \n"
warning_label=Label(text = warning_text, font=("Arial", 8)).place(x = 265, y = 220)

equation_label = Label(text = "Input your equation:")
equation_label.place(x = 15, y = 210)

equation=StringVar()

equation_entry=Entry(textvariable = equation, width = "36")
equation_entry.place(x = 15, y = 240)

Button(screen,text = "Calculate", width = "30", height = "2", command = calculateInputEquation, bg = "grey").place(x = 15, y = 270)

result_label = Label(screen, fg="green", font=('Arial', 12))
result_label.place(x = 15, y = 340)

screen.mainloop()