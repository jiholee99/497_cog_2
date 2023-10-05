# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *


class PizzaBuilder_DM(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    DM_module = HDM(retrieval)
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
        DM_module.add("prev:none next:crust")
        DM_module.add("prev:crust next:marinara")
        DM_module.add("prev:crust next:bbq")
        DM_module.add("prev:marinara next:mozzarella")
        DM_module.add("prev:bbq next:cheddar")
        DM_module.add("prev:mozzarella next:pepperoni")
        DM_module.add("prev:cheddar next:bacon")
        goal.set("start_pizza")

    # Set goal so that we can prep ingredients

    def prep_ingredients(goal="start_pizza"):
        # start building our pizza!
        goal.set("build_pizza")
        # Request next step from DM
        DM_module.request("prev:none next:?")



    # Request next step from DM

    ###Rules to request from declarative memory for next step/ingredient and place that ingredient on your pizza and make sure you can more on to cooking pizza
    def place_crust(goal="build_pizza" ,retrieval="prev:?prev next:?next"):
        # Place the crust
        # print("Placing the curst")
        # print(f"Prev : {next}")
        my_pizza.append(next)
        goal.set("place_sauce")
        DM_module.request("prev:crust next:?")

    def place_sauce(goal="place_sauce", retrieval="prev:crust next:?next"):  # utility=0.1
        # print(f"placing the sauce... {next}")
        my_pizza.append(next)
        goal.set("place_cheese")
        prevStr = next
        DM_module.request(f"prev:{prevStr} next:?")

    def place_mozarella(goal="place_cheese", retrieval="prev:marinara next:?next" ):
        # print(f"placing the mozzarella : {next}")
        my_pizza.append(next)
        DM_module.request("prev:mozzarella next:?")
        goal.set("place_topping n:pepperoni")


    def place_cheddar(goal="place_cheese", retrieval="prev:bbq next:?next"):
        # print(f"placing the cheddar : {next}")
        my_pizza.append(next)
        DM_module.request("prev:cheddar next:?")
        goal.set("place_topping n:bacon")


    def place_topping(goal="place_topping n:?n", retrieval=f"prev:?prev next:?next"):
        # print(f"placing the topping {n} {prev} {next}")
        my_pizza.append(next)
        goal.set("place onion next:onion")
        DM_module.request("prev:n next:?")

    def place_onion(goal="place onion next:?next"):
        # print(f"placing the onion {next}")
        my_pizza.append(next)
        goal.set("cook_pizza")


    def cook_pizza_step(goal="cook_pizza"):
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
