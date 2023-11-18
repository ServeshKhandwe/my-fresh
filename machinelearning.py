import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

class machinelearning:
    def __init__(self, file_path):
        self.file_path = file_path
        self.recipes_df = self.load_data()

    @st.cache(allow_output_mutation=True)
    def load_data(self):
        # Load the dataset
        df = pd.read_csv(self.file_path)
        df.dropna(subset=['name'], inplace=True)
        return df

    def train_model(self, liked_recipes):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.recipes_df['name'])
        liked_indices = self.recipes_df[self.recipes_df['id'].isin(liked_recipes)].index
        liked_matrix = tfidf_matrix[liked_indices]
        model = NearestNeighbors(n_neighbors=min(3, len(liked_indices)), metric='cosine')
        model.fit(liked_matrix)
        return model, tfidf_vectorizer

    def get_recommendations(self, model, tfidf_vectorizer, liked_recipes):
        liked_indices = self.recipes_df[self.recipes_df['id'].isin(liked_recipes)].index
        liked_matrix = tfidf_vectorizer.transform(self.recipes_df.loc[liked_indices, 'name'])
        distances, indices = model.kneighbors(liked_matrix)
        recommended_indices = list(set(indices.flatten()))
        recommended_indices = [i for i in recommended_indices if i not in liked_indices]
        return self.recipes_df.iloc[recommended_indices]

    def generateOnereceipe():
        recipe=load_data()
        return recipe.sample(1)

def main():
    file_path = '/Users/serveshkhandwe/Desktop/hacaktumtry/RAW_recipes.csv'  # Or use st.text_input to get user input
    recommender = RecipeRecommender(file_path)

    st.title("Recipe Recommendation System")

    # Initialize or update the user's liked recipes in a session state
    if 'liked_recipes' not in st.session_state:
        st.session_state.liked_recipes = set()
    if 'sample_recipes' not in st.session_state:
        st.session_state.sample_recipes = recommender.recipes_df.sample(1)
    if 'next_pressed' not in st.session_state:
        st.session_state.next_pressed = False

    st.header("Select recipes you like from these options")

    # Display recipe selection checkboxes
    for recipe in st.session_state.sample_recipes.itertuples():
        checkbox_label = f"{recipe.name} (ID: {recipe.id})"
        if st.checkbox(checkbox_label, key=recipe.id):
            st.session_state.liked_recipes.add(recipe.id)
        elif recipe.id in st.session_state.liked_recipes:
            st.session_state.liked_recipes.remove(recipe.id)

    if st.button("Next"):
        st.session_state.sample_recipes = recommender.recipes_df.sample(1)
        st.session_state.next_pressed = True

    if st.button("Submit Feedback") and st.session_state.next_pressed:
        st.write("You have liked these recipes (IDs):", st.session_state.liked_recipes)

        if len(st.session_state.liked_recipes) >= 5:
            st.write("Training the model based on your likes...")
            model, tfidf_vectorizer = recommender.train_model(list(st.session_state.liked_recipes))
            recommendations = recommender.get_recommendations(model, tfidf_vectorizer, list(st.session_state.liked_recipes))
            st.write("Recommended Recipes based on your likes:")
            for index, row in recommendations.iterrows():
                st.text(f"{row['name']} (ID: {row['id']})")
        else:
            st.write("Please like a total of 5 recipes to train the model.")

    if not st.session_state.next_pressed:
        st.experimental_rerun()

if __name__ == "__main__":
    main()
