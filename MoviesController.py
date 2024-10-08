from MoviesDB import DataManage
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


class DataOperator:
    def __init__(self):
        self.MDdf = DataManage().MDdf

    def get_movie_info(self, title):
        if title not in self.MDdf['Title'].values:
            return None
        else:
            return self.MDdf[self.MDdf['Title'] == title].to_dict('records')[0]

    def search_movies(self, option, value):
        if option == 'Title':
            value = value.lower()
            if value not in self.MDdf['Title'].str.lower().values:
                return None
            else:
                return self.MDdf.loc[self.MDdf['Title'].str.lower() == value]

        elif option == 'Released_Year':
            # if value type is not int --> change to int and find the year
            # but if the value cannot be changed to int --> return None
            try:
                value = int(value)
            except ValueError:
                return None
            if value not in self.MDdf['Released_Year'].values:
                return None
            else:
                return self.MDdf.loc[self.MDdf['Released_Year'] == value]

        elif option == 'Certificate':
            value = value.lower()
            if value in self.MDdf['Certificate'].str.lower().values:
                return self.MDdf.loc[self.MDdf['Certificate'].str.lower() == value]
            else:
                return self.MDdf[self.MDdf['Certificate'].isna()]

        elif option == 'Genre':
            # convert the input value to lowercase for comparison
            value = value.lower()

            # define a function to check if the genre is in the list of genres
            def genre_in_list(genres, value):
                return any(genre.strip().lower() == value for genre in genres.split(','))

            # filter the dataframe based on the function
            filtered_df = self.MDdf[self.MDdf['Genre'].apply(lambda x: genre_in_list(x, value))]
            # return the filtered dataframe
            if filtered_df.empty:
                return None
            else:
                return filtered_df

        elif option == 'Casts':
            self.MDdf['Casts'] = self.MDdf['Casts'].str.split(',')
            self.MDdf = self.MDdf.explode('Casts')
            value = value.lower()
            if value not in self.MDdf['Casts'].str.lower().values:
                return None
            else:
                return self.MDdf.loc[self.MDdf['Casts'].str.lower() == value]

        elif option == 'Director':
            value = value.lower()
            if value not in self.MDdf['Director'].str.lower().values:
                return None
            else:
                return self.MDdf.loc[self.MDdf['Director'].str.lower() == value]
        else:
            return None

    def sort_movies(self, option, direct):
        if direct == 'ascending order':
            direct = True
        else:  # descending
            direct = False

        if option == 'Title':
            return self.MDdf.sort_values(by=['Title'], ascending=direct).iloc[:, 1:16]
        elif option == 'Released_Year':
            return self.MDdf.sort_values(by=['Released_Year'], ascending=direct).iloc[:, 1:16]
        elif option == 'Runtime (minutes)':
            return self.MDdf.sort_values(by=['Runtime (minutes)'], ascending=direct).iloc[:, 1:16]
        elif option == 'IMDB_Rating':
            return self.MDdf.sort_values(by=['IMDB_Rating'], ascending=direct).iloc[:, 1:16]
        elif option == 'Meta_score':
            return self.MDdf.sort_values(by=['Meta_score'], ascending=direct).iloc[:, 1:16]
        elif option == 'No_of_Votes':
            return self.MDdf.sort_values(by=['No_of_Votes'], ascending=direct).iloc[:, 1:16]
        elif option == 'Gross':
            return self.MDdf.sort_values(by=['Gross'], ascending=direct).iloc[:, 1:16]
        else:
            return None


