import streamlit as st

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

previous_recipe, current_recipe, next_recipe = st.columns(3)
current_idx = 0
length = 10

with previous_recipe:
    # display the recipe before the current one in the recipe list
    # recipes[current_idx-1]
    # with a smaller size
    if current_idx > 0:
        st.write("")

with current_recipe:
    # display the current recipe 
    # with the normal size
    st.write("")

with next_recipe:
    # display the recipe after the current one in the recipe list
    # with a smaller size as 'previous_recipe'
    if current_idx < length - 1:
        st.write("")


