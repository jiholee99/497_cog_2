# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *


class PizzaBuilder_DM(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    DM_module = HDM(retrieval, finst_size=22, finst_time=100.0)
    my_pizza = []

    def cook_pizza(self, pizza_ingred):
        '''
        Takes in list of "ingrediants" and outputs a "pizza"
        Inputs: pizza_ingred [list of strings]
        Output: cooked_pizza [string]
        '''
        # Whats going on here? - https://docs.python.org/3/library/stdtypes.html#str.join
        return ("_".join(pizza_ingred))

    def init():
        # Add memory chunks to declarative memory module
        # (More chunks needed in DM!)
        print("Init")
        DM_module.add("prev:crust next:marinara")
        DM_module.add("prev:marinara next:mozzarella")
        DM_module.add("prev:mozzarella next:pepperoni")
        DM_module.add("prev:pepperoni next:onion")
        DM_module.add("prev:crust next:bbq")
        DM_module.add("prev:bbq next:cheddar")
        DM_module.add("prev:cheddar next:bacon")
        DM_module.add("prev:bacon next:onion")
        goal.set(f"build_pizza ingredient:crust request:{True}")

    # Set goal so that we can prep ingredients

    def request_next_ingredient(goal=f"build_pizza ingredient:?ingredient request:{True}"):
        print(f"Requesting next ingridient : {ingredient}")
        DM_module.request(f"prev:{ingredient} next:?")
        goal.set(f"build_pizza ingredient:?ingredient request:{False}")

    def place_ingredient(goal=f"build_pizza ingredient:?ingredient request:{False}", retrieval="prev:?prev next:?next"):
        print(f"placing ingredient : ingredient={ingredient}, prev={prev}, next={next}")
        my_pizza.append(next)
        goal.set(f"build_pizza ingredient:{next} request:{True}")

    def cook_pizza_step(goal="build_pizza ingredient:onion"):
        my_pizza = self.cook_pizza(my_pizza)
        print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
        self.stop()


class EmptyEnvironment(python_actr.Model):
    pass


env_name = EmptyEnvironment()
agent_name = PizzaBuilder_DM()
env_name.agent = agent_name
python_actr.log_everything(env_name)
env_name.run()