class DataVisualization:
    def __init__(self):
        self.MDdf = DataManage().MDdf
        plt.rcParams['font.family'] = 'Montserrat'
        plt.rcParams['font.size'] = 10

    def distribution_graph(self, feature):
        if feature not in ['No_of_Votes', 'IMDB_Rating', 'Gross',
                           'Meta_score', 'Runtime (minutes)']:
            print('Invalid feature')
            return None

        sns.set_style('dark')
        fig, ax = plt.subplots(figsize=(10, 6))

        if feature in ['No_of_Votes', 'Gross']:
            sns.histplot(self.MDdf[feature], bins=30, kde=True, color='red')
        else:
            sns.kdeplot(self.MDdf[feature], fill=True, color='red')

        ax.set_facecolor('#1B1A1A')
        fig.set_facecolor('#1B1A1A')
        ax.tick_params(colors='white', which='both')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')

        ax.set_xlabel(feature.replace('_', ' '), color='white')
        ax.set_ylabel('Density' if feature in ['IMDB_Rating', 'Meta_score', 'Runtime (minutes)'] else 'Count',
                      color='white')
        ax.set_title(f'Distribution of {feature.replace("_", " ")}', fontsize=14, color='white')
        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')

        sns.despine()
        plt.tight_layout()
        return fig

    def bar_graph(self, feature):
        if feature not in [
            'Top IMDB Rating Movies', 'Number of votes of Top Rating Movies',
            'Meta scores of Top Rating Movies', 'Gross of Top Rating Movies',
            'Certificates of Top Rating Movies', 'The Director with the most movie credits',
            'The Star with the most movie appearances'
        ]:
            print('Invalid feature')
            return None

        sns.set_style('dark')
        fig, ax = plt.subplots(figsize=(10, 6))
        color = 'Spectral'

        if feature == 'Top IMDB Rating Movies':
            data = self.MDdf.nlargest(10, 'IMDB_Rating')[['Title', 'IMDB_Rating']]
            sns.barplot(data=data, x='IMDB_Rating', y='Title', palette=color)
            ax.set_xlim(0, 10)
            ax.set_xlabel('IMDB Rating')
            ax.set_ylabel('Movie Title')

        elif feature == 'Number of votes of Top Rating Movies':
            data = self.MDdf.nlargest(10, 'IMDB_Rating')[['Title', 'No_of_Votes']]
            ax = sns.barplot(data=data, x='No_of_Votes', y='Title', palette=color)
            plt.xlabel('Number of Votes')
            plt.ylabel('Movie Title')

        elif feature == 'Meta scores of Top Rating Movies':
            data = self.MDdf.nlargest(10, 'IMDB_Rating')[['Title', 'Meta_score']]
            sns.barplot(data=data, x='Meta_score', y='Title', palette=color)
            ax.set_xlabel('Meta scores')
            ax.set_ylabel('Movie Title')

        elif feature == 'Gross of Top Rating Movies':
            data = self.MDdf.nlargest(10, 'IMDB_Rating')[['Title', 'Gross']]
            sns.barplot(data=data, x='Gross', y='Title', palette=color)
            ax.set_xlabel('Gross')
            ax.set_ylabel('Movie Title')

        elif feature == 'Certificates of Top Rating Movies':
            top_rated_movies = self.MDdf.nlargest(10, 'IMDB_Rating')
            data = top_rated_movies['Certificate'].value_counts()
            sns.barplot(x=data.index, y=data.values, palette=color)
            ax.set_xlabel('Certificate')
            ax.set_ylabel('Number of Movies')

        elif feature == 'The Director with the most movie credits':
            data = self.MDdf['Director'].value_counts().nlargest(10)
            sns.barplot(x=data.values, y=data.index, palette=color)
            ax.set_xlabel('Number of Movies')
            ax.set_ylabel('Director')

        elif feature == 'The Star with the most movie appearances':
            stars = self.MDdf['Casts'].str.split(',', expand=True).stack().value_counts().nlargest(10)
            data = stars.reset_index()
            data.columns = ['Star', 'Appearances']
            sns.barplot(data=data, x='Star', y='Appearances', palette=color)
            ax.set_xlabel('Stars')
            ax.set_ylabel('Number of Movie Appearances')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')

        ax.set_facecolor('#1B1A1A')
        fig.set_facecolor('#1B1A1A')
        ax.tick_params(colors='white', which='both')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        ax.set_title(f'{feature}', fontsize=14, color='white')
        sns.despine()
        plt.tight_layout()
        return fig

    def line_graph(self, feature):
        if feature not in ['No_of_Votes', 'IMDB_Rating', 'Gross', 'Genre',
                           'Meta_score', 'Number of Movies', 'Runtime (minutes)']:
            print('Invalid feature')
            return None

        if feature == 'Genre':
            MDdf2 = self.MDdf.copy()
            MDdf2['Genre'] = MDdf2['Genre'].str.split(', ')
            exploded_df = MDdf2.explode('Genre')
            genre_counts = exploded_df.groupby(['Released_Year', 'Genre']).size().unstack().fillna(0)

            sns.set_style('dark')
            fig, ax = plt.subplots(figsize=(10, 6))
            genre_counts.plot(kind='line', ax=ax, colormap='tab20', linewidth=2)
            ax.set_facecolor('#1B1A1A')
            fig.set_facecolor('#1B1A1A')
            ax.tick_params(colors='white', which='both')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.title.set_color('white')
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
            legend = ax.legend(title='Genre', loc='center right', bbox_to_anchor=(1.2, 0.5),
                               borderaxespad=0., fontsize=9, facecolor='#1B1A1A',
                               edgecolor='white', labelcolor='white')
            for text in legend.get_texts():
                text.set_color('white')
            legend.get_title().set_color('white')
            ax.set_xlabel('Released Year', color='white')
            ax.set_ylabel('Number of Movies', color='white')
            ax.set_title('Number of Movies in Each Genre Over the Years', fontsize=11, color='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

        else:
            if feature == 'Number of Movies':
                avg_values = self.MDdf.groupby('Released_Year').size()
            elif feature == 'Meta_score':
                self.MDdf = self.MDdf.dropna(subset=['Meta_score'])
                avg_values = self.MDdf.groupby('Released_Year')[feature].mean()
            else:
                avg_values = self.MDdf.groupby('Released_Year')[feature].mean()

            sns.set_style('dark')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=avg_values.index, y=avg_values.values, ax=ax, color='red')
            ax.set_facecolor('#1B1A1A')
            fig.set_facecolor('#1B1A1A')
            ax.tick_params(colors='white', which='both')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.title.set_color('white')

            ax.set_xlabel('Released Year', color='white')
            if feature == 'Number of Movies':
                ax.set_ylabel('Number of Movies', color='white')
                ax.set_title('Number of Movies Over the Years', fontsize=13, color='white')
            else:
                ax.set_ylabel(f'Average {feature.replace("_", " ")}', color='white')
                ax.set_title(f'Average {feature.replace("_", " ")} Over the Years', fontsize=13, color='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

        sns.despine()
        plt.tight_layout()
        return fig

    def pie_graph(self, feature):
        if feature not in ['Certificate', 'Genre']:
            print('Invalid feature')
            return None

        if feature == 'Certificate':
            top_counts = self.MDdf['Certificate'].value_counts().nlargest(5)
            others_count = top_counts.iloc[5:].sum()
        elif feature == 'Genre':
            self.MDdf['Genre'] = self.MDdf['Genre'].str.split(', ')
            self.MDdf = self.MDdf.explode('Genre')
            top_counts = self.MDdf['Genre'].value_counts().nlargest(10)
            others_count = top_counts.iloc[10:].sum()
        top_counts['Others'] = others_count

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.set_facecolor('#1B1A1A')
        colors = sns.color_palette('rocket', len(top_counts))
        wedges, texts, autotexts = ax.pie(top_counts, labels=top_counts.index,
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        for text in texts:
            text.set_color('white')
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
        legend = ax.legend(wedges, top_counts.index, title='Categories',
                           loc='center left', bbox_to_anchor=(-0.1, 0.5, 0, 0.05),
                           facecolor='#1B1A1A', edgecolor='white', labelcolor='white', fontsize=9)
        plt.setp(legend.get_texts(), color='white')
        legend.get_title().set_color('white')
        legend.get_title().set_fontsize(9)
        ax.set_title(f'{feature} Distribution', fontsize=11, color='white')
        ax.axis('equal')
        return fig

    def scatter_graph(self, x_feature, y_feature):
        features = ['Runtime (minutes)', 'Meta_score', 'No_of_Votes', 'Gross']
        if x_feature not in features or y_feature not in features:
            print('Invalid features')
            return None

        sns.set_style('dark')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=self.MDdf, x=x_feature, y=y_feature, size='IMDB_Rating', sizes=(20, 200),
                        color='#F06043', legend=True, ax=ax)
        sns.regplot(data=self.MDdf, x=x_feature, y=y_feature, scatter=False, color='red', ax=ax)
        ax.set_facecolor('#1B1A1A')
        fig.set_facecolor('#1B1A1A')
        ax.tick_params(colors='white', which='both')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')

        ax.set_xlabel(x_feature.replace('_', ' '), color='white')
        ax.set_ylabel(y_feature.replace('_', ' '), color='white')
        ax.set_title(f'Scatter plot of {x_feature.replace("_", " ")} and {y_feature.replace("_", " ")}', fontsize=14, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        sns.despine()
        plt.tight_layout()

        return fig

    def network_graph(self, feature):
        if feature not in ['Casts and their movies', 'Directors and their movies', 'Movies in each certificate',
                           'Movies in each genre']:
            print('Invalid feature')
            return None

        G = nx.Graph()

        if feature == 'Casts and their movies':
            for _, row in self.MDdf.iterrows():
                movie = row['Title']
                casts = row['Casts'].split(', ')
                for cast in casts:
                    G.add_node(cast, type='cast')
                    G.add_node(movie, type='movie')
                    G.add_edge(cast, movie)

        elif feature == 'Directors and their movies':
            for _, row in self.MDdf.iterrows():
                movie = row['Title']
                director = row['Director']
                G.add_node(director, type='director')
                G.add_node(movie, type='movie')
                G.add_edge(director, movie)

        elif feature == 'Movies in each certificate':
            for _, row in self.MDdf.iterrows():
                movie = row['Title']
                certificate = row['Certificate']
                G.add_node(certificate, type='certificate')
                G.add_node(movie, type='movie')
                G.add_edge(certificate, movie)

        elif feature == 'Movies in each genre':
            for _, row in self.MDdf.iterrows():
                movie = row['Title']
                genres = row['Genre'].split(', ')
                for genre in genres:
                    G.add_node(genre, type='genre')
                    G.add_node(movie, type='movie')
                    G.add_edge(genre, movie)

        fig, ax = plt.subplots(figsize=(15, 12))
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        node_color = [G.nodes[n]['type'] for n in G.nodes]
        node_colors = {'cast': '#1f78b4', 'movie': '#33a02c', 'director': '#e31a1c', 'certificate': '#ff7f00',
                       'genre': '#6a3d9a'}
        node_color = [node_colors[n] for n in node_color]

        nx.draw(G, pos, with_labels=True, node_color=node_color, edge_color='gray', node_size=200, font_size=5,
                font_color='white', ax=ax)
        ax.set_title(f'Network graph of {feature}', fontsize=10, color='white')
        ax.set_facecolor('#1B1A1A')
        ax.set_axis_off()

        fig.set_facecolor('#1B1A1A')
        plt.tight_layout()

        return fig
