from dash import Dash
import dash_cytoscape as cyto

"""
This script sets up an organizational chart of the GAStech employee hierarchy from the VAST2014 data using Dash Cytoscape
"""

# Create Data
# Administration
nodes = [{'data':{'id':'MatBramar', 'label':"Mat Bramar"}, 'classes': 'Administration'},
         {'data':{'id':'AndaRibera', 'label':"Anda Ribera"}, 'classes': 'Administration'},
         {'data':{'id':'RachelPantanal', 'label':"Rachel Pantanal"}, 'classes': 'Administration'},
         {'data':{'id':'LindaLagos', 'label':"Linda Lagos"}, 'classes': 'Administration'},
         {'data':{'id':'RuscellaMiesHaber', 'label':"Ruscella MiesHaber"}, 'classes': 'Administration'},
         {'data':{'id':'CarlaForluniau', 'label':"Carla Forluniau"}, 'classes': 'Administration'},
         {'data':{'id':'CorneliaLais', 'label':"Cornelia Lais"}, 'classes': 'Administration'}]  

# Executive
nodes = nodes + [{'data':{'id':'WillemVasco-Pais', 'label':"WillemVasco-Pais"}, 'classes': 'Executive'},
         {'data':{'id':'StenSanjorgeJr', 'label':"StenSanjorgeJr"}, 'classes': 'Executive'},
         {'data':{'id':'IngridBarranco', 'label':"IngridBarranco"}, 'classes': 'Executive'},
         {'data':{'id':'AdaCampo-Corrente', 'label':"AdaCampo-Corrente"}, 'classes': 'Executive'},
         {'data':{'id':'OrhanStrum', 'label':"OrhanStrum"}, 'classes': 'Executive'}] 


edges = [{'data': {'source':'StenSanjorgeJr', 'target':'WillemVasco-Pais'}},
         {'data': {'source':'StenSanjorgeJr', 'target':'IngridBarranco'}},
         {'data': {'source':'StenSanjorgeJr', 'target':'AdaCampo-Corrente'}},
         {'data': {'source':'StenSanjorgeJr', 'target':'OrhanStrum'}},]

# Engineering
nodes = nodes + [{'data':{'id':'IsandeBorrasca', 'label':"IsandeBorrasca"}, 'classes': 'Engineering'},
                 {'data':{'id':'AxelCalzas', 'label':"AxelCalzas"}, 'classes': 'Engineering'},
                 {'data':{'id':'KareOrilla', 'label':"KareOrilla"}, 'classes': 'Engineering'},
                 {'data':{'id':'ElsaOrilla', 'label':"ElsaOrilla"}, 'classes': 'Engineering'},
                 {'data':{'id':'BrandTempestad', 'label':"BrandTempestad"}, 'classes': 'Engineering'},
                 {'data':{'id':'LarsAzada', 'label':"LarsAzada"}, 'classes': 'Engineering'},
                 {'data':{'id':'FelixBalas', 'label':"FelixBalas"}, 'classes': 'Engineering'},
                 {'data':{'id':'LidelseDedos', 'label':"LidelseDedos"}, 'classes': 'Engineering'},
                 {'data':{'id':'BirgittaFrente', 'label':"BirgittaFrente"}, 'classes': 'Engineering'},
                 {'data':{'id':'AdraNubarron', 'label':"AdraNubarron"}, 'classes': 'Engineering'},
                 {'data':{'id':'GustavCazar', 'label':"GustavCazar"}, 'classes': 'Engineering'},
                 {'data':{'id':'ViraFrente', 'label':"ViraFrente"}, 'classes': 'Engineering'},
                 {'data':{'id':'MarinOnda', 'label':"MarinOnda"}, 'classes': 'Engineering'}
                 ] 
