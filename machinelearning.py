import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Function to load and preprocess data
@st.cache(allow_output_mutation=True)
def load_data():
    # Load the dataset
    df = pd.read_csv('/Users/serveshkhandwe/Desktop/hacaktumtry/RAW_recipes.csv')
    df.dropna(subset=['name'], inplace=True)
    return df

# Function to train the recommendation model
def train_model(recipes_df, liked_recipes):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(recipes_df['name'])
    liked_indices = recipes_df[recipes_df['id'].isin(liked_recipes)].index
    liked_matrix = tfidf_matrix[liked_indices]
    model = NearestNeighbors(n_neighbors=min(3, len(liked_indices)), metric='cosine')
    model.fit(liked_matrix)
    return model, tfidf_vectorizer

# Function to get recommendations
def get_recommendations(recipes_df, model, tfidf_vectorizer, liked_recipes):
    liked_indices = recipes_df[recipes_df['id'].isin(liked_recipes)].index
    liked_matrix = tfidf_vectorizer.transform(recipes_df.loc[liked_indices, 'name'])
    distances, indices = model.kneighbors(liked_matrix)
    recommended_indices = list(set(indices.flatten()))
    recommended_indices = [i for i in recommended_indices if i not in liked_indices]
    return recipes_df.iloc[recommended_indices]

def returnOnereceipe():
    recipe_df=load_data
    return recipe_df.sample(1)
    
def main():
    st.title("Recipe Recommendation System")

    recipes_df = load_data()

    # Initialize or update the user's liked recipes in a session state
    if 'liked_recipes' not in st.session_state:
        st.session_state.liked_recipes = set()
    if 'sample_recipes' not in st.session_state:
        st.session_state.sample_recipes = recipes_df.sample(5)
    if 'next_pressed' not in st.session_state:
        st.session_state.next_pressed = False

    st.header("Select recipes you like from these five options")

    # Display recipe selection checkboxes
    for recipe in st.session_state.sample_recipes.itertuples():
        checkbox_label = f"{recipe.name} (ID: {recipe.id})"
        if st.checkbox(checkbox_label, key=recipe.id):
            st.session_state.liked_recipes.add(recipe.id)
        elif recipe.id in st.session_state.liked_recipes:
            st.session_state.liked_recipes.remove(recipe.id)

    if st.button("Next"):
        # Load a new set of recipes
        st.session_state.sample_recipes = recipes_df.sample(5)
        st.session_state.next_pressed = True

    if st.button("Submit Feedback") and st.session_state.next_pressed:
        # Display the liked recipes
        st.write("You have liked these recipes (IDs):", st.session_state.liked_recipes)

        # Check if the user has liked at least 5 recipes
        if len(st.session_state.liked_recipes) >= 5:
            st.write("Training the model based on your likes...")
            model, tfidf_vectorizer = train_model(recipes_df, list(st.session_state.liked_recipes))
            recommendations = get_recommendations(recipes_df, model, tfidf_vectorizer, list(st.session_state.liked_recipes))
            st.write("Recommended Recipes based on your likes:")
            for index, row in recommendations.iterrows():
                st.text(f"{row['name']} (ID: {row['id']})")
        else:
            st.write("Please like a total of 5 recipes to train the model.")

    # Reset the next_pressed state if 'Next' is not pressed
    if not st.session_state.next_pressed:
        st.experimental_rerun()

if __name__ == "__main__":
    main()
