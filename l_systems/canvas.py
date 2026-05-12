class ConstantMeanings:
    TURN_90_RIGHT = "Turn 90º Right"
    TURN_90_LEFT = "Turn 90º Left"
    MOVE_FORWARD = "Move Forward"
    DO_NOTHING = "Do Nothing"
    TURN_60_RIGHT = "Turn 60º Right"
    TURN_60_LEFT = "Turn 60º Left"
    START_SAVING = "Start Saving"
    STOP_SAVING = "Stop Saving"
    TURN_22_5_RIGHT = "Turn 22.5º Right"
    TURN_22_5_LEFT = "Turn 22.5º Left"
    CHANGE_COLOR_BROWN = "Change Color Brown"
    CHANGE_COLOR_GREEN = "Change Color Green"
    CHANGE_COLOR_BLUE = "Change Color Blue"
    CHANGE_COLOR_PURPLE = "Change Color Purple"

    def all():
        return set(["Turn 90º Right", "Turn 90º Left", 
                    "Move Forward", "Do Nothing", 
                    "Turn 60º Right", "Turn 60º Left", 
                    "Start Saving", "Stop Saving",
                    "Turn 22.5º Right", "Turn 22.5º Left",
                    "Change Color Brown", "Change Color Green",
                    "Change Color Blue", "Change Color Purple"])
    
    def list_all():
        return ["Turn 90º Right", "Turn 90º Left", 
                "Turn 60º Right", "Turn 60º Left", 
                "Turn 22.5º Right", "Turn 22.5º Left", 
                "Move Forward", "Do Nothing", 
                "Start Saving", "Stop Saving",
                "Change Color Brown", "Change Color Green",
                "Change Color Blue", "Change Color Purple"]
    
class Rule:
    def __init__(self, base, result):
        self.base = base
        self.string_result = result
        self.list_result = list(result)
    
    def print(self):
        print(f'{self.base} --> {self.string_result}')

    def separate(self, result_as_string):
        if result_as_string:
            return (self.base, self.string_result)
        else:
            return (self.base, self.list_result)

    def __eq__(self, other):
        return ((self.base == other.base) and (self.string_result == other.string_result))

class CanvasState:
    """Singleton class that stores the current canvas state."""
    variables = set()
    constants = set()
    variable_meanings = {}
    constant_meanings = {}
    initial = ""
    rules = []
    should_draw = True
    scale_factor = 1.0
    show_turtle = True

    def add_variable(self, new_variable, meaning):
        if not new_variable == "" and meaning in ConstantMeanings.all():
            if new_variable not in self.list_var_const():
                self.variables.add(new_variable)
            self.variable_meanings[new_variable] = meaning


    def remove_variable(self, variable):
        if variable in self.variables:
            if variable == self.initial:
                self.initial = ""
            self.variables.remove(variable)
            self.variable_meanings.pop(variable)

    def list_variables(self):
        return sorted(list(self.variables))
    
    def add_constant(self, new_constant, meaning):
        if not new_constant == "" and meaning in ConstantMeanings.all():
            if new_constant not in self.list_var_const():
                self.constants.add(new_constant)
            self.constant_meanings[new_constant] = meaning

    def remove_constant(self, constant):
        if constant in self.constants:
            self.constants.remove(constant)
            self.constant_meanings.pop(constant)

    def list_constants(self):
        return sorted(list(self.constants))
    
    def list_var_const(self):
        return sorted(list(self.constants.union(self.variables)))
    
    def remove_item(self, item):
        self.remove_variable(item)
        self.remove_constant(item)

    def add_rule(self, rule):
        base, result = rule.separate(False)
        result_valid = True
        if len(result) == 0:
            result_valid = False
        for item in result:
            if not item in self.constants and not item in self.variables:
                result_valid = False

        if rule not in self.rules and base in self.variables and result_valid:
            self.rules.append(rule)

    def remove_rule(self, rule):
        if rule in self.rules:
            self.rules.remove(rule)
    
    def rules_list(self):
        return self.rules
    
    def initial_list(self):
        return list(self.initial)