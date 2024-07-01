

# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib
from flask import Flask, request, jsonify, render_template

# Create a Flask app instance
app = Flask(__name__)

df = pd.read_csv("D:\\AI_Bot\\JK_TEK\\books.csv")
#print(df.head())
#df.describe()

#one-hot encoding for the rating variable
df2 = df.copy()
df2['average_rating'] = pd.to_numeric(df2['average_rating'], errors='coerce')
df2.loc[ (df2['average_rating'] >= 0) & (df2['average_rating'] <= 1), 'rating_between'] = "between 0 and 1"
df2.loc[ (df2['average_rating'] > 1) & (df2['average_rating'] <= 2), 'rating_between'] = "between 1 and 2"
df2.loc[ (df2['average_rating'] > 2) & (df2['average_rating'] <= 3), 'rating_between'] = "between 2 and 3"
df2.loc[ (df2['average_rating'] > 3) & (df2['average_rating'] <= 4), 'rating_between'] = "between 3 and 4"
df2.loc[ (df2['average_rating'] > 4) & (df2['average_rating'] <= 5), 'rating_between'] = "between 4 and 5"

#one-hot encoding for the jenre variable
rating=pd.get_dummies(df2['rating_between'])
rating.head(5)

jenre=pd.get_dummies(df2['jenre'])
jenre.head(5)

features = pd.concat([rating,
                      jenre,
                      df2['average_rating'],
                      df2['ratings_count']
    
], axis=1)
features.head(5)

#feature transformation
scaler=MinMaxScaler()
features=scaler.fit_transform(features)


# Load the trained model
model = joblib.load('D:\\AI_Bot\\JK_TEK\\nearest_neighbors_model.joblib')
dist, idlist = model.kneighbors(features)

#function to recommend books based on a given book title
def BookRecommender(book_name):
    book_list_name = []
    book_id = df2[df2['title'] == book_name].index
    book_id = book_id[0]
    for newid in idlist[book_id]:
        book_list_name.append(df2.loc[newid].title)
    return book_list_name

# Define the route for the home page
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

# Define the route for the book recommendation
@app.route('/recommend_books', methods=['POST'])
def recommendation():
    Book_name = request.form['book-title']
    print(Book_name)
    recommended_books = BookRecommender(Book_name)
    #return jsonify({'recommended_books': recommended_books})
    return render_template('index.html', Recommended_Books=recommended_books)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


