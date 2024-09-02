import pandas as pd
import re
import json
import urllib.request as urlreq
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bio as dashbio

def create_chord_data(df_email):
    """
    Method for creating chord diagram data from email data

    input:
        - email_data
    output:
        - chord_diagram_data
        - chord_diagram_people_data
    """
    # setup color scheme
    color_map = {'Facilities':'green', 'InformationTechnology':'pink', 'Security':'purple', 'Executive':'red', 'Engineering':'yellow', 'Administration':'blue'}

    chord_data = []

    # create connections list and people information list
    # people holds information about nodes such as how many ingoing and outgoing messages there are
    connections = dict(df_email.groupby(by=["from", "to", 'Department']).size())
    people = []
    count = 0 
    for i in list(connections.keys()):
        if i[0] == i[1]:
            connections.pop(i)
        else:
            v = connections[i]
            connections[i] = [v, 0, 0, 0, 0]


            
    for i in list(df_email['from'].unique()):
        count=0
        for key in connections.keys():
            if key[0] == i:
                v = connections[key]
                v[1] = count
                count += v[0]
                v[2] = count
                connections[key] = v
                color = color_map[key[2]]
        for key in connections.keys():
            if key[1] == i:
                v = connections[key]
                v[3] = count
                count += v[0]
                v[4] = count
                connections[key] = v
        people.append({'id': i, 'label':re.sub(r"(\w)([A-Z])", r"\1 \2", i), 'color':color, 'len':count})


    # format connections
    n=1
    for i, key in enumerate(connections.keys()):
        if key[0] != key[1]:
            entry = {'source': {'id':key[0], 'end':connections[key][2]*n, 'start':connections[key][1]*n, 'value':connections[key][0], 'color': color_map[key[2]]}, 
                    'target':{'id':key[1], 'end':connections[key][4]*n, 'start':connections[key][3]*n, 'value':connections[key][0], 'color': color_map[key[2]]}, 'color': color_map[key[2]], 'value':connections[key][0]}
            chord_data.append(entry)

    # format people data
    people = [dict(t) for t in {tuple(d.items()) for d in people}]

    return chord_data, people


# the rest of the scripts creates an initial chord diagram
layout_config = {
    "innerRadius": 300,
    "outerRadius": 350,
    "cornerRadius": 0,
    "labels": {
        "size": 10,
    },
    "ticks": {"display": False},
}

# setup chord diagram data
chord_data, people = create_chord_data(pd.read_csv('modified_data/email_preprocessed.csv'))
# create intiial plot using dash Circos
initial_chord_diagram = dashbio.Circos(
            id="chord_diagram",
            layout=people,
            selectEvent={"2": "both"},
            tracks=[
                {
                    "type": "CHORDS",
                    "data": chord_data,
                    "config": {
                        "tooltipContent": {
                            "source": "source",
                            "sourceID": "id",
                            "target": "target",
                            "targetID": "id",
                            "targetEnd": 'value',
                        },
                        'color':'RdYlBu',
                    },
                }
            ],
            config= layout_config,
        )