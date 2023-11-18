import streamlit as st
from streamlit_card import card

# Sample data
ingredients = ["Tomato", "Chicken", "Basil", "Milk"]

# Initialize session state
if 'liked' not in st.session_state:
    st.session_state['liked'] = []
if 'rejected' not in st.session_state:
    st.session_state['rejected'] = []

# Layout
left_col, mid_col, right_col = st.columns(3)

with left_col:
    st.write("Rejected Ingredients")
    for item in st.session_state['rejected']:
        st.write(item)

with mid_col:
    st.write("All Ingredients")
    for item in ingredients:
        if st.button(f"Like {item}"):
            st.session_state['liked'].append(item)
        if st.button(f"Reject {item}"):
            st.session_state['rejected'].append(item)

with right_col:
    st.write("Liked Ingredients")
    for item in st.session_state['liked']:
        st.write(item)

# Recipe logic and display would go here

# give me a list of recipes!
# random list at first
# ranked by recommendation algorithm
# Sample recipes
recipes_data = {
    "Recipe 1": {
        "Ingredients": ["Chicken", "Broccoli", "Soy Sauce", "Garlic", "Ginger"],
        "Instructions": "1. Cook chicken in soy sauce.\n2. Add broccoli, garlic, and ginger. Cook until tender.",
    },
    "Recipe 2": {
        "Ingredients": ["Salmon", "Lemon", "Dill", "Olive Oil", "Salt", "Pepper"],
        "Instructions": "1. Season salmon with salt and pepper.\n2. Squeeze lemon over the salmon. Sprinkle with dill.\n3. Grill or bake until cooked through.",
    },
    "Recipe 3": {
        "Ingredients": ["Pasta", "Tomatoes", "Basil", "Garlic", "Olive Oil"],
        "Instructions": "1. Cook pasta according to package instructions.\n2. Saute tomatoes, garlic, and basil in olive oil.\n3. Toss cooked pasta with the sauce.",
    },
    "Recipe 4": {
        "Ingredients": ["Quinoa", "Black Beans", "Corn", "Avocado", "Lime", "Cilantro"],
        "Instructions": "1. Cook quinoa according to package instructions.\n2. Mix quinoa with black beans, corn, diced avocado, lime juice, and chopped cilantro.",
    },
    "Recipe 5": {
        "Ingredients": ["Eggs", "Spinach", "Feta Cheese", "Onion", "Mushrooms"],
        "Instructions": "1. Saute spinach, mushrooms, and onions.\n2. Beat eggs and pour over the vegetables.\n3. Sprinkle feta cheese on top. Cook until eggs are set.",
    },
}

# Display sample recipes
for recipe_name, recipe_details in recipes_data.items():
    print(f"Recipe: {recipe_name}")
    print("Ingredients:", ", ".join(recipe_details["Ingredients"]))
    print("Instructions:")
    print(recipe_details["Instructions"])
    print("\n" + "="*30 + "\n")


previous_recipe, current_recipe, next_recipe = st.columns([1, 1.5, 1])
current_idx = 1
length = 10

with previous_recipe:
    # display the recipe before the current one in the recipe list
    # recipes[current_idx-1]
    # with a smaller size
    # with st.expander("previous recipe", True):
    #     if current_idx > 0:
    #         st.write("")
    prv_recipe = card(key="previous",
                      title="previous recipe", 
         text=list(recipes_data.values())[current_idx-1]["Instructions"],
         styles={
            "card": {
                "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                "height": "600px" # <- if you want to set the card height to 300px
            }
        })

with current_recipe:
    # display the current recipe 
    # with the normal size
    cur_recipe = card(key="current", 
                      title="current recipe", 
         text=list(recipes_data.values())[current_idx]["Instructions"],
         styles={
            "card": {
                "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                "height": "600px" # <- if you want to set the card height to 300px
            }
        })

with next_recipe:
    # display the recipe after the current one in the recipe list
    # with a smaller size as 'previous_recipe'
    
    if current_idx < length - 1:
        nxt_recipe = card(key="next",
                          title="next recipe", 
                          text=list(recipes_data.values())[current_idx+1]["Instructions"],
                          styles={
                        "card": {
                            "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                            "height": "600px" # <- if you want to set the card height to 300px
                        }
                    })
        
def goto_next():
    global current_idx
    current_idx += 1

st.button("next", key="gotonext", 
          on_click=goto_next)


