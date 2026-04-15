#   _____  _    _  ____   __  __            _____   _____  _   _  ______
#  / ____|| |  | ||  _ \ |  \/  |    /\    |  __ \ |_   _|| \ | ||  ____|
# | (___  | |  | || |_) || \  / |   /  \   | |__) |  | |  |  \| || |__
#  \___ \ | |  | ||  _ < | |\/| |  / /\ \  |  _  /   | |  | . ` ||  __|
#  ____) || |__| || |_) || |  | | / ____ \ | | \ \  _| |_ | |\  || |____
# |_____/  \____/ |____/ |_|  |_|/_/    \_\|_|  \_\|_____||_| \_||______|
#
# State variables:
#   surface: submarine is on the surface (True) or underwater (False)
#   hatch:   hatch is open (True) or closed (False)
#   sunk:    submarine is sunk (True) or not (False)
#
# Actions: up, down, open, close
# Rules:
#   - open performed underwater -> sunk
#   - down performed with hatch open -> sunk
#   - once sunk: only self-loop (down, changes nothing)

from minictl import State, Model, CTLChecker, CTLFormula


s1 = State("s1", {"surface", "hatch", "sunk"})   
s2 = State("s2", {"surface", "hatch"})           
s3 = State("s3", {"surface", "sunk"})            
s4 = State("s4", {"surface"})                    
s5 = State("s5", {"hatch", "sunk"})              
s6 = State("s6", {"hatch"})                   
s7 = State("s7", {"sunk"})                       
s8 = State("s8", set())                         


transitions = {
    "s1": ["s1"],
    "s2": ["s2", "s1", "s4"],   # up/open->s2, down(hatch open)->sunk(s1), close->s4
    "s3": ["s3"],
    "s4": ["s4", "s8", "s2"],   # up/close->s4, down->s8, open->s2
    "s5": ["s5"],
    "s6": ["s2", "s5", "s8"],   # up->s2, down/open->sunk(s5), close->s8
    "s7": ["s7"],
    "s8": ["s4", "s8", "s7"],   # up->s4, down/close->s8, open->sunk(s7)
}

model = Model([s1, s2, s3, s4, s5, s6, s7, s8], transitions)
checker = CTLChecker(model)


def holds_in_s(formula_str):
    result = checker.check(CTLFormula.parse(formula_str))
    return "s4" in result


print("Ex 2 - AG(!sunk) true in s4?", holds_in_s("AG(!sunk)"))

print("Ex 3 - E[!sunk U (!surface and !sunk)] true in s4?", holds_in_s("E[!sunk U (!surface and !sunk)]"))

print("Ex 4.1 - AF(surface and !hatch and !sunk) in s4?", holds_in_s("AF(surface and !hatch and !sunk)"))

print("Ex 4.2 - AG(surface -> EF(!surface)) in s4?", holds_in_s("AG(surface -> EF(!surface))"))

print("Ex 4.3 - AG(!hatch -> EF(hatch)) in s4?", holds_in_s("AG(!hatch -> EF(hatch))"))

print("Ex 4.4 - EF(EG(!surface and !sunk)) in s4?", holds_in_s("EF(EG(!surface and !sunk))"))

print("Ex 4.5 - AG(sunk -> AG(sunk)) in s4?", holds_in_s("AG(sunk -> AG(sunk))"))
