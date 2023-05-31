import pandas as pd
import json
import logging
import sys
import csv

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class MovieAnalyzer:
    def __init__(self):
        self.movies_df = None

    def load_dataset(self, file_path):
        """
        Load the dataset from a CSV file.
        """
        try:
            self.movies_df = pd.read_csv(file_path)
            logger.info(f"Dataset loaded from '{file_path}'.")
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            sys.exit(1)
        except csv.Error as e:
            logger.error(f"Error reading CSV file: {e}")
            sys.exit(1)

    def print_number_of_movies(self):
        """
        Print the number of movies in the dataset.
        """
        if self.movies_df is not None:
            num_movies = len(self.movies_df)
            logger.info(f"Number of movies: {num_movies}")
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

    # def join_csv_files(rating_file, movie_file):
    #     # Read the rating CSV file
    #     rating_df = pd.read_csv(rating_file)
    #
    #     # Read the movie CSV file
    #     movie_df = pd.read_csv(movie_file)
    #
    #     # Join the two DataFrames based on the movieid column
    #     joined_df = pd.merge(rating_df, movie_df, left_on='movieId', right_on='id')
    #
    #     # Select only the movie_name and rating columns
    #     result_df = joined_df[['original_title', 'rating', 'id']]
    #
    #     return result_df

    def print_average_rating(self):
        rating_file = 'C:/Users/erezh/PycharmProjects/MovieRating/ratings.csv'
        rating_df = pd.read_csv(rating_file)
        if rating_df is not None:
            avg_rating = rating_df['rating'].mean()
            logger.info(f"Average rating: {avg_rating:.2f}")
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

    def print_top_rated_movies(self, n=5):

        rating_file_path = 'C:/Users/erezh/PycharmProjects/MovieRating/ratings.csv'
        movie_file_path = 'C:/Users/erezh/PycharmProjects/MovieRating/movies_metadata.csv'

        rating_df = pd.read_csv(rating_file_path)
        movie_df = pd.read_csv(movie_file_path)

        rating_df['movieId'] = rating_df['movieId'].astype(str)
        movie_df['id'] = movie_df['id'].astype(str)

        joined_df = pd.merge(rating_df, movie_df, left_on='movieId', right_on='id')

        result_df = joined_df[['original_title', 'rating', 'id']]

        if result_df is not None:
            top_movies = result_df.nlargest(n, 'rating')
            logger.info(f"Top {n} highest rated movies:")
            logger.info(top_movies.to_string(index=False))
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

    def print_movies_per_year(self):
        """
        Print the number of movies released each year.
        """
        if self.movies_df is not None:
            movies_per_year = self.movies_df['release_date'].value_counts().sort_index()
            logger.info("Number of movies released each year:")
            logger.info(movies_per_year.to_string())
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

    def print_movies_per_genre(self):
        """
            Print the number of movies in each genre.
            """
        if self.movies_df is not None:
            # Extract the genres from the "genres" column
            genres = self.movies_df['genres'].apply(lambda x: [genre['name'] for genre in eval(x)])

            # Flatten the list of genres
            flattened_genres = [genre for sublist in genres for genre in sublist]

            # Count the number of movies in each genre
            genre_counts = pd.Series(flattened_genres).value_counts()

            logger.info("Number of movies in each genre:")
            logger.info(genre_counts.to_string())
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

    def save_dataset_to_json(self, file_path):
        """
        Save the dataset to a JSON file.
        """
        if self.movies_df is not None:
            try:
                self.movies_df.to_json(file_path, orient='records')
                logger.info(f"Dataset saved to '{file_path}'.")
            except Exception as e:
                logger.error(f"Error saving dataset to JSON: {e}")
        else:
            logger.error("Dataset not loaded. Please load the dataset first.")

if __name__ == '__main__':
    # Create an instance of MovieAnalyzer
    analyzer = MovieAnalyzer()

    # Load the dataset
    analyzer.load_dataset('C:/Users/erezh/PycharmProjects/MovieRating/movies_metadata.csv')


    analyzer.print_number_of_movies()
    analyzer.print_average_rating()
    analyzer.print_top_rated_movies(n=5)
    analyzer.print_movies_per_year()
    analyzer.print_movies_per_genre()

    # Save the dataset to a JSON file
    analyzer.save_dataset_to_json('movies_dataset.json')
