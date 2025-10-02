My Recommendation System Projects
This repository contains two simple recommendation system projects I built: one for movies and one for music. Both projects are built in Python using Jupyter Notebooks.

What These Projects Do
The main goal of these projects is to suggest items (movies or songs) to a user. They do this in a few different ways:

Popularity Based: This is the simplest method. It just looks at which movies or songs have been rated or listened to the most by everyone and recommends those. It's a good starting point but isn't personalized.

Item Based (Collaborative Filtering): This method is a bit smarter. It finds items that are similar to each other. For example, if you like a certain song, it will look for other songs that people who liked your song also liked. It then recommends those similar songs to you. The movie project does the same thing with movie features like genre and director.

The Recommenders.py File
You'll notice there is a file called Recommenders.py. I made this file to keep my code organized.

When you're building a project, it's a good idea to separate the main logic from the code that just runs the steps. The Recommenders.py file holds the core "engine" of the recommendation system. It contains the classes and functions that actually figure out what to recommend.

By putting all that logic in a separate file, the main Jupyter Notebook stays clean and easy to read. The notebook is just used for loading the data, running the recommender, and showing the results. This is a common practice in software development. It makes the code easier to manage, test, and reuse in the future. If I wanted to build another recommendation system, I could just import my Recommenders.py file and use it again.

How to Run the Projects
To run these projects, you will need to have Python installed, along with libraries like pandas, numpy, and seaborn.

Make sure you have the dataset files (triplet_file.csv, song_data.csv, and the movie dataset files) in the same folder as the notebook.

Also make sure the Recommenders.py file is in that same folder.

Open the Jupyter Notebook file (.ipynb) for either the music or movie project.

Run the cells one by one from top to bottom.

The code will load the data, build the recommendation models, and then show you some example recommendations. One of the cells will even let you type in a song name to get recommendations for it.
