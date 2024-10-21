# What's about Movie

## 🎬 Description
This project is a part of the Computer Programming 2 course (Year 1 project). It is an application that showcases movies from the IMDB database, allowing users to search and sort the data. Users can see information about the film. The data can be analyzed from graphs where users can select the type of graph and the data they want.

## 🎬 Data Sources
The data is used in this project from [www.kaggle.com](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)

**Column Description**
- Poster_Link - Link of the poster that IMDB using
- Series_Title = Name of the movie
- Released_Year - Year at which that movie released
- Certificate - Certificate earned by that movie
- Runtime - Total runtime of the movie
- Genre - Genre of the movie
- IMDB_Rating - Rating of the movie at the IMDB site
- Overview - mini story/ summary
- Meta_score - Score earned by the movie
- Director - Name of the Director
- Star1,Star2,Star3,Star4 - Name of the Stars
- No_of_votes - Total number of votes
- writers: Writer of the movie
- Gross - Money earned by that movie
 
## 🎬 Setup and Run the application
### Install the libraries/packages
1. Open your terminal or command prompt
2. Navigate to the directory where your requirements.txt file is located
3. Create a Virtual Environment
```
python -m venv venv
```
5. Activate your virtual environment
   * On Windows:
     ```
     venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```
     source venv/bin/activate
     ```
6.  Install all the packages listed in the requirements.txt
```
pip install -r requirements.txt
```
7. Deactivate the Virtual Environment (when done)
```
deactivate
```
### Run the application
Go to **main.py** to run this application or use a command
```
python Main.py
```
 
## 🎬 Classes Overview
1. `App`: The main application class that initializes and manages the entire application flow and user interface.
2. `BasePage`: Serves as the foundation for all page classes, containing common functionality and properties for pages within the application.
3. `HomePage` (Inherits from `BasePage`): Represents the landing page of the application, providing navigation to other pages and basic functionalities.
4. `InformationPage`: Handles searching, sorting, and retrieving detailed information about films from IMDB.
5. `GraphPage`(Inherits from `BasePage`): Specifically focused on graphical data analysis and visualization, displaying charts and graphs based on movie data.
6. `AboutPage`(Inherits from `BasePage`): Provides information about the application, such as its purpose, developers, and instructions for use.
7. `MoviesControl`: Interfaces with the `DataOperator` class to manage movie data operations. It handles searching and sorting, passing the arranged data to the `InformationPage`.
8. `MoviesStatistics`: Works with the `DataVisualization` class to prepare data for graphical representation in the `GraphPage`.
9. `MoviesDB`: Manages the movie database by reading the CSV file and serving as the data source for other classes.
10. `DataManage`: Responsible for managing the dataset. It likely includes loading, cleaning, and preparing the movie data for analysis and visualization.
11. `DataOperator`: Provides functionalities for retrieving movie information and searching through the dataset. It includes methods to get movie details, search by various criteria, and sort the dataset.
12. `DataVisualization`: Manages the creation of visualizations using the dataset. It includes methods for generating distribution graphs, bar graphs, line graphs, pie charts, scatter plots, and network graphs.

## 🎬 Design Patterns Used
This application uses the **Model-View-Controller (MVC)** pattern, structured as follows:
- **Model (Database)**: `MoviesDB` and `DataManage` - Responsible for managing the movie data and interactions with the CSV file, including loading, cleaning, and preparing data for analysis.
- **View (User Interface)**: `BasePage`, `HomePage`, `InformationPage`, `GraphPage`, and `AboutPage` - These classes display the user interface and interact with the user, presenting data and facilitating navigation.
- **Controller (Data Operations)**: `MoviesControl` and `MoviesStatistics` - These classes handle data operations, manage user inputs, and pass data between the model and the view.
 
## 🎬 Other Information
**Libraries/Packages Used in This Project**
- `customtkinter`: A modern Tkinter framework for creating custom UIs.
- `matplotlib`: For creating static, animated, and interactive visualizations.
- `networkx`: To create, manipulate, and study the structure and dynamics of complex networks.
- `pandas`: For data manipulation and analysis.
- `Pillow`: Used to open and manipulate images.
- `seaborn`: For statistical data visualization.
- `numpy`: For numerical computing.
- `scipy`: For scientific and technical computing.
- `requests`: For making HTTP requests.
- `tkinter`: The standard GUI toolkit for Python.


Thank you for your attention
