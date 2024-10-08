from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import customtkinter as ctk
from MoviesController import DataOperator, DataVisualization
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import requests
import io


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title('What\'s about Movie Program')
        self.geometry('960x540')
        self.iconbitmap('pictures/app_icon.ico')
        self.resizable(False, False)
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(side='top', fill='both', expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def show_page(self, page):
        showed_page = page(self, self.frame)
        showed_page.grid(row=0, column=0, sticky='nsew')
        showed_page.lift()

    def run(self):
        self.show_page(HomePage)
        self.mainloop()


class BasePage(ctk.CTkFrame):
    def __init__(self, root, frame):
        super().__init__(frame)
        self.root = root
        self.set_background()
        self.graph_btn = None
        self.info_btn = None
        self.home_btn = None

    def set_background(self, bg_pic='pictures/home_bg.png'):
        bg = Image.open(bg_pic)
        resized_bg = bg.resize((960, 540))
        bg = ctk.CTkImage(light_image=resized_bg, dark_image=resized_bg, size=(960, 540))
        bg_label = ctk.CTkLabel(self, text='', image=bg)
        bg_label.place(relx=0.5, rely=0.5, anchor='center')

    def menu_button(self):
        corner_colors = ('#020300', '#020300', '#020300', '#020300')
        style = {'font': ('Montserrat', 13), 'fg_color': '#3F3E3E',
                 'text_color': 'white', 'hover_color': '#CF0001',
                 'corner_radius': 20, 'border_width': 0,
                 'border_color': '#020300'}
        # Home menu
        self.home_btn = ctk.CTkButton(self, text='HOME',
                                      command=lambda: self.root.show_page(HomePage),
                                      **style, background_corner_colors=corner_colors)
        self.home_btn.place(relx=0.25, rely=0.1, anchor='center')
        # Info menu
        self.info_btn = ctk.CTkButton(self, text='INFORMATION PAGE',
                                      command=lambda: self.root.show_page(InformationPage),
                                      **style, background_corner_colors=corner_colors)
        self.info_btn.place(relx=0.5, rely=0.1, anchor='center')
        # Graph menu
        self.graph_btn = ctk.CTkButton(self, text='GRAPH PAGE',
                                       command=lambda: self.root.show_page(GraphPage),
                                       **style, background_corner_colors=corner_colors)
        self.graph_btn.place(relx=0.75, rely=0.1, anchor='center')


class HomePage(BasePage):
    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_background('pictures/home_bg.png')
        self.menu_button()
        self.about_btn()
        self.home_btn.configure(fg_color='#CF0001', text_color='white')

    def about_btn(self):
        # About project menu
        about_btn = ctk.CTkButton(self, text='ABOUT PROJECT',
                                  command=lambda: self.root.show_page(AboutPage),
                                  font=('Montserrat', 13), fg_color='white',
                                  text_color='black', hover_color='#CF0001',
                                  corner_radius=20, border_width=0,
                                  border_color='#020300',
                                  background_corner_colors=('black', 'black', 'black', 'black'))
        about_btn.place(relx=0.5, rely=0.8, anchor='center')


class InformationPage(BasePage):
    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.data_operator = DataOperator()
        self.set_background('pictures/all_bg.png')
        self.menu_button()
        self.info_btn.configure(fg_color='#CF0001', text_color='white')
        self.search_by()
        self.sort_by()
        self.tree = None
        self.scrolly = None
        self.scrollx = None

    def search_by(self):
        combobox_var = ctk.StringVar(value='Choose an option')  # set initial value
        style = {'font': ('Montserrat', 13), 'text_color': 'white',
                 'border_width': 0, 'corner_radius': 0,
                 'dropdown_fg_color': 'black', 'dropdown_font': ('Montserrat', 13)}
        # text label
        lb_search_by = ctk.CTkLabel(self, text='Search the movie by ',
                                    font=('Montserrat', 13),
                                    text_color='white', bg_color='#151515')
        lb_search_by.place(relx=0.15, rely=0.2, anchor='center')
        # search combobox
        search_combobox = ctk.CTkComboBox(self,
                                          values=['Title', 'Released_Year', 'Certificate', 'Genre',
                                                  'Director', 'Casts'], **style,
                                          variable=combobox_var, width=150, height=20)
        search_combobox.place(relx=0.3, rely=0.2, anchor='center')
        # search entry
        search_entry = ctk.CTkEntry(self, placeholder_text='Search a movie', font=('Montserrat', 13),
                                    corner_radius=0, width=300, height=20)
        search_entry.place(relx=0.57, rely=0.2, anchor='center')
        # search button
        search_btn = ctk.CTkButton(self, text='Search',
                                   command=lambda: self.search_results(search_combobox.get(),
                                                                       search_entry.get()),
                                   font=('Montserrat', 13), fg_color='#3F3E3E',
                                   text_color='white', hover_color='grey', border_color='#3F3E3E',
                                   background_corner_colors=('#3F3E3E', '#3F3E3E', '#3F3E3E', '#3F3E3E'),
                                   width=70, height=15)
        search_btn.place(relx=0.78, rely=0.2, anchor='center')

    def search_results(self, search_option, search_text):
        try:
            if self.tree:
                self.tree.destroy()
            if self.scrolly:
                self.scrolly.destroy()
            if self.scrollx:
                self.scrollx.destroy()
        except Exception as e:
            print(f'Exception while destroying widgets: {e}')

        data = self.data_operator.search_movies(search_option, search_text)
        if data is None or data.empty:
            try:
                if self.tree:
                    self.tree.destroy()
                if self.scrolly:
                    self.scrolly.destroy()
                if self.scrollx:
                    self.scrollx.destroy()
            except Exception as e:
                print(f'Exception while destroying widgets: {e}')

            self.lb_not_found = ctk.CTkLabel(self, text='No results found', bg_color='#151515',
                                             text_color='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.4, anchor='center')
        else:
            try:
                if self.lb_not_found:
                    self.lb_not_found.destroy()
            except Exception as e:
                print(f'Exception while destroying label: {e}')

            # create a sub-frame for the Treeview
            sub_frame = tk.Frame(self, bg='#1B1A1A')
            sub_frame.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.6)

            # create ttk.Treeview inside sub-frame
            self.tree = ttk.Treeview(sub_frame)
            self.tree.place(relheight=1, relwidth=1)
            self.scrolly = tk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            self.scrollx = tk.Scrollbar(sub_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
            self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
            self.tree.configure(xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)

            columns = data.columns[1:-1]
            # set columns and headings
            self.tree['column'] = list(columns)
            self.tree['show'] = 'headings'
            for column in self.tree['column']:
                self.tree.heading(column, text=column)
            df_rows = data.iloc[:, 1:-1].to_numpy().tolist()
            for row in df_rows:
                self.tree.insert('', 'end', values=row)

            # bind event
            self.tree.bind('<<TreeviewSelect>>', self.on_movie_select)

    def sort_by(self):
        sort_combobox_var = ctk.StringVar(value='Choose an option')  # set initial value for sort combobox
        direct_combobox_var = ctk.StringVar(value='ascending order')  # set initial value for direction combobox
        style = {'font': ('Montserrat', 13), 'text_color': 'white',
                 'border_width': 0, 'corner_radius': 0,
                 'dropdown_fg_color': 'black', 'dropdown_font': ('Montserrat', 13)}
        # text label
        lb_sort_by = ctk.CTkLabel(self, text='Sort movies by ',
                                  font=('Montserrat', 13),
                                  text_color='white', bg_color='#151515')
        lb_sort_by.place(relx=0.15, rely=0.25, anchor='center')
        # sort combobox
        sort_combobox = ctk.CTkComboBox(self,
                                        values=['Title', 'Released_Year', 'Runtime (minutes)',
                                                'IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross'],
                                        **style, variable=sort_combobox_var, width=150, height=20)
        sort_combobox.place(relx=0.3, rely=0.25, anchor='center')
        # direct label
        lb_direct_in = ctk.CTkLabel(self, text='in',
                                    font=('Montserrat', 13),
                                    text_color='white', bg_color='#151515')
        lb_direct_in.place(relx=0.4, rely=0.25, anchor='center')
        # direct combobox
        direct_combobox = ctk.CTkComboBox(self,
                                          values=['ascending order', 'descending order'],
                                          **style, variable=direct_combobox_var, width=150, height=20)
        direct_combobox.place(relx=0.493, rely=0.25, anchor='center')
        # show result button
        show_btn = ctk.CTkButton(self, text='Show',
                                 command=lambda: self.show_movies(sort_combobox.get(),
                                                                  direct_combobox.get()),
                                 font=('Montserrat', 13), fg_color='#3F3E3E',
                                 text_color='white', hover_color='grey', border_color='#3F3E3E',
                                 background_corner_colors=('#3F3E3E', '#3F3E3E', '#3F3E3E', '#3F3E3E'),
                                 width=70, height=15)
        show_btn.place(relx=0.65, rely=0.25, anchor='center')
        # clear result button
        clear_btn = ctk.CTkButton(self, text='Clear',
                                  command=lambda: self.root.show_page(InformationPage),
                                  font=('Montserrat', 13), fg_color='#3F3E3E',
                                  text_color='white', hover_color='grey', border_color='#3F3E3E',
                                  background_corner_colors=('#3F3E3E', '#3F3E3E', '#3F3E3E', '#3F3E3E'),
                                  width=70, height=15)
        clear_btn.place(relx=0.78, rely=0.25, anchor='center')

    def show_movies(self, sort_option, direct):
        try:
            if self.tree:
                self.tree.destroy()
            if self.scrolly:
                self.scrolly.destroy()
            if self.scrollx:
                self.scrollx.destroy()
        except Exception as e:
            print(f'Exception while destroying widgets: {e}')

        data = self.data_operator.sort_movies(sort_option, direct)
        if data is None:
            try:
                if self.tree:
                    self.tree.destroy()
                if self.scrolly:
                    self.scrolly.destroy()
                if self.scrollx:
                    self.scrollx.destroy()
            except Exception as e:
                print(f'Exception while destroying widgets: {e}')

            self.lb_not_found = tk.Label(self, text='Please select sort option first', background='#151515',
                                         foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')
        else:
            try:
                if self.lb_not_found:
                    self.lb_not_found.destroy()
            except Exception as e:
                print(f'Exception while destroying label: {e}')

            # Create a sub-frame for the Treeview
            sub_frame = tk.Frame(self, bg='#1F222B')
            sub_frame.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.6)

            # Create ttk.Treeview inside sub-frame
            self.tree = ttk.Treeview(sub_frame)
            self.tree.place(relheight=1, relwidth=1)
            self.scrolly = tk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            self.scrollx = tk.Scrollbar(sub_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
            self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
            self.tree.configure(xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)

            # Set columns and headings
            self.tree['column'] = list(data.columns)
            self.tree['show'] = 'headings'
            for column in self.tree['column']:
                self.tree.heading(column, text=column)
            df_rows = data.to_numpy().tolist()
            for row in df_rows:
                self.tree.insert('', 'end', values=row)

            # bind event
            self.tree.bind('<<TreeviewSelect>>', self.on_movie_select)

    def on_movie_select(self, event):
        selected_item = self.tree.selection()[0]
        selected_movie_title = self.tree.item(selected_item, 'values')[0]
        selected_movie = self.data_operator.get_movie_info(selected_movie_title)
        self.show_movie_details(selected_movie)

    def show_movie_details(self, movie):
        self.set_background('pictures/all_bg.png')
        back_btn = ctk.CTkButton(self, text='BACK',
                                 command=lambda: self.root.show_page(InformationPage),
                                 font=('Montserrat', 13), fg_color='white',
                                 text_color='black', hover_color='#CF0001',
                                 corner_radius=0, border_width=0,
                                 border_color='#020300', width=70, height=15)
        back_btn.place(relx=0.9, rely=0.85, anchor='center')

        # title label
        lb_title = ctk.CTkLabel(self, text=f'{movie.get('Title')}, {movie.get('Released_Year')}',
                                font=('Montserrat', 15),
                                text_color='white', bg_color='#CF0001', justify='left')
        lb_title.place(relx=0.5, rely=0.2, anchor='center')
        # show poster_link
        poster_link = movie.get('Poster_Link')
        if poster_link:
            try:
                response = requests.get(poster_link)
                response.raise_for_status()
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((250, 350), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                poster_label = tk.Label(self, image=photo)
                poster_label.image = photo
                poster_label.place(relx=0.2, rely=0.55, anchor='center')
            except requests.exceptions.RequestException as e:
                print(f'Failed to load image: {e}')
        else:
            print('Poster link not available')

        # rating label
        lb_rating = ctk.CTkLabel(self, text=f'IMDB Rating: {movie.get('IMDB_Rating')} / 10',
                                 font=('Montserrat', 14),
                                 text_color='white', bg_color='#151515')
        lb_rating.place(relx=0.35, rely=0.3, anchor='w')
        # certificate label
        lb_certificate = ctk.CTkLabel(self, text=f'Certificate: {movie.get('Certificate')}',
                                      font=('Montserrat', 13),
                                      text_color='white', bg_color='#151515')
        lb_certificate.place(relx=0.35, rely=0.35, anchor='w')
        # genre label
        lb_genre = ctk.CTkLabel(self, text=f'Genre: {movie.get('Genre')}',
                                font=('Montserrat', 13),
                                text_color='white', bg_color='#151515')
        lb_genre.place(relx=0.35, rely=0.4, anchor='w')
        # Runtime label
        lb_runtime = ctk.CTkLabel(self, text=f'Runtime: {movie.get('Runtime (minutes)')} minutes',
                                  font=('Montserrat', 13),
                                  text_color='white', bg_color='#151515')
        lb_runtime.place(relx=0.35, rely=0.45, anchor='w')
        # meta_score label
        lb_score = ctk.CTkLabel(self, text=f'Meta Score: {movie.get('Meta_score')} / 100',
                                font=('Montserrat', 13),
                                text_color='white', bg_color='#151515')
        lb_score.place(relx=0.35, rely=0.5, anchor='w')
        # number of vote label
        lb_vote = ctk.CTkLabel(self, text=f'Number of votes: {movie.get('No_of_Votes')}',
                               font=('Montserrat', 13),
                               text_color='white', bg_color='#151515')
        lb_vote.place(relx=0.35, rely=0.55, anchor='w')
        # gross label
        lb_gross = ctk.CTkLabel(self, text=f'Gross: {movie.get('Gross')}',
                                font=('Montserrat', 13),
                                text_color='white', bg_color='#151515')
        lb_gross.place(relx=0.35, rely=0.6, anchor='w')
        # overview label
        lb_overview = ctk.CTkLabel(self, text=f'Overview: {movie.get('Overview')}',
                                   font=('Montserrat', 13),
                                   text_color='white', bg_color='#151515', wraplength=550,
                                   justify='left')
        lb_overview.place(relx=0.35, rely=0.67, anchor='w')
        # director label
        lb_director = ctk.CTkLabel(self, text=f'Director: {movie.get('Director')}',
                                   font=('Montserrat', 13),
                                   text_color='white', bg_color='#151515')
        lb_director.place(relx=0.35, rely=0.74, anchor='w')
        # casts label
        lb_casts = ctk.CTkLabel(self, text=f'Casts: {movie.get('Casts')}',
                                font=('Montserrat', 13),
                                text_color='white', bg_color='#151515')
        lb_casts.place(relx=0.35, rely=0.79, anchor='w')


class GraphPage(BasePage):
    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.lb_not_found = None
        self.feature1_combobox_var = None
        self.feature1_combobox = None
        self.graph_type_combobox = None
        self.feature2_combobox_var = None
        self.feature2_combobox = None
        self.data_visualization = DataVisualization()
        self.set_background('pictures/all_bg.png')
        self.menu_button()
        self.graph_btn.configure(fg_color='#CF0001', text_color='white')
        self.graph_combobox()
        self.graph_frame = None

    def graph_combobox(self):
        type_combobox_var = ctk.StringVar(value='Choose an option')  # set initial value
        style = {'font': ('Montserrat', 13), 'text_color': 'white',
                 'border_width': 0, 'corner_radius': 0,
                 'dropdown_fg_color': 'black', 'dropdown_font': ('Montserrat', 13)}

        # text label
        lb_graph_type = ctk.CTkLabel(self, text='Choose a graph type',
                                     font=('Montserrat', 13),
                                     text_color='white', bg_color='#151515')
        lb_graph_type.place(relx=0.1, rely=0.25, anchor='w')

        # graph type combobox
        self.graph_type_combobox = ctk.CTkComboBox(self,
                                                   values=['Distribution graph', 'Bar graph', 'Pie graph',
                                                           'Line graph', 'Scatter graph', 'Network graph'],
                                                   **style, variable=type_combobox_var, width=150, height=20,
                                                   command=self.update_feature_combobox)
        self.graph_type_combobox.place(relx=0.35, rely=0.25, anchor='w')

        # show button
        show_graph_btn = ctk.CTkButton(self, text='Show Graph',
                                       command=lambda: self.show_graph(),
                                       font=('Montserrat', 13), fg_color='#3F3E3E',
                                       text_color='white', hover_color='grey', border_color='#3F3E3E',
                                       background_corner_colors=('#3F3E3E', '#3F3E3E', '#3F3E3E', '#3F3E3E'),
                                       width=70, height=15)
        show_graph_btn.place(relx=0.7, rely=0.25, anchor='w')

    def update_feature_combobox(self, event=None):
        graph_type = self.graph_type_combobox.get()
        if graph_type == 'Choose an option':
            self.lb_not_found = tk.Label(self, text='Please select graph type first', background='#151515',
                                         foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')
            return

        style = {'font': ('Montserrat', 13), 'text_color': 'white',
                 'border_width': 0, 'corner_radius': 0,
                 'dropdown_fg_color': 'black', 'dropdown_font': ('Montserrat', 13)}

        feature1_combobox_var = ctk.StringVar(value='Choose an option')
        feature2_combobox_var = ctk.StringVar(value='Choose an option')
        # text label
        lb_graph_feature = ctk.CTkLabel(self, text='Choose a feature that you want to see its graph\n'
                                                   '(Except for scatter graph, choose 2 features)',
                                        font=('Montserrat', 13),
                                        text_color='white', bg_color='#151515')
        lb_graph_feature.place(relx=0.1, rely=0.31, anchor='w')

        # Remove existing feature comboboxes
        if self.feature1_combobox:
            self.feature1_combobox.place_forget()
            self.feature1_combobox.destroy()
            self.feature1_combobox = None

        if self.feature2_combobox:
            self.feature2_combobox.place_forget()
            self.feature2_combobox.destroy()
            self.feature2_combobox = None

        # create feature combobox
        if graph_type == 'Distribution graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=['No_of_Votes', 'IMDB_Rating', 'Gross',
                                                             'Meta_score', 'Runtime (minutes)'],
                                                     **style, variable=feature1_combobox_var, width=200, height=20)

        elif graph_type == 'Bar graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=[
                                                         'Top IMDB Rating Movies',
                                                         'Number of votes of Top Rating Movies',
                                                         'Meta scores of Top Rating Movies',
                                                         'Gross of Top Rating Movies',
                                                         'Certificates of Top Rating Movies',
                                                         'The Director with the most movie credits',
                                                         'The Star with the most movie appearances'
                                                     ],
                                                     **style, variable=feature1_combobox_var, width=300, height=20)

        elif graph_type == 'Line graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=['No_of_Votes', 'IMDB_Rating', 'Gross', 'Genre',
                                                             'Meta_score', 'Number of Movies', 'Runtime (minutes)'],
                                                     **style, variable=feature1_combobox_var, width=200, height=20)

        elif graph_type == 'Pie graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=['Certificate', 'Genre'],
                                                     **style, variable=feature1_combobox_var, width=200, height=20)

        elif graph_type == 'Scatter graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=['Runtime (minutes)', 'Meta_score', 'No_of_Votes', 'Gross'],
                                                     **style, variable=feature1_combobox_var, width=200, height=20)
            self.feature2_combobox = ctk.CTkComboBox(self,
                                                     values=['Runtime (minutes)', 'Meta_score', 'No_of_Votes', 'Gross'],
                                                     **style, variable=feature2_combobox_var, width=200, height=20)

        elif graph_type == 'Network graph':
            self.feature1_combobox = ctk.CTkComboBox(self,
                                                     values=['Casts and their movies', 'Directors and their movies',
                                                             'Movies in each certificate',
                                                             'Movies in each genre'],
                                                     **style, variable=feature1_combobox_var, width=200, height=20)

        if self.feature1_combobox and self.feature2_combobox:
            self.feature1_combobox.place(relx=0.45, rely=0.3, anchor='w')
            self.feature2_combobox.place(relx=0.7, rely=0.3, anchor='w')
        else:
            self.feature1_combobox.place(relx=0.45, rely=0.3, anchor='w')

    def show_graph(self):
        graph_type = self.graph_type_combobox.get()
        if self.feature1_combobox is None:
            if self.lb_not_found:
                # self.lb_not_found.place_forget()
                self.lb_not_found.destroy()
            self.lb_not_found = tk.Label(self, text='Please select a graph type first', background='#151515',
                                         foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')
            return

        feature1 = self.feature1_combobox.get()
        feature2 = self.feature2_combobox.get() if self.feature2_combobox else None

        if self.graph_frame:
            self.graph_frame.destroy()

        if self.lb_not_found:
            # self.lb_not_found.place_forget()
            self.lb_not_found.destroy()

        if feature1 == 'Choose an option':
            self.lb_not_found = tk.Label(self, text='Please select a feature', background='#151515',
                                         foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')
            return

        if graph_type == 'Scatter graph' and feature2 == 'Choose an option':
            self.lb_not_found = tk.Label(self, text='Please select a second feature', background='#151515',
                                         foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')
            return

        # generate the graph
        fig = None
        if graph_type == 'Distribution graph':
            fig = self.data_visualization.distribution_graph(feature1)
        elif graph_type == 'Bar graph':
            fig = self.data_visualization.bar_graph(feature1)
        elif graph_type == 'Line graph':
            fig = self.data_visualization.line_graph(feature1)
        elif graph_type == 'Pie graph':
            fig = self.data_visualization.pie_graph(feature1)
        elif graph_type == 'Scatter graph':
            fig = self.data_visualization.scatter_graph(feature1, feature2)
        elif graph_type == 'Network graph':
            fig = self.data_visualization.network_graph(feature1)

        if fig:
            fig.set_size_inches(6.75, 4.05)
            fig.tight_layout(pad=1.0)

            if self.graph_frame:
                self.graph_frame.destroy()

            self.graph_frame = ctk.CTkFrame(self, width=675, height=405)
            self.graph_frame.place(relx=0.5, rely=0.68, anchor="center")

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
            canvas.get_tk_widget().configure(width=675, height=405)
        else:
            self.lb_not_found = ctk.CTkLabel(self, text='Graph not available', background='#151515',
                                                 foreground='red', font=('Montserrat', 13))
            self.lb_not_found.place(relx=0.5, rely=0.5, anchor='center')


class AboutPage(BasePage):
    def __init__(self, main_frame, root):
        super().__init__(main_frame, root)
        self.set_background('pictures/about_bg.png')
        self.menu_button()
