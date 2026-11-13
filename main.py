from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

set_website_title("Limiting Reactant Calculator")
set_site_information(
    author="Kellen Lichty",
    description="Takes in input values and calculates limiting reactant, theoretical yield, and percent yield.",
    sources="Thanks to the Drafter docs.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

#helper function section
@dataclass
class Compound:
    name: str
    mass: float
    molarmass: float
    coeff: int

@dataclass
class Reaction:
    reac1: Compound
    reac2: Compound
    prod1: Compound
    prod2: Compound

reaction1 = Reaction(Compound("Al", 124.0, 27.0, 2), Compound("Fe2O3", 601.0, 159.7, 1), Compound("Al2O3", 234.2, 102.0, 1), Compound("Fe", 1.0, 55.85, 2)) 

#helper function 1: mass to mole
def masstomole(mass: float, molarmass: float) -> float:
    """
    Purpose: Takes in a mass of element/compound/etc, and calculates the amount it equals in moles of the same element/compound using the molar mass. 
Stoich: mass (g)/1(mol (mol)/molarmass (g))=mol

    Args: mass (float) - the amount of stuff there is in grams
molarmass (float) - the amount of grams there are in 1 mol of the compound

    Returns: amountinmoles (float) - the amount of stuff there is in moles
    """
    amountinmoles = mass / molarmass
    return amountinmoles

assert_equal(masstomole(10.0, 20.0), 0.5)
assert_equal(masstomole(20.0, 10.0), 2.0)



#helper function 2: mole to mole
def moletomole(molesinput: float, coeffinput: int, coeffoutput: int) -> float:
    """
    Purpose: Takes in the amount of input material in moles, as well as the coefficients of the input and output materials. Completes a calculation to give the amount of output material in moles. 
Stoich: molesinput (mol input)/1(coeffoutput (mol output)/coeffinput (mol input)) = mol output

    Args: molesinput (float) - the amount of the input material in moles
coeffinput (int) - the coefficient of the input material from the balanced reaction
coeffoutput (int) - the coefficient of the output material from the balanced reaction

    Returns: molesoutput (float) - 
    """
    molesoutput = molesinput * coeffoutput / coeffinput
    return molesoutput

assert_equal(moletomole(10.0, 2, 4), 20.0)
assert_equal(moletomole(10.0, 4, 2), 5.0)



#helper function 3: find limiting reactant
def findlimreac(reaction: Reaction) -> Compound:
    """
    Purpose: Takes in a reaction dataclass and compares the amount of each reactant in moles (using functions mass to mole and mole to mole) to find which one produces less of product 1.

    Args: reaction (Reaction) - A Reaction dataclass which contains 4 compounds reac1/2and prod1/2

    Returns: reaction.reac1.name (str) - the name of the first reactant
reaction.reac2.name (str) - the name of the second reactant
    """
    amount1 = moletomole(masstomole(reaction.reac1.mass, reaction.reac1.molarmass), reaction.reac1.coeff, reaction.prod1.coeff)
    amount2 = moletomole(masstomole(reaction.reac2.mass, reaction.reac2.molarmass), reaction.reac2.coeff, reaction.prod1.coeff)
    if amount1 >= amount2:
        return reaction.reac2
    elif amount2 > amount1:
        return reaction.reac1

assert_equal(findlimreac(reaction1), Compound("Al", 124.0, 27.0, 2))



#helper function 4: find theoretical yield
def findtheoyield(reaction: Reaction) -> float:
    """
    moles limreac/1(moles prod1/moles limreac)(g prod1/moles prod1)
    """
    limreac = findlimreac(reaction)
    product = reaction.prod1
    theoyield = masstomole(limreac.mass, limreac.molarmass) * product.coeff / limreac.coeff * product.molarmass
    return theoyield

assert_equal(findtheoyield(reaction1), 234.2)



#helper function 5: find percent yield
def findpercentyield(reaction: Reaction) -> float:
    """
    finds the percent yield of a given reaction
    """
    theoyield = findtheoyield(reaction)
    percentyield = reaction.prod1.mass / theoyield * 100
    return percentyield

assert_equal(findpercentyield(reaction1), 99.99)


#---------------------------------------


#drafter/route section
@dataclass
class State:
    message: str
    balancedreaction: Reaction
    limreac: Compound
    theoyield: float
    percentyield: float

#default state
state0 = State("Welcome to Home Page of Limiting Reactant Calculator, choose your action below", Reaction(Compound("", 0.0, 0.0, 0), Compound("", 0.0, 0.0, 0), Compound("", 0.0, 0.0, 0), Compound("", 0.0, 0.0, 0)), None, 0.0, 0.0)



#route function 1: index
@route
def index(state: State) -> Page:
    """
    This function produces the initial home page of the website, which has 5 buttons on it. 

The input values button takes the user to the input values page, where they can input the values for one compound of the reaction. 

The calculate answers button takes the user to the calculate answers page, where they can calculate the answers for the reaction that they input. 

The view answers button takes the user to the view answers page where the identified limiting reactant, theoretical yield, and percent yield are shown in a text box. 

The process explanation button takes the user to the process explanation page where there is a text box explaining how the answers were calculated
    """    
    return Page(state, [Text(state.message), Button("Input Values", compoundinput), Button("Calculate Answers", calculateanswers), Button("View Answers", viewanswers), Button("Process Explanation", explainprocess), Button("Reset Values", reset)])



#route function 2: reset
@route
def reset(state: State) -> Page:
    state.message = state0.message
    state.balancedreaction = state0.balancedreaction
    state.limreac = state0.limreac
    state.theoyield = state0.theoyield
    state.percentyield = state0.percentyield
    return index(state)



#route function 3: home
@route
def home(state: State) -> Page:
    return index(state)



#route function 4: compoundinput
@route
def compoundinput(state: State) -> Page:
    """
    Upon clicking the input values button on the home page, the user is taken to the compound input page, where there are 4 buttons, one to input the name of the compound, one to input the mass, one to input the molar mass, and one to input the coefficient in the balanced reaction. After going through each button, the user can press the 5th home button to return to the home page and see an updated balanced reaction with one compound filled in.
    """
    page_content = []

    compounds = [
        ("Reactant 1", "reac1", "Mass (g):"),
        ("Reactant 2", "reac2", "Mass (g):"),
        ("Product 1", "prod1", "Actual Mass (g):"),
        ("Product 2", "prod2", "Mass (g):")
    ]

    for title, prefix, mass_label in compounds:
        page_content.append(Text(title))

        page_content.append(Text("Compound Name:"))
        page_content.append(TextBox(prefix + "_name"))

        page_content.append(Text(mass_label))
        page_content.append(TextBox(prefix + "_mass"))

        page_content.append(Text("Molar Mass (g/mol):"))
        page_content.append(TextBox(prefix + "_molarmass"))

        page_content.append(Text("Coefficient:"))
        page_content.append(TextBox(prefix + "_coeff"))

    page_content.append(Button("Save Reaction", savecompoundinput))
    page_content.append(Button("Return Home", home))

    return Page(state, page_content)



#route function 5: save compound input
@route
def savecompoundinput(state: State,
                      reac1_name: str, reac1_mass: float,
                      reac1_molarmass: float, reac1_coeff: int,
                      reac2_name: str, reac2_mass: float,
                      reac2_molarmass: float, reac2_coeff: int,
                      prod1_name: str, prod1_mass: float,
                      prod1_molarmass: float, prod1_coeff: int,
                      prod2_name: str, prod2_mass: float,
                      prod2_molarmass: float, prod2_coeff: int) -> Page:

    state.balancedreaction = Reaction(
        Compound(reac1_name, reac1_mass, reac1_molarmass, reac1_coeff),
        Compound(reac2_name, reac2_mass, reac2_molarmass, reac2_coeff),
        Compound(prod1_name, prod1_mass, prod1_molarmass, prod1_coeff),
        Compound(prod2_name, prod2_mass, prod2_molarmass, prod2_coeff)
    )

    return Page(state, [
        Text("Your reaction has been saved!"),
        Button("Return Home", home),
        Button("Input Values Again", compoundinput)
    ])



#route function 6: calculate answers
@route
def calculateanswers(state: State) -> Page:
    """
    Upon clicking the calculate answers button on the home page, the user is taken to the calculate answers page, where there are 2 buttons. 1 will calculate the answers, which this function does, and the other returns the user to the home page.
    """
    if state.balancedreaction.reac1.mass != 0:
        state.limreac = findlimreac(state.balancedreaction)
        state.theoyield = findtheoyield(state.balancedreaction)
        state.percentyield = findpercentyield(state.balancedreaction)
        return Page(state, [Text("Calculations done."), Button("View Answers", viewanswers), Button("Return Home", home)])
    else:
        return Page(state, [Text("Please input values first."), Button("Input Values", compoundinput), Button("Return Home", home)])


#route function 7: view answers
@route
def viewanswers(state: State) -> Page:
    """
    Upon clicking the view answers button on the home page, the user is taken to the calculate answers page, where there is a textbox displaying the answers for the specified limiting reactant, theoretical yield, and percent yield. There is also a button that returns to the home page
    """
    if state.balancedreaction.reac1.mass != 0:    
        return Page(state, [Text(f"The limiting reactant is {state.limreac.name}, the theoretical yield is {state.theoyield} g product, and the percent yield is {state.percentyield}%."), Button("Return Home", home)])
    else:
        return Page(state, [Text("Please input values first."), Button("Input Values", compoundinput), Button("Return Home", home)])




#route function 8: explain process
@route
def explainprocess(state: State) -> Page:
    """
    Upon clicking the process explanation button on the home page, the user is taken to the process explanation page, where there is a textbox that shows how the calculations were completed, and a button for returning home.
    """
    return Page(state, [Text("The way this process is completed is in 3 major steps. First, you must determine which reactant is limiting, meaning runs out first. This is done by converting the mass of each reactant to moles of reactant and then to moles of product. Whichever reactant produces less moles of product is the limiting reactant. Second, to find the theoretical yield, take the moles of product produced by the limiting reactant and convert to mass of product using molar mass. Third, to find percent yield, use the given mass of product, divide it by the theoretical yield, and multiply by 100."), Button("Return Home", home)])



start_server(state0)


