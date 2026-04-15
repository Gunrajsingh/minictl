#   _____  _    _   _____  _______  ____   __  __     ____   _____   ______  _____          _______  ____   _____
#  / ____|| |  | | / ____||__   __|/ __ \ |  \/  |   / __ \ |  __ \ |  ____||  __ \     /\ |__   __|/ __ \ |  __ \
# | |     | |  | || (___     | |  | |  | || \  / |  | |  | || |__) || |__   | |__) |   /  \   | |  | |  | || |__) |
# | |     | |  | | \___ \    | |  | |  | || |\/| |  | |  | ||  ___/ |  __|  |  _  /   / /\ \  | |  | |  | ||  _  /
# | |____ | |__| | ____) |   | |  | |__| || |  | |  | |__| || |     | |____ | | \ \  / ____ \ | |  | |__| || | \ \
#  \_____| \____/ |_____/    |_|   \____/ |_|  |_|   \____/ |_|     |______||_|  \_\/_/    \_\|_|   \____/ |_|  \_\
#
#
# (Before following this assignment, it is smart to look at the minictl usage guide,
# as this is an assignment for CTL model checking in general, not minictl specifically)
#
# In this assignment, we will look at defining our own custom operator,
# and providing an algorithm for it.
#
# In definition of E[ϕUψ], ϕ does not need to hold true in the state in which ψ is true,
# only in preceding states. However, it is not impossible to imagine a modality in which
# ϕ does need to hold true, even in the state in which ψ is true.
# In this assignment, you will write an implementation of a model checking algorithm for this
# custom version of E[ϕUψ].
#
# Consider the following model (it might be smart to draw it out):
 
from minictl import State, Model, CTLFormula, CTLChecker
 
s1 = State("s1", {"p"})
s2 = State("s2", set())
s3 = State("s3", {"p", "q"})
s4 = State("s4", {"q"})
s5 = State("s5", {"p", "q"})
model = Model(
    [s1, s2, s3, s4, s5],
    {
        "s1": ["s2"],
        "s2": ["s1"],
        "s3": ["s1", "s4"],
        "s4": ["s4"],
        "s5": ["s2", "s4", "s5"],
    },
)
 
checker = CTLChecker(model)
print("Standard E[pU!q]:", checker.check(CTLFormula.parse("E[pU!q]")))
 
 
from copy import copy
 
 
def new_eu(lhs: set[str], rhs: set[str], model: Model) -> set[str]:
    result = lhs & rhs  
 
    all_states = model.get_states()
    predecessors = {s.name: set() for s in all_states}
    for state in all_states:
        for succ in model.get_next(state.name):
            predecessors[succ].add(state.name)
 
    worklist = copy(result)
    while worklist:
        current = worklist.pop()
        for pred in predecessors[current]:
            if pred not in result and pred in lhs:
                result.add(pred)
                worklist.add(pred)
 
    return result
 
 
checker = CTLChecker(model)
checker.set_custom("EU", new_eu)
print("Custom  E[pU!q]:", checker.check(CTLFormula.parse("E[pU!q]")))
