# What's about Movie

## 🎬 Description
This project is an application that showcases popular movies from the IMDB database, allowing users to search and sort the data. You can also visit the IMDB website for more information about the film. And the data can be analyzed from graphs where users can select the type of graph and the data they want.

## 🎬 Data Sources
My database for using in this project from [www.kaggle.com](https://www.kaggle.com/datasets/rajugc/imdb-top-250-movies-dataset)

**Column Description**
- rank: Rank of the movie
- name: Name of the movie
- year: Release year
- rating: Rating of the movie
- genre: Genre of the movie
- certificate: Certificate of the movie
- run_time: Total movie run time
- tagline: Tagline of the movie
- budget: Budget of the movie
- box_office: Total box office collection across the world
- casts: All casts of the movie
- directors: Director of the movie
- writers: Writer of the movie
- link: Link of movie page in IMDB website *(this column is added from the original database)*
 
## 🎬 Running the Application
go to **main.py** to run this application or using this command

 
## 🎬 Design
There are 6 classes in this project.
- ```Page```: This class is the main page of the program.
- ```InformationPage```: This class inherits from the Page class and uses for searching, sorting and visiting the IMDB website for more information about the film.
- ```StatisticsPage```: This class inherits from the Page class and is used for graphical data analysis such as bar graphs, pie graphs, and line graphs.
- ```MoviesControl```: This class uses the data from the Movie DB class and operates this data about searching and sorting and passes arranged data to the InformationPage class.
- ```MoviesStatistics```: This class uses the data from the Movie DB class and operates this data about preparing data to show the graph in the InformationPage class.
- ```MoviesDB```: This class uses to read csv flie as the database.

## 🎬 Design Patterns Used
This application uses **Model-View-Controller pattern**, by using
- Model part (Database): ```MoviesDB```
- View part (Displays the user interface and interacts with the user): ```Page``` , ```InformationPage``` and ```StatisticsPage```
- Controller (Operate the data): ```MoviesControl``` and ```MoviesStatistics```
 
## 🎬 Other Information
**modules used in this project** 
- tkinter
- seaborn
- matplotlib
- PIL: use to open image
- webview: use to display web content within a desktop application
- matplotlib.backends.backend_tkagg: use to create Matplotlib figures and plots and display them within a Tkinter application, in Scatter graph part
- matplotlib.backends._backend_tk: use to create toolbar in Scatter graph part