edges = edges + [{'data': {'source':'LidelseDedos', 'target':'FelixBalas'}},
                 {'data': {'source':'LidelseDedos', 'target':'AdraNubarron'}},
                 {'data': {'source':'FelixBalas', 'target':'LarsAzada'}},
                 {'data': {'source':'AdraNubarron', 'target':'BirgittaFrente'}},
                 {'data': {'source':'MarinOnda', 'target':'ViraFrente'}},
                 {'data': {'source':'MarinOnda', 'target':'ElsaOrilla'}},
                 {'data': {'source':'MarinOnda', 'target':'IsandeBorrasca'}},
                 {'data': {'source':'MarinOnda', 'target':'GustavCazar'}},
                 {'data': {'source':'ViraFrente', 'target':'BrandTempestad'}},
                 {'data': {'source':'ElsaOrilla', 'target':'AxelCalzas'}},
                 {'data': {'source':'IsandeBorrasca', 'target':'KareOrilla'}},
                ]

# Facilties
nodes = nodes + [{'data':{'id':'BertrandOvan', 'label':"BertrandOvan"}, 'classes': 'Facilities'},
                 {'data':{'id':'EmileArpa', 'label':"EmileArpa"}, 'classes': 'Facilities'},
                 {'data':{'id':'VarroAwelon', 'label':"VarroAwelon"}, 'classes': 'Facilities'},
                 {'data':{'id':'DanteCoginian', 'label':"DanteCoginian"}, 'classes': 'Facilities'},
                 {'data':{'id':'AlbinaHafon', 'label':"AlbinaHafon"}, 'classes': 'Facilities'},
                 {'data':{'id':'BenitoHawelon', 'label':"BenitoHawelon"}, 'classes': 'Facilities'},
                 {'data':{'id':'ClaudioHawelon', 'label':"ClaudioHawelon"}, 'classes': 'Facilities'},
                 {'data':{'id':'HenkMies', 'label':"HenkMies"}, 'classes': 'Facilities'},
                 {'data':{'id':'ValeriaMorlun', 'label':"ValeriaMorlun"}, 'classes': 'Facilities'},
                 {'data':{'id':'AdanMorlun', 'label':"AdanMorlun"}, 'classes': 'Facilities'},
                 {'data':{'id':'CeciliaMorluniau', 'label':"CeciliaMorluniau"}, 'classes': 'Facilities'},
                 {'data':{'id':'IreneNant', 'label':"IreneNant"}, 'classes': 'Facilities'},
                 {'data':{'id':'DylanScozzese', 'label':"DylanScozzese"}, 'classes': 'Facilities'}
                 ] 

edges = edges + [{'data': {'source':'BertrandOvan', 'target':'DanteCoginian'}},
                 {'data': {'source':'BertrandOvan', 'target':'AlbinaHafon'}},
                 {'data': {'source':'BertrandOvan', 'target':'BenitoHawelon'}},
                 {'data': {'source':'BertrandOvan', 'target':'ValeriaMorlun'}},
                 {'data': {'source':'BertrandOvan', 'target':'IreneNant'}},
                 {'data': {'source':'DanteCoginian', 'target':'EmileArpa'}},
                 {'data': {'source':'DanteCoginian', 'target':'VarroAwelon'}},
                 {'data': {'source':'AlbinaHafon', 'target':'CeciliaMorluniau'}},
                 {'data': {'source':'BenitoHawelon', 'target':'ClaudioHawelon'}},
                 {'data': {'source':'BenitoHawelon', 'target':'HenkMies'}},
                 {'data': {'source':'ValeriaMorlun', 'target':'AdanMorlun'}},
                 {'data': {'source':'IreneNant', 'target':'DylanScozzese'}},
                ]

