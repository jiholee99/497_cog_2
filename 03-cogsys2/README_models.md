# Pizza model
* In init(), it adds "recipe" chunks to DM_module to specify the order of pizza ingredients (e.g. crust then sauce then cheese)
* prep_ingredients() initiates the process by requesting the first step from DM_module
* There are various production rules like place_crust() and place_sauce() that match on the retrieved DM chunk to get the next ingredient
* They append each ingredient to a list my_pizza to build the pizza representation
* After adding an ingredient, they update the goal and request the next step chunk from DM_module
* This repeats until all ingredients are added, finally reaching cook_pizza_step()
* This rule combines the ingredients in my_pizza into a string and prints it out


# VaccumAgent
* Init() sets the initial goal and home location
* recall_dirty_spots_dm() requests dirty locations from declarative memory
* move_to_dirty_spot() moves to a retrieved dirty location
* clean_cell() cleans the current dirty cell and adds it to DM
* start_swirl() starts a spiral search pattern
* rsearch productions implement the spiral search using motor commands
* forward_rsearch() moves forward until a wall
* left_rsearch() turns left when hitting the wall
* new_search() starts wider spiral after 4 left turns
* handle_wall() handles wall collision during search