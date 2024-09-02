from dash import Dash, html, dcc, callback, Output, Input, no_update
from dash import Dash, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text
from bokeh.embed import json_item
from bokeh.resources import CDN
from bokeh.embed import file_html

import msticpy as mp
# import figures and functions from the other scripts
from organizational_chart import org_chart
from chord_diagram import create_chord_data, initial_chord_diagram

# read preprocessed data 

article_data  = pd.read_csv('modified_data/articles_preprocessed.csv')
email_data  = pd.read_csv('modified_data/email_preprocessed.csv')

color_map = {'Facilities':'green', 'InformationTechnology':'pink', 'Security':'purple', 'Executive':'red', 'Engineering':'yellow', 'Administration':'blue'}
color_legend = ""
for i in color_map:
    color_legend += str(i) 
    color_legend += f': {color_map[i]}\n'

stop_words = ['January', 'PM', 'AM', 'pm', 'am', 'january'] +  [str(x) for x in list(range(2015))]
my_stop_words = list(text.ENGLISH_STOP_WORDS) + stop_words

# setup Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

# Specify App layout
# Sidebar

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Specify Sidebar Layout
sidebar = html.Div(
    [
        html.H3("Sidebar", className="display-4", style={'color':'black', 'font-size':'30px'}),
        html.Hr(),
        # email selection tab
        html.H5('Email Selection:', style={'color':'black', 'font-size':'20px'}),
        html.Pre(id='email_selection', style={'color':'black', 'font-size':'10px'}),
        # machine learning tab
        html.H5('Machine Learning:', style={'color':'black', 'font-size':'20px'}),
        html.H5('Compute Sentiment Scores:', style={'color':'black', 'font-size':'15px'}),
        dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='sentiment', style={'color':'black', 'font-size':'12px'}),
        html.H5('Article Clustering:', style={'color':'black', 'font-size':'15px'}),
        dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='article_cluster', style={'color':'black', 'font-size':'12px'}),
        html.H5('Use Article Clustering to classify email headers:', style={'color':'black', 'font-size':'15px'}),
        dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='email_cluster', style={'color':'black', 'font-size':'12px'}),
        html.Pre(id='clusters_header', style={'color':'black', 'font-size':'20px'}),
        html.Pre(id='clusters_top10', style={'color':'black', 'font-size':'10px'}),
        # reset button and reset button whilst filtering main article data content on cluster
        html.H5('Filter Article Data on learned Clusters:', style={'color':'black', 'font-size':'15px'}),
        dcc.RadioItems(['No', '0','1', '2', '3', '4'], 'No', inline=True, id='article_filter', style={'color':'black', 'font-size':'12px'}),
        html.Pre('', id='filter_text', style={'color':'black', 'font-size':'10px'},),
        html.Button('Article Filtering Reset', id='reset'),
        # color legend
        html.H5('Department color legend:', style={'color':'black', 'font-size':'20px'}),
        html.Pre(color_legend, style={'color':'black', 'font-size':'10px'}),
    
        #html.Button('Cluster Reset', id='reset_cluster'),

    ],
    style=SIDEBAR_STYLE,
)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div([dcc.Store(id='email_data'),
                    dcc.Store(id='article_data', data={"data-frame-article": article_data.to_dict('records')}),  
                    #dcc.Store(id='reset_memory'),
    html.H1(children='MailDash', style={'textAlign':'center'}),
    html.Div([html.Hr(style={'borderWidth': "1vh", "width": "100%", "backgroundColor": "#AB87FF","opacity": "unset",}),
	],),
    html.Div(
        [
            dbc.Row(dbc.Col(html.Div(org_chart))),
            html.Div([html.Hr(style={'borderWidth': "1vh", "width": "100%", "backgroundColor": "#AB87FF","opacity": "unset",}),
	        ],),
            dbc.Row(
                [
                    dbc.Col(html.Div(initial_chord_diagram)),
                    dbc.Col(html.Div(dcc.Graph(id='mail_dist'))),
                ]
            ),
        ]
    ),
    html.Div([html.Hr(style={'borderWidth': "1vh", "width": "100%", "backgroundColor": "#AB87FF","opacity": "unset",}),
	],),
    html.Div(
        [
            dbc.Row([dbc.Col('Email Timeline'), dbc.Col('Article Timeline')]),
            dbc.Row(
                [
                    #dbc.Col(html.Td([dav.BokehJSON(id="bokeh")])),
                    dbc.Col(html.Iframe(id='bokeh_email',
                                        srcDoc=None,
                                        style= {'width':'700px', 'height':'700px'}
                                        )),
                    dbc.Col(html.Iframe(id='bokeh_article',
                                        srcDoc=None,
                                        style= {'width':'700px', 'height':'700px'}
                                        )),
                ]
            ),
        ]
    ),
    
    #html.Pre(id='org-chart-tapNodeData-json'),
    #html.Pre(id='chord-diagram-tapNodeData-json'),
    ], style=CONTENT_STYLE
)
app.layout = html.Div([sidebar, content])