# Security
nodes = nodes + [{'data':{'id':'FelixResumir', 'label':"FelixResumir"}, 'classes': 'Security'},
                 {'data':{'id':'KanonHerrero', 'label':"KanonHerrero"}, 'classes': 'Security'},
                 {'data':{'id':'VarjaLagos', 'label':"VarjaLagos"}, 'classes': 'Security'},
                 {'data':{'id':'StenigFusil', 'label':"StenigFusil"}, 'classes': 'Security'},
                 {'data':{'id':'MinkeMies', 'label':"MinkeMies"}, 'classes': 'Security'},
                 {'data':{'id':'HennieOsvaldo', 'label':"HennieOsvaldo"}, 'classes': 'Security'},
                 {'data':{'id':'IsiaVann', 'label':"IsiaVann"}, 'classes': 'Security'},
                 {'data':{'id':'LoretoBodrogi', 'label':"LoretoBodrogi"}, 'classes': 'Security'},
                 {'data':{'id':'HidekiCocinaro', 'label':"HidekiCocinaro"}, 'classes': 'Security'},
                 {'data':{'id':'IngaFerro', 'label':"IngaFerro"}, 'classes': 'Security'},
                 {'data':{'id':'EdvardVann', 'label':"EdvardVann"}, 'classes': 'Security'},
                 ] 

edges = edges + [{'data': {'source':'FelixResumir', 'target':'EdvardVann'}},
                 {'data': {'source':'FelixResumir', 'target':'LoretoBodrogi'}},
                 {'data': {'source':'FelixResumir', 'target':'HennieOsvaldo'}},
                 {'data': {'source':'FelixResumir', 'target':'StenigFusil'}},
                 {'data': {'source':'FelixResumir', 'target':'VarjaLagos'}},
                 {'data': {'source':'EdvardVann', 'target':'IngaFerro'}},
                 {'data': {'source':'LoretoBodrogi', 'target':'MinkeMies'}},
                 {'data': {'source':'HennieOsvaldo', 'target':'KanonHerrero'}},
                 {'data': {'source':'StenigFusil', 'target':'IsiaVann'}},
                 {'data': {'source':'VarjaLagos', 'target':'HidekiCocinaro'}},
                ]
# IT
nodes = nodes + [{'data':{'id':'LinneaBergen', 'label':"LinneaBergen"}, 'classes': 'IT'},
                 {'data':{'id':'LucasAlcazar', 'label':"LucasAlcazar"}, 'classes': 'IT'},
                 {'data':{'id':'IsakBaza', 'label':"IsakBaza"}, 'classes': 'IT'},
                 {'data':{'id':'NilsCalixto', 'label':"NilsCalixto"}, 'classes': 'IT'},
                 {'data':{'id':'SvenFlecha', 'label':"SvenFlecha"}, 'classes': 'IT'},
                 ] 

edges = edges + [{'data': {'source':'LinneaBergen', 'target':'LucasAlcazar'}},
                 {'data': {'source':'LinneaBergen', 'target':'IsakBaza'}},
                 {'data': {'source':'LinneaBergen', 'target':'NilsCalixto'}},
                 {'data': {'source':'LinneaBergen', 'target':'SvenFlecha'}},
                ]
# combine nodes and edges
elements = nodes + edges\

# create chart using cytoscape
org_chart = cyto.Cytoscape(
    id='org-chart',
    zoomingEnabled=False,
    zoom=0.7,
    elements=elements,
    style={'width': '1400px', 'height': '500px'},
    layout={
        'name': 'breadthfirst',
        'roots': '#StenSanjorgeJr, #MarinOnda, #LidelseDedos, #BertrandOvan, #FelixResumir, #LinneaBergen'
    },
    stylesheet=[
        {
            'selector': 'node',
            'style': {
                'shape': 'rectangle',
                'label': 'data(label)'
            }
        },
        {
            'selector': 'label',
            'style': {
                'content': 'data(label)',   
                'color': 'white',
                'fontsize': 'small',
            }
        },
        {
            'selector': '.Administration',
            'style': {
                'background-color': 'blue',
            }
        },
        {
            'selector': '.Engineering',
            'style': {
                'background-color': 'yellow',
            }
        },
        {
            'selector': '.Executive',
            'style': {
                'background-color': 'red',
            }
        },
        {
            'selector': '.Facilities',
            'style': {
                'background-color': 'green',
            }
        },
                    {
            'selector': '.Security',
            'style': {
                'background-color': 'purple',
            }
        },
                    {
            'selector': '.IT',
            'style': {
                'background-color': 'pink',
            }
        }
    ]
)