# Define callbacks and interactive figure creating functions

@callback(Output('email_data', 'data', ),
          Output('article_data', 'data'),
          Output('email_selection', 'children'),
          Output('clusters_header', 'children'),
          Output('clusters_top10', 'children'),
              #Input('chord_diagram', 'selectedNodeData'), # org chart selection
              Input('org-chart', 'selectedNodeData'), # chord diagram selection
              Input('article_data', 'data'),
              Input('email_cluster', 'value'),
              Input('article_cluster', 'value'),
)          
def update_data(org_chart_selection, article_data_, email_cluster, article_cluster, chord_diagram_selection=[]):

    # email filtering
    selected_org = []
    selected_chord = []

    # filter on org chart diagram selection
    if org_chart_selection:
        for p in org_chart_selection:
            selected_org.append(p['id'])

    if chord_diagram_selection:
        for p in chord_diagram_selection:
            selected_chord.append(p['id'])

    if selected_org:
        if selected_chord:
            # intersection of lists
            selected = list(set(selected_chord) & set(selected_org)) 
        else:
            selected = selected_org
    elif selected_chord:
        selected = selected_chord
    else:
        selected = []

    if selected:
        if len(selected) < 3:
            filtered_email_data = email_data[(email_data['from'].isin(selected)) | (email_data['to'].isin(selected))]
        else:
            filtered_email_data = email_data[(email_data['from'].isin(selected)) & (email_data['to'].isin(selected)) & (email_data['from'] != email_data['to'])]
    else:
        filtered_email_data = email_data

    if not selected:
        email_selection = 'All Emails are Selected'
    elif len(selected) < 3:
        email_selection = f'Emails from or to {selected} are Selected'
    else:
        email_selection = f'Emails between {selected} are Selected'
        

    df_article = article_data_['data-frame-article']
    df_article = pd.DataFrame(df_article)

    clusters_header = ''
    clusters_top10 = ''

    if 'Yes' in article_cluster:
        vectorizer = TfidfVectorizer(
            max_df=0.5,
            min_df=5,
            stop_words=my_stop_words,
        )
        X_tfidf = vectorizer.fit_transform(df_article.Content)

        lsa = make_pipeline(TruncatedSVD(n_components=100), Normalizer(copy=False))
        X_lsa = lsa.fit_transform(X_tfidf)
        #explained_variance = lsa[0].explained_variance_ratio_.sum()

        number_of_clusters = 5
        kmeans = KMeans(
            n_clusters=number_of_clusters,
            max_iter=100,
            n_init=5,
        )

        clusters = kmeans.fit_predict(X_lsa)

        original_space_centroids = lsa[0].inverse_transform(kmeans.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()

        clusters_header =  'Clusters:'

        for i in range(number_of_clusters):
            clusters_top10 += f"Cluster {i}: "
            for ind in order_centroids[i, :10]:
                clusters_top10 += f'{terms[ind]}, '
            clusters_top10 += '\n'

        df_article['Cluster'] = clusters

        if 'Yes' in email_cluster:
            X_tfidf_email = vectorizer.transform(filtered_email_data.Subject)
            X_lsa_email = lsa.transform(X_tfidf_email)
            email_clusters = kmeans.predict(X_lsa_email)

            filtered_email_data['Cluster'] = email_clusters


    

    return {"data-frame-email": filtered_email_data.to_dict('records')}, {"data-frame-article": df_article.to_dict('records')}, email_selection, clusters_header, clusters_top10

# Organizational Chart Select Data callback
@callback(Output('org-chart-tapNodeData-json', 'children'),
              Input('org-chart', 'selectedNodeData'))
def displayTapNodeData(data):
    return json.dumps(data, indent=2)

# Chord Diagram
@callback(
    Output('chord_diagram', 'tracks'),
    Output('chord_diagram', 'layout'),
    Input('email_data', 'data'),
    State("chord_diagram", "tracks"),
    State("chord_diagram", "layout")
)
def update_chord_diagram(data, current_track, current_layout):
    data_email = data['data-frame-email']
    df_email = pd.DataFrame(data_email)
    
    chord_data, people = create_chord_data(df_email)
    
    current_track[0].update(data=chord_data)

    return current_track, people

@callback(
    Output("mail_dist", "figure"), 
    Input("email_data", "data"),
    Input("article_cluster", "value"),
    Input("email_cluster", "value"))
def update_bar_chart(data, ac, ec):
    data_email = data['data-frame-email']
    df_email = pd.DataFrame(data_email)
    # create figure 
    fig = px.bar(df_email, x='from', color='Department', template='none', hover_data=['from', 'to', 'Subject'], color_discrete_map=color_map,)

    # check if clustering is available for email
    if 'Yes' in ac:
        if 'Yes' in ec:
            fig = px.bar(df_email, x='from', color='Cluster', template='none', hover_data=['from', 'to', 'Subject'], color_discrete_map=color_map,)
    

    
    fig.update_layout(width=700, height=700)

    return fig

@callback(Output("bokeh_email", "srcDoc"), 
              Input("email_data", "data"),
              Input("sentiment", "value"),
              Input("article_cluster", "value"),
              Input("email_cluster", "value"),
              )
def email_timeline(data, sentiment, article_cluster, email_cluster):
    data_email = data['data-frame-email']
    df_email = pd.DataFrame(data_email)
    if 'Yes' in sentiment:
        fig = df_email.mp_plot.timeline_values(
            group_by="Department",
            color=color_map, 
            source_columns= ['from', 'to', 'Subject'],
            time_column="Date",
            y="Sentiment Score",
            kind=["circle"],
            width=700,
        )   
    else:
        fig = df_email.mp_plot.timeline(
            group_by="from",
            source_columns= ['from', 'to', 'Subject'],
            time_column="Date",
            width=700,
        )

    if 'Yes' in article_cluster:
        if 'Yes' in email_cluster:
            if 'Yes' in sentiment:
                fig = df_email.mp_plot.timeline_values(
                    group_by="Cluster",
                    source_columns= ['from', 'to', 'Subject'],
                    time_column="Date",
                    y="Sentiment Score",
                    kind=["circle"],
                    width=700,
                )   
            else:
                fig = df_email.mp_plot.timeline(
                    group_by="Cluster",
                    source_columns= ['from', 'to', 'Subject'],
                    time_column="Date",
                    width=700,
                )

    html_fig = file_html(fig, CDN)

    return html_fig

@callback(Output("bokeh_article", "srcDoc"), 
              Input("article_data", "data"),
              Input("sentiment", "value"),
              Input("article_cluster", "value"))
def article_timeline(data, sentiment, article_cluster):
    data_article = data['data-frame-article']
    df_article = pd.DataFrame(data_article)

    if 'Yes' in article_cluster:
        if 'Yes' in sentiment:
            fig = df_article.mp_plot.timeline_values(
                group_by="Cluster",
                source_columns= ['Medium', 'Header'],
                y="Sentiment Score",
                time_column="Date",
                kind=["circle"],
                width=700,
                )
        else:
            fig = df_article.mp_plot.timeline(time_column="Date", source_columns= ['Medium', 'Header'], group_by='Cluster', width=700)
            
    else:
        if 'Yes' in sentiment:
            fig = df_article.mp_plot.timeline_values(
                group_by="Medium",
                source_columns= ['Medium', 'Header'],
                y="Sentiment Score",
                time_column="Date",
                kind=["circle"],
                width=700,
                )
        else:
            fig = df_article.mp_plot.timeline(time_column="Date", source_columns= ['Medium', 'Header'], group_by='Medium', width=700)

    html_fig = file_html(fig, CDN)

    return html_fig


@callback(Output("article_data", "data", allow_duplicate=True), 
          Output('filter_text', 'children', allow_duplicate=True),
          Output('clusters_header', 'children', allow_duplicate=True),
          Output('clusters_top10', 'children', allow_duplicate=True),
              Input("reset", "n_clicks"), prevent_initial_call=True)
def reset_article_data(reset):

    return {"data-frame-article": article_data.to_dict('records')}, '', '', ''

@callback(Output("email_cluster", "value"), 
          Output("article_cluster", "value"), 
          Output("article_data", "data", allow_duplicate=True),
          Output("article_filter", "value"),
          Output('filter_text', 'children'),
          #Output("article_cluster", "value"),
              Input("article_filter", "value"),
              Input("article_data", "data"),
              Input("article_cluster", "value"),
              Input('filter_text', 'children'), prevent_initial_call=True)
def article_cluster_filtering(article_filter, data, article_cluster, text):
    data_article = data['data-frame-article']
    df_article = pd.DataFrame(data_article)
    # check if filtering cluster in inputted
    if 'No' not in article_filter:
    #check if clustering is done
        if 'Yes' in article_cluster:
            # update article database and reset clustering buttons
            df_article = df_article[(df_article['Cluster'] == int(article_filter[0]))]
            text += f'-> Article Data filtered on Cluster {int(article_filter[0])}\n'

            return 'No', 'No', {"data-frame-article": df_article.to_dict('records')}, 'No', text
    return no_update


if __name__ == '__main__':
    app.run(debug=True)


