import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from phew import Loss_given_delay as lgd
from phew import Cola
from phew import Premium
from phew import Expenses
from phew import Interest_rates
from phew import Time_value
from phew import Annuity
import numpy as np
import plotly.graph_objs as go
from statsmodels.tsa.stattools import adfuller

def create_dash_application(flask_app):
    
    app = dash.Dash(server = flask_app,name = 'tripDelayInsurance',url_base_pathname = '/',suppress_callback_exceptions=True,prevent_initial_callbacks = False,external_stylesheets=[dbc.themes.ZEPHYR,dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME])

    navbar = dbc.NavbarSimple(
        children=[
            dbc.Button('Sidebar',style = {'color':'white','border-color':'white'}, outline=True, color="secondary", className="mr-1", id="btn_sidebar")
        ],
        brand= [html.I(className = "fa-solid fa-road",style = {'color':'white'})," Trip Delay Insurance Pricing"],
        brand_href="#",
        color="primary",
        dark=True,
        fluid=True,
        sticky = 'top'
    )
    
    
    # the style arguments for the sidebar. We use position:fixed and a fixed width
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 62.5,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0.5rem 1rem",
        "background-color": "#f8f9fa",
    }
    
    SIDEBAR_HIDEN = {
        "position": "fixed",
        "top": 62.5,
        "left": "-16rem",
        "bottom": 0,
        "width": "16rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0rem 0rem",
        "background-color": "#f8f9fa",
    }
    
    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "transition": "margin-left .5s",
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }
    
    CONTENT_STYLE1 = {
        "transition": "margin-left .5s",
        "margin-left": "2rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"
    }
    
    sidebar = html.Div(
        [   
            html.Br(),
            html.Br(),
            dbc.Nav(
                [
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-house",style = {'color':'black'}),'  Home']), href="/page-1", id="page-1-link"),
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-person-chalkboard",style = {'color':'black'}),'  Presentations']), href="/page-6", id="page-6-link"),
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-heart-crack",style = {'color':'black'}),'  Loss calculation']), href="/page-2", id="page-2-link"),
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-percent",style = {'color':'black'}),'  Rate calculation']), href="/page-3", id="page-3-link"),
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-money-bill",style = {'color':'black'}),'  Tax calculation']), href="/page-4", id="page-4-link"),
                    dbc.NavLink( html.H6([html.I(className = "fa-solid fa-file-code",style = {'color':'black'}),'  Phew Package']), href="/page-5", id="page-5-link")
                ],
                vertical=True,
                pills=True,
                style = {'background-color':'white'}
            ),
        ],
        id="sidebar",
        style=SIDEBAR_STYLE,
    )
    
    content = html.Div(
    
        id="page-content",
        style=CONTENT_STYLE)
    
    app.layout = html.Div(
        [
            dcc.Store(id='side_click'),
            dcc.Location(id="url"),
            navbar,
            sidebar,
            content,
        ],
    )
    
    
    
    @app.callback(
        [
            Output("sidebar", "style"),
            Output("page-content", "style"),
            Output("side_click", "data"),
        ],
    
        [Input("btn_sidebar", "n_clicks")],
        [
            State("side_click", "data"),
        ]
    )
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                sidebar_style = SIDEBAR_HIDEN
                content_style = CONTENT_STYLE1
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = 'SHOW'
    
        return sidebar_style, content_style, cur_nclick
    
    # this callback uses the current pathname to set the active state of the
    # corresponding nav link to true, allowing users to tell see page they are on
    @app.callback(
        [Output(f"page-{i}-link", "active") for i in range(1, 7)],
        [Input("url", "pathname")],
    )
    def toggle_active_links(pathname):
        if pathname == "/":
            # Treat page 1 as the homepage / index
            return True, False, False,False,False,False
        return [pathname == f"/page-{i}" for i in range(1, 7)]
    
    
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        
        if pathname in ["/", "/page-1"]:
            
            content = [
                        
                        dbc.Row([
                            dbc.Col([
                                
                                html.Iframe(src = 'https://sketchfab.com/models/2aa81ee9d9d7449281d15aa1169d9267/embed?',style = {'height':'100%','width':'100%'})
                                
                                ],width = {'size':12})
                            
                            ],style = {'height':'400px'}),
                        html.Br(),
                        dbc.Row([
                            
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.CardHeader([
                                            html.H5([html.I(className = "fa-solid fa-circle-question fa-bounce",style = {'color':'white'}),' What is it?'],style = {'text-align':'center','color':'white'})
                                        ],style = {'background-color':'#035efc'}),
                                    html.Br(),
                                    html.H6(['Travel insurance'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Trip delay coverage'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Targeting formal sector workers'],style = {'color':'#035efc','text-align':'center','font-family':'forte'})
                                    
                                    ],color = 'white',style = {'height':'100%'})
                                
                                ],width = {'size':3},style = {'height':'100%'}),
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.CardHeader([
                                            html.H5([html.I(className = "fa-solid fa-hands-holding fa-flip",style = {'color':'white'}),' Benefits'],style = {'text-align':'center','color':'white'})
                                        ],style = {'background-color':'#035efc'}),
                                    html.Br(),
                                    html.H6(['Expenses coverage'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Public transport up'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Increased productivity'],style = {'color':'#035efc','text-align':'center','font-family':'forte'})
                                    
                                    ],color = 'white',style = {'height':'100%'})
                                
                                ],width = {'size':3},style = {'height':'100%'}),
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.CardHeader([
                                            html.H5([html.I(className = "fa-solid fa-chart-line fa-flip",style = {'color':'white'}),' Models'],style = {'text-align':'center','color':'white'})
                                        ],style = {'background-color':'#035efc'}),
                                    html.Br(),
                                    html.H6(['ARIMA'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Vasicek'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Actuarial'],style = {'color':'#035efc','text-align':'center','font-family':'forte'})
                                    
                                    ],color = 'white',style = {'height':'100%'})
                                
                                ],width = {'size':3},style = {'height':'100%'}),
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.CardHeader([
                                            html.H5([html.I(className = "fa-solid fa-gears fa-bounce",style = {'color':'white'}),' Design'],style = {'text-align':'center','color':'white'})
                                        ],style = {'background-color':'#035efc'}),
                                    html.Br(),
                                    html.H6(['Losses computation'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Rate computation'],style = {'color':'#035efc','text-align':'center','font-family':'forte'}),
                                    html.H6(['Tax computation'],style = {'color':'#035efc','text-align':'center','font-family':'forte'})
                                    
                                    ],color = 'white',style = {'height':'100%'})
                                
                                ],width = {'size':3},style = {'height':'100%'}),
                            
                            ],style = {'height':'200px'}),
                        html.Br(),
                        html.Hr(),
                        html.Hr()
                        ]
                
            return content
        
        elif pathname == "/page-2":
            
            
            content2 = [
                
                dbc.Row([
                    
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Inflation", tab_id="inflP",id = 'infM'),
                                dbc.Tab(label="CPI", tab_id="cpiP",id = 'cpiM'),
                                dbc.Tab(label="Losses", tab_id="lossP",id = 'lossM')
                                ],
                            id="tabsLoss",
                            active_tab="inflP",
                            ),
                        dbc.Tooltip(
                                    "Inflation forecast model",
                                    target="infM",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "CPI forecast model",
                                    target="cpiM",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "Compute losses",
                                    target="lossM",
                                    placement = 'top'
                                ),
                        html.Div(
                            id = 'contentReplyLoss'
                            )
                    
                    ])
                ]
            
            return content2
        
        elif pathname == "/page-3":
            
            content3 = [
                
                dbc.Row([
                    
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Pure Premium", tab_id="pureP",id = 'putoo'),
                                dbc.Tab(label="Exchange forecast", tab_id="exchP",id = 'extoo'),
                                dbc.Tab(label="Gross Rate", tab_id="grossP",id = 'grotoo')
                                ],
                            id="tabsPremium",
                            active_tab="pureP",
                            ),
                        dbc.Tooltip(
                                    "Compute pure premium",
                                    target="putoo",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "Foreign exchange forecast",
                                    target="extoo",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "Compute gross rate",
                                    target="grotoo",
                                    placement = 'top'
                                ),
                        html.Div(
                            id = 'contentReplyPremium'
                            )
                    
                    ])
                ]
            
            return content3
        
        # If the user tries to reach a different page, return a 404 message   
        elif pathname == "/page-4":
            contentt = [
                        
                        dbc.Row([
                            
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Effective rates", tab_id="aboutEf",id = 'abouteff'),
                                        dbc.Tab(label="Tax", tab_id="tax4",id = 'tax'),
                                        dbc.Tab(label="Notebook", tab_id="taxnot",id = 'taxnote')
                                        ],
                                    id="tabsTax",
                                    active_tab="aboutEf",
                                    ),
                                dbc.Tooltip(
                                            "Effective rates computation",
                                            target="abouteff",
                                            placement = 'top'
                                        ),
                                dbc.Tooltip(
                                            "Head tax compuation",
                                            target="tax",
                                            placement = 'top'
                                        ),
                                dbc.Tooltip(
                                            "Notebook for all the calculations",
                                            target="taxnote",
                                            placement = 'top'
                                        ),
                                html.Div(
                                    id = 'contentReplyTax'
                                    )
                            
                            ])
                        ]
                
            return contentt
        
        # If the user tries to reach a different page, return a 404 message
        elif pathname == "/page-5":
            content5 = [
                        
                        dbc.Row([
                            
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="About", tab_id="aboutP",id = 'aboutphew'),
                                        dbc.Tab(label="Documentation", tab_id="documentation",id = 'docu')
                                        ],
                                    id="tabs5",
                                    active_tab="aboutP",
                                    ),
                                dbc.Tooltip(
                                            "Brief details",
                                            target="aboutphew",
                                            placement = 'top'
                                        ),
                                dbc.Tooltip(
                                            "Read documentation",
                                            target="docu",
                                            placement = 'top'
                                        ),
                                html.Div(
                                    id = 'contentReply5'
                                    )
                            
                            ])
                        ]
                
            return content5
        
        elif pathname == '/page-6':
            
            content7 = [
                        
                        dbc.Row([
                            
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Presentation 1", tab_id="overview",id = 'overviewP'),
                                        dbc.Tab(label="Presentation 2", tab_id="data_analysis",id = 'data analysis')
                                        ],
                                    id="tabOver",
                                    active_tab="overview",
                                    ),
                                dbc.Tooltip(
                                            "Presentation 1 content",
                                            target="overviewP",
                                            placement = 'top'
                                        ),
                                dbc.Tooltip(
                                            "Presentation 2 content",
                                            target="data analysis",
                                            placement = 'top'
                                        ),
                                html.Div(
                                    id = 'contentReplyOver'
                                    )
                            
                            ])
                        ]
            
            return content7
        
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
    
    
    @app.callback(Output("contentReplyOver", "children"), [Input("tabOver", "active_tab")])
    def switch_tabOver(at):
        
        if at == 'overview':
            
            dropdata = dbc.Row(
                           [
                               dbc.Label(" Data", html_for="dropdowndf",width = {'size':4,'offset':1},id = 'dropdata'),
                               dbc.Col(
                                   dcc.Dropdown(
                                   id="dropdowndf",
                                   value = 'inflation',
                                   options=[
                                       {"label": "inflation", "value": 'inflation'},
                                       {"label": "cpi", "value": 'cpi'},
                                       {"label": "realInterest", "value": 'rinterest'},
                                       {"label": "exchangeRate", "value": 'exchangerate'}
                                   ],
                               ),width = 6),
                           ],
                           className="mb-3",
                           )
            
            send_buttonOv = dbc.Row(
                       [
                           dbc.Label("", html_for="button-rowOv", width=2),
                           dbc.Col([
                               dbc.Button(
                                   id="button-rowOv",children = ['Change'],
                                   color = 'primary',
                               ),
                               dbc.Tooltip(children = [
                                   
                                   html.H6(['Data'],style = {'color':'white'}),
                                   dcc.Markdown([
                                       
                                       '''
                                        Change dataset
                                       '''
                                       
                                       ],mathjax = True)
                                   
                                   ],target="button-rowOv",placement = 'right'),
                               dbc.Toast(
                                   "Changed",
                                   id="positioned-toastOv",
                                   header="Data",
                                   is_open=False,
                                   duration = 4000, 
                                   icon="success",
                                   # top: 66 positions the toast below the navbar
                                   style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                       )],
                               width={'size':6,'offset':3},
                           ),
                       ],
                       className="mb-3",
                   )
            
            return [
                
                html.Br(),
                dbc.Row([
                    
                    dbc.Col([
                        dbc.Card([
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                            dbc.CardBody([
                                                html.H5(['ARIMA AND VASICEK INTEREST MODEL APPROACH TO PRICING OF TRIP DELAY INSURANCE FOR FORMAL SECTOR WORKERS IN MALAWI'],style = {'text-align':'center','font-weight':'bold'}),
                                                html.H6(['Precious Nliwasa'],style = {'text-align':'center'}),
                                                html.H6(['28th March, 2024'],style = {'text-align':'center'})
                                            ])
                                        
                                        
                                    ])
                                    
                                ],width = {'size':10,'offset':1})
                            ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    
                                    dbc.Card([
                                        
                                        dbc.CardHeader(['Main Objective']),
                                        dbc.CardBody([
                                            html.Br(),
                                            html.H5([' The work aims at pricing a trip delay insurance product for formal sector workers who take long distance public transport in Malawi.']),
                                            html.Br(),
                                            html.Br()
                                            ])
                                        
                                        ])
                                    
                                    ],width = {'size':5,'offset':1},style = {'height':'100%'}),
                                dbc.Col([
                                    dbc.Card([
                                        
                                        dbc.CardHeader(['Specific objectives']),
                                        dbc.CardBody([
                                            html.Ul([
                                                
                                                html.Li(html.H5(['To calculate loss amount for trip delay risk'])),
                                                html.Li(html.H5(['To calculate sum of gross rates'])),
                                                html.Li(html.H5(['To calculate head tax'])),
                                                html.Li(html.H5(['To establish a model for pricing social travel insurance.']))
                                                
                                                ])
                              
                                            
                                            
                                            ])
                                        ])
                                    ],width = {'size':5},style = {'height':'100%'})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    
                                    dbc.Card([
                                        
                                        dbc.CardHeader(['Progress']),
                                        dbc.CardBody([
                                             html.Br(),
                                             html.Br(),
                                             dbc.Progress(label = 'Data collection 100%',value = 100,color = 'success',striped = True,animated = True,style = {'height':'30px'}),
                                             html.Br(),
                                             dbc.Progress(label = 'Data analysis 89%',value = 89,color = 'success',striped = True,animated = True,style = {'height':'30px'}),
                                             html.Br(),
                                             dbc.Progress(label = 'Dissertation 30%',value = 30,color = 'danger',striped = True,animated = True,style = {'height':'30px'}),
                                             html.Br(),
                                             html.Br()
                                            ])
                                   
                                        
                                        ])
       
                                    ],width = {'size':5,'offset':1}),
                                dbc.Col([
                                    
                                    dbc.Accordion([
                                        
                                        dbc.AccordionItem([
                                            html.H5(['To find a method for pricing trip delay insurance that is not heavy dependent on frequency data, ARIMA-Vasicek approach is being proposed. Potentially, the work can lead to studies on social travel insurance.'])
                                            ],title = 'Introduction'),
                                        dbc.AccordionItem([
                                            
                                            html.Ul([
                                                html.Li(html.H5('Establishment of pricing framework for social trip delay insurance')),
                                                html.Li(html.H5('Potential establishment of a discipline called social travel insurance')),
                                                html.Li(html.H5('Provides an incentive for more workers to use public transport'))
                                                ])
                                            
                                            ],title = 'Justification'),
                                        dbc.AccordionItem([
                                            html.Ul([
                                                html.Li(html.H5('To choose one risk event to model')),
                                                html.Li(html.H5('To write literature review as academic work')),
                                                html.Li(html.H5('To avoid use of backward looking methods in forecasting'))
                                                ])
                                            ],title = 'Comments')
                                        
                                        ],flush = True)
                                    
                                    ],width = {'size':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    
                                    dbc.Card([
                                        
                                        dbc.CardHeader('Datasets'),
                                        dbc.CardBody([
                                            
                                            dropdata,send_buttonOv
                                            ])
                                        ])
         
                                    ],width = {'size':5,'offset':1}),
                                dbc.Col([
                                    
                                    dbc.Card([
                                        
                                        dbc.CardHeader('Other datasets'),
                                        dbc.CardBody([
                                            html.Br(),
                                            html.A(children = [html.H6('Us inflation')],href = 'https://www.statista.com/statistics/244983/projected-inflation-rate-in-the-united-states/'),
                                            html.A(children = [html.H6('Malawi population')],href = 'https://www.ceicdata.com/en/malawi/population-projection-national-statistical-office-of-malawi'),
                                            html.A(children = [html.H6('Lending rates')],href = 'https://www.rbm.mw/Statistics/BankRates')
                                            
                                            ])
                                        ])
                                    
                                    ],width = {'size':5}),
                                
                                
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    
                                    dcc.Graph(id = 'data-graph',style = {'height':'300px'})
                                    ],width = {'size':10,'offset':1})
                                
                                ]),
                            dbc.Row([
                                
                                dbc.Col(id = 'datasetsOv',width = {'size':10,'offset':1})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    
                                    dbc.Accordion([
                                        
                                        dbc.AccordionItem([
                                            
                                            dcc.Markdown([
                                                
                                                '''
                                                $$ 
                                                H_0 : There \quad is \quad unit \quad root
                                                $$
                                                
                                                $$
                                                H_1 : There \quad is \quad not \quad unit \quad root
                                                $$
                                                '''
                                                
                                                ],mathjax = True),
                                            html.Hr(),
                                            dbc.Row(
                                                dbc.Col(id = 'stationarity-test'))
                                            ],title = 'Stationarity test'),
                                        dbc.AccordionItem([
                                            
                                            html.Ul([
                                                
                                                html.Li(html.H5('Usage of general CPI data instead of  transport and food CPI for benefit movement modelling')),
                                                html.Li(html.H5('Vasicek model is associated with short rates modeling not long-term rates modeling')),
                                                html.Li(html.H5('ARIMA model identification techniques and reliability of the chosen model depend on the skill of forecaster'))
                                                ])
                                            
                                            ],title = 'Limitations'),
                                        dbc.AccordionItem([
                                            html.H5(['Implementation is being possible by a python library called ',html.A(['phew'],href = 'https://pypi.org/project/phew/')])
                                            ],title = 'Phew'),
                                        dbc.AccordionItem([
                                            html.H5(['To price trip delay insurance for formal sector workers in Malawi, a function that captures losses that can result from trip delays has been defined. The loss amount function will lead to calculation of gross rates sum which will aid in head tax calculation. To achieve that, the project applies Vasicek and ARMA(p,q) model to model evolution of interest rates and losses increase.'])
                                            ],title = 'Conclusion')
                                        
                                        ],flush = True)
                                    ],width = {'size':5,'offset':1}),
                                dbc.Col([
                                             
                                    dbc.Accordion(
                                        [
                                            dbc.AccordionItem(
                                                children = [
                                                    
                                                    dcc.Markdown([
                                                        '''
                                                        Loss amount for a year L(y) is being calculated by,
                                                        $$
                                                        L_y =\sum_{s=1}^{z} L_s * D_s
                                                         $$
                                                         , where L(s) is the average daily loss value for a specific season, given by
                                                         $$
                                                         L_s = E_y * C  * B_y * R_s
                                                         $$
                                                        '''
                                                        ],mathjax = True)
                                                    ],
                                                title="Loss amount",
                                            ),
                                            dbc.AccordionItem(
                                                children = [
                                                    
                                                    dcc.Markdown([
                                                        
                                                        '''
                                                        The benefit for each year can be given by,
                                                        $$
                                                        B_{n,y} = \prod_{i=1}^{n} x_i B_0
                                                        $$
                                                        where x(i) is CPI, OR
                                                        $$
                                                        B_{n,y} = \prod_{i=1}^{n} B_0(1 + r_i)
                                                        $$
                                                        where r(i) is inflation rate.
                                                        Both x(i) and r(i) values forecast by ARMA model,
                                                        $$
                                                        x(r)_i = \phi_0 + \sum_{i=1}^{p}\phi_i x(r)_{t-1} + \epsilon_t + \sum_{i=1}^{q} \Theta_{i} \epsilon_{t-1} 
                                                        $$
                                                        '''
                                                        ],mathjax = True)
                                                    ],
                                                title="Benefit",
                                            ),
                                            dbc.AccordionItem(
                                                children = [
                                                    
                                                    dcc.Markdown([
                                                        
                                                        '''
                                                        $$
                                                        EAR = (1 + (nominal\quad rate) / \pi)^{\pi} - 1 
                                                        $$
                                                        $$
                                                        \Delta r_t = a(b - r_{t-1})\Delta t + \epsilon_t (0,\sigma^2)
                                                        $$
                                                        '''
                                                        ],mathjax = True)
                                                    ],
                                                title="Effective rates", 
                                            ),
                                            dbc.AccordionItem(
                                                children = [
                                                    
                                                    dcc.Markdown([
                                                        
                                                        '''
                                                        $$
                                                        T = PV_{T rates} / (N* PV_{annuity})
                                                        $$
                                                        '''
                                                        ],mathjax = True)
                                                    ],
                                                title = 'Tax'
                                                ),
                                        ], 
                                        flush=True,
                                    )
                                
                                    ],width = {'size':5})
                                ]),
                            html.Br()
                            ])
                        ],width = {'size':12})
                    ])
                
                ]
        
        elif at == 'data_analysis':
            return at
    
    @app.callback([Output("datasetsOv", "children"),Output("data-graph", "figure"),Output('stationarity-test','children')], State("dropdowndf", "value"),Input('button-rowOv','n_clicks'))
    def OvData(v,n):
        
        if v == 'inflation':
            
            # loading inflation data
            inflation_rate = pd.read_csv('assets/inflationRate.csv')
            inflation_rate.columns = ['Year','Inflation rate (%)']
            inflation_rate.index = inflation_rate.Year
            inflation_rate.drop('Year',axis = 'columns',inplace = True)
            inflation_rate['Inflation rate (%)'] = [float(i) for i in inflation_rate['Inflation rate (%)']]
            inflation_rate.index = pd.to_datetime([str(int(i)) + '-12-31' for i in inflation_rate.index])
            
            table = inflation_rate['Inflation rate (%)'].describe()
            index = table.index
            table = pd.DataFrame(table)
            table['Parameter'] = index
            
            table = table[['Parameter','Inflation rate (%)']]
            
            
            df = [dbc.Row([
                            dbc.Col([
                                
                                dash_table.DataTable(id ='dashTable',columns = [
                   
                                    {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                    if i == 'year'
                                    else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                    for i in table.columns
                                    ],
                                    data = table.to_dict('records'),
                                    filter_action = 'native',
                                    editable = False,
                                    page_size = 8,
                                    sort_action = 'native',
                                    sort_mode = 'multi',
                                    row_selectable = 'single',
                                    selected_rows=[],
                                    column_selectable = 'multi',
                                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                    style_header = {'background-color':'#035efc','color':'white'})
                                
                                
                                ],width = {'size':12})
                            ])]
            
            scatter_data = [go.Scatter(x = inflation_rate.index,y = inflation_rate['Inflation rate (%)'],line = dict(color = 'green'))]
            lay = dict(title = 'Inflation rate (%) Malawi',xaxis = dict(title = 'Year'),yaxis = dict(title = 'Inflation rate (%)'))
            figure = dict(data = scatter_data,layout = lay)
            
            result = adfuller(inflation_rate['Inflation rate (%)']) # applying augmented dicky fuller test
            test_statistic,p_value = result[0],round(result[1],3)
            
            table_header = [
                html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
            ]
            
            row1 = html.Tr([html.Td("Significance value"), html.Td("0.05")])
            row2 = html.Tr([html.Td("Test statistic"), html.Td(str(test_statistic))])
            row3 = html.Tr([html.Td("P-value"), html.Td(str(p_value))])
            
            table_body = [html.Tbody([row1, row2, row3])]
            
            htable = dbc.Table(table_header + table_body, bordered=True)
            
            return df,figure ,htable
        
        elif v == 'cpi':
            
            # loading cpi data
            cpi_df = pd.read_csv('assets/cpiData.csv')
            cpi_df.index = cpi_df.Year
            cpi_df.drop('Year',axis = 'columns',inplace = True)
            cpi_df['CPI'] = [float(i) for i in cpi_df['CPI']]
            cpi_df.index = pd.to_datetime(cpi_df.index)
            
            table = cpi_df['CPI'].describe()
            index = table.index
            table = pd.DataFrame(table)
            table['Parameter'] = index
            
            table = table[['Parameter','CPI']]
            
            df = [dbc.Row([
                            dbc.Col([
                                
                                dash_table.DataTable(id ='dashTable',columns = [
                   
                                    {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                    if i == 'year'
                                    else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                    for i in table.columns
                                    ],
                                    data = table.to_dict('records'),
                                    filter_action = 'native',
                                    editable = False,
                                    page_size = 8,
                                    sort_action = 'native',
                                    sort_mode = 'multi',
                                    row_selectable = 'single',
                                    selected_rows=[],
                                    column_selectable = 'multi',
                                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                    style_header = {'background-color':'#035efc','color':'white'})
                                
                                
                                ],width = {'size':12})
                            ])]
            
            scatter_data = [go.Scatter(x = cpi_df.index,y = cpi_df['CPI'],line = dict(color = 'green'))]
            lay = dict(title = 'CPI Malawi',xaxis = dict(title = 'Year'),yaxis = dict(title = 'CPI'))
            figure = dict(data = scatter_data,layout = lay)
            
            result = adfuller(cpi_df['CPI']) # applying augmented dicky fuller test
            test_statistic,p_value = result[0],round(result[1],3)
            
            table_header = [
                html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
            ]
            
            row1 = html.Tr([html.Td("Significance value"), html.Td("0.05")])
            row2 = html.Tr([html.Td("Test statistic"), html.Td(str(test_statistic))])
            row3 = html.Tr([html.Td("P-value"), html.Td(str(p_value))])
            
            table_body = [html.Tbody([row1, row2, row3])]
            
            htable = dbc.Table(table_header + table_body, bordered=True)
            
            return df,figure,htable
        
        elif v == 'rinterest':
            
            # loading real interest rate
            real_interest = pd.read_csv('assets/realInte.csv')
            real_interest.columns = ['Year','Real interest (%)']
            real_interest.index = real_interest.Year
            real_interest.drop('Year',axis = 'columns',inplace = True)
            real_interest['Real interest (%)'] = [float(i) for i in real_interest['Real interest (%)']]
            real_interest.index = pd.to_datetime([str(int(i)) + '-12-31' for i in real_interest.index])
            
            table = real_interest['Real interest (%)'].describe()
            index = table.index
            table = pd.DataFrame(table)
            table['Parameter'] = index
            
            table = table[['Parameter','Real interest (%)']]
            
            df = [dbc.Row([
                            dbc.Col([
                                
                                dash_table.DataTable(id ='dashTable',columns = [
                   
                                    {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                    if i == 'year'
                                    else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                    for i in table.columns
                                    ],
                                    data = table.to_dict('records'),
                                    filter_action = 'native',
                                    editable = False,
                                    page_size = 8,
                                    sort_action = 'native',
                                    sort_mode = 'multi',
                                    row_selectable = 'single',
                                    selected_rows=[],
                                    column_selectable = 'multi',
                                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                    style_header = {'background-color':'#035efc','color':'white'})
                                
                                
                                ],width = {'size':12})
                            ])]
            
            scatter_data = [go.Scatter(x = real_interest.index,y = real_interest['Real interest (%)'],line = dict(color = 'green'))]
            lay = dict(title = 'Real interest (%) Malawi',xaxis = dict(title = 'Year'),yaxis = dict(title = 'Real interest (%)'))
            figure = dict(data = scatter_data,layout = lay)
            
            result = adfuller(real_interest['Real interest (%)']) # applying augmented dicky fuller test
            test_statistic,p_value = result[0],round(result[1],3)
            
            table_header = [
                html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
            ]
            
            row1 = html.Tr([html.Td("Significance value"), html.Td("0.05")])
            row2 = html.Tr([html.Td("Test statistic"), html.Td(str(test_statistic))])
            row3 = html.Tr([html.Td("P-value"), html.Td(str(p_value))])
            
            table_body = [html.Tbody([row1, row2, row3])]
            
            htable = dbc.Table(table_header + table_body, bordered=True)
            
            return df,figure,htable
        
        elif v == 'exchangerate':
            
            # loading exchange data
            exchange_df = pd.read_csv('assets/exchangeRates.csv')
            exchange_df.columns = ['Date','Buying']
            exchange_df.index = pd.to_datetime(exchange_df.Date)
            exchange_df.drop('Date',axis = 'columns',inplace = True)
            exchange_df['Buying'] = [float(i) for i in exchange_df['Buying']]
            
            table = exchange_df['Buying'].describe()
            index = table.index
            table = pd.DataFrame(table)
            table['Parameter'] = index
            
            table = table[['Parameter','Buying']]
            
            df = [dbc.Row([
                            dbc.Col([
                                
                                dash_table.DataTable(id ='dashTable',columns = [
                   
                                    {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                    if i == 'year'
                                    else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                    for i in table.columns
                                    ],
                                    data = table.to_dict('records'),
                                    filter_action = 'native',
                                    editable = False,
                                    page_size = 8,
                                    sort_action = 'native',
                                    sort_mode = 'multi',
                                    row_selectable = 'single',
                                    selected_rows=[],
                                    column_selectable = 'multi',
                                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                    style_header = {'background-color':'#035efc','color':'white'})
                                
                                
                                ],width = {'size':12})
                            ])]
            
            scatter_data = [go.Scatter(x = exchange_df.index,y = exchange_df['Buying'],line = dict(color = 'green'))]
            lay = dict(title = 'Kwacha against Dollar',xaxis = dict(title = 'Year'),yaxis = dict(title = 'Buying'))
            figure = dict(data = scatter_data,layout = lay)
            
            result = adfuller(exchange_df['Buying']) # applying augmented dicky fuller test
            test_statistic,p_value = result[0],round(result[1],3)
            
            table_header = [
                html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
            ]
            
            row1 = html.Tr([html.Td("Significance value"), html.Td("0.05")])
            row2 = html.Tr([html.Td("Test statistic"), html.Td(str(test_statistic))])
            row3 = html.Tr([html.Td("P-value"), html.Td(str(p_value))])
            
            table_body = [html.Tbody([row1, row2, row3])]
            
            htable = dbc.Table(table_header + table_body, bordered=True)
            
            return df,figure,htable
            
        
    
    @app.callback(Output("contentReplyTax", "children"), [Input("tabsTax", "active_tab")])
    def switch_tabTax(at):
        
        if at == 'aboutEf':
            
            numberef = dbc.Row(
                       [
                           dbc.Label("Prediction points", html_for="example-numberef-row", width=2),
                           dbc.Col(
                               dbc.Input(
                                   id="example-numberef-row",type = 'number' ,value=7                   ),
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )
                   
                   
            send_buttonef = dbc.Row(
                       [
                           dbc.Label("", html_for="button-rowef", width=2),
                           dbc.Col([
                               dbc.Button(
                                   id="button-rowef",children = ['Compute'],
                                   color = 'primary',
                               ),
                               dbc.Tooltip(children = [
                                   
                                   html.H6(['Effective rates'],style = {'color':'white'}),
                                   dcc.Markdown([
                                       
                                       '''
                                       $$ 
                                       \Delta r_t = a(b-r_{t-1})\Delta t + \epsilon_t (0,\sigma^2) $$
                                       '''
                                       
                                       ],mathjax = True)
                                   
                                   ],target="button-rowef",placement = 'right'),
                               dbc.Toast(
                                   "Computed",
                                   id="positioned-toastef",
                                   header="Effective rates",
                                   is_open=False,
                                   duration = 4000, 
                                   icon="success",
                                   # top: 66 positions the toast below the navbar
                                   style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                       )],
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )
                   
            return [
                       html.Br(),
                       dbc.Row([
                           dbc.Col([
                               dbc.Accordion([
                               dbc.AccordionItem(
                                   dbc.Row([
                                       
                                       dbc.Form([html.Br(),numberef,send_buttonef],style = {'border-style':'ridge'})
                                       
                                       ]), title= 'Entry'
                               ),
                               dbc.AccordionItem(id = 'resultsAccordef', title= 'Results'
                               )
                               
                               ],start_collapsed=False,id = 'accordief')
                       
                           ],width = {'size':12})
                       ])
                           ]
        
        elif at == 'tax4':
            
                   
            rates = dbc.Row(
                       [
                           dbc.Label("Rates shift()", html_for="example-ratestaX-row", width=2),
                           dbc.Col(
                               dbc.Input(
                                   id="example-ratestaX-row",type = 'text' ,value= '0.3323827058253736,0.3424981801564191,0.34727817685838286,0.34953693089433163,0.35060428932845333'),
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )
                   
            
            trates = dbc.Row(
                       [
                           dbc.Label("Total gross rates", html_for="example-trates-row", width=2),
                           dbc.Col(
                               dbc.Input(
                                   id="example-trates-row",type = 'text' ,value='100055729.4714379,127335227.5915525,166261234.4481129,206626960.5665632,263013396.75131822' ),
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )
                   
            expo = dbc.Row(
                       [
                           dbc.Label("Exposures shift()", html_for="example-expotaX-row", width=2),
                           dbc.Col(
                               dbc.Input(
                                   id="example-expotaX-row",type = 'text' ,value= '2177662.5468,2234246.7888,2291756.7114,2350073.8794,2409116.7672'                  ),
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )    
        
            yeartaX = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-yeartaX-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-yeartaX-row",type = 'number' ,value=2025
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
                   
            send_buttontaX = dbc.Row(
                       [
                           dbc.Label("", html_for="button-rowtaX", width=2),
                           dbc.Col([
                               dbc.Button(
                                   id="button-rowtaX",children = ['Compute'],
                                   color = 'primary',
                               ),
                               dbc.Tooltip(children = [
                                   
                                   html.H6(['Tax'],style = {'color':'white'}),
                                   dcc.Markdown([
                                       
                                       '''
                                       $$ 
                                       T = PV_{T rates} / (N* PV_{annuity})
                                       '''
                                       
                                       ],mathjax = True)
                                   
                                   ],target="button-rowtaX",placement = 'right'),
                               dbc.Toast(
                                   "Computed",
                                   id="positioned-toasttaX",
                                   header="Head tax",
                                   is_open=False,
                                   duration = 4000, 
                                   icon="success",
                                   # top: 66 positions the toast below the navbar
                                   style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                       )],
                               width=10,
                           ),
                       ],
                       className="mb-3",
                   )
            
            return [
                       html.Br(),
                       dbc.Row([
                           dbc.Col([
                               dbc.Accordion([
                               dbc.AccordionItem(
                                   dbc.Row([
                                       
                                       dbc.Form([html.Br(),rates,trates,expo,yeartaX,send_buttontaX],style = {'border-style':'ridge'})
                                       
                                       ]), title= 'Entry'
                               ),
                               dbc.AccordionItem(id = 'resultsAccordtaX', title= 'Results'
                               )
                               
                               ],start_collapsed=False,id = 'accordtaX')
                       
                           ],width = {'size':12})
                       ])
                           ]
        
        elif at == 'taxnot':
        
            return [
                
                html.Br(),
                dbc.Row([
                    
                    dbc.Col([
                        
                        html.Iframe(id = 'html_pricing',src = 'assets/trip delay pricing.pdf',height = '550px',width = '100%',style = {'color':'red'})
                        
                        ],width = {'size':9}),
                    dbc.Col([
                        
                        dbc.Card([
                            
                            dbc.CardHeader([
                                
                                html.H5([html.I(className = "fa-solid fa-download fa-bounce",style = {'color':'white'}),' Download'],style = {'text-align':'center','color':'white','font-weight':'bold'})
                                ],style = {'background-color':'#035efc'}),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id ='notebuttax',children = ['N'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Notebook",
                                                target="notebuttax",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'taxnoteD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            html.Br(),
                            html.Br()
                            
                            ])
                        
                        ],width = {'size':3})
                    
                    ])
                
                ]
    
    @app.callback(Output("contentReplyPremium", "children"), [Input("tabsPremium", "active_tab")])
    def switch_tabpremium(at):
        
        if at == 'pureP':
            
            RatioF = dbc.Row(
                [
                    dbc.Label("Ratio, 2", html_for="example-fratio-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-fratio-row",type = 'text' ,value='0.13,0.13,0.13,0.13,0.13,0.13'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            RatioE2 = dbc.Row(
                [
                    dbc.Label("Ratio, 1", html_for="example-eratio-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-eratio-row",type = 'text' ,value='0.78,0.78,0.78,0.78,0.78,0.78'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            pop_data = dbc.Row(
                [
                    dbc.Label("Population", html_for="example-pop-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-pop-row",type = 'text', value='21475962,22033992,22601151,23176271,23758548,24347875'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            year3 = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-year3-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-year3-row",type = 'number' ,value=2024
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            send_button3 = dbc.Row(
                [
                    dbc.Label("", html_for="button-row3", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-row3",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(children = [
                            
                            html.H6(['Exposures'],style = {'color':'white'}),
                            dcc.Markdown([
                                
                                '''
                                $$
                                ratio*ratio2*pop
                                 $$
                                '''
                                
                                ],mathjax = True)
                            
                            ],target="button-row3",placement = 'right'),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toast3",
                            header="Exposures",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            losses_p = dbc.Row(
                [
                    dbc.Label("Losses", html_for="example-losses-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-losses-row",type = 'text' ,value='62893815.09375922,82662758.65861861,111144024.80776481,139765324.61015093,177976015.6661491'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            exposures_p = dbc.Row(
                [
                    dbc.Label("Exposures", html_for="example-expo-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-expo-row",type = 'text' ,value='2177662.5468,2234246.7888,2291756.7114,2350073.8794,2409116.7672'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            year4 = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-year4-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-year4-row",type = 'number' ,value=2025
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            send_button4 = dbc.Row(
                [
                    dbc.Label("", html_for="button-row4", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-row4",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(children = [
                            
                            html.H6(['Pure Premium'],style = {'color':'white'}),
                            dcc.Markdown([
                                
                                '''
                                $$
                                loss / exposures
                                 $$
                                '''
                                
                                ],mathjax = True)
                            
                            ],target="button-row4",placement = 'right'),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toast4",
                            header="Pure premium",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            return  [
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Accordion([
                                dbc.AccordionItem(
                                    dbc.Row([
                                        dbc.Accordion([
                                            
                                            dbc.AccordionItem(dbc.Row([
                                                                
                                                                dbc.Form([html.Br(),RatioE2,RatioF,pop_data,year3,send_button3],style = {'border-style':'ridge'})
                                                                
                                                                ]),title= 'Entry'),
                                            dbc.AccordionItem(id = 'exposures_results',title= 'Results')
                                            
                                            ])
                                        ]), title= 'Exposures'
                                    ),
                         dbc.AccordionItem(
                             dbc.Row([
                                 dbc.Accordion([
                                     
                                     dbc.AccordionItem(dbc.Row([
                                                         
                                                         dbc.Form([html.Br(),losses_p,exposures_p,year4,send_button4],style = {'border-style':'ridge'})
                                                         
                                                         ]),title= 'Entry'),
                                     dbc.AccordionItem(id = 'pure_results',title= 'Results')
                                     
                                     ])
                                 ]), title= 'Pure premium'
                             )
    
    
                            
                            ],start_collapsed=False,id = 'accordipremium')
                    
                        ],width = {'size':12})
                     ])
                         ]
        
        elif at == 'exchP':
            
            return [
                
                html.Br(),
                dbc.Row([
                    
                    dbc.Col([
                        
                        html.Iframe(id = 'html_exchange',src = 'assets/fe_forecast.pdf',height = '550px',width = '100%',style = {'color':'red'})
                        
                        ],width = {'size':9}),
                    dbc.Col([
                        
                        dbc.Card([
                            
                            dbc.CardHeader([
                                
                                html.H5([html.I(className = "fa-solid fa-download fa-bounce",style = {'color':'white'}),' Download'],style = {'text-align':'center','color':'white','font-weight':'bold'})
                                ],style = {'background-color':'#035efc'}),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id ='notebutex',children = ['N'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Notebook",
                                                target="notebutex",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'exchnoteD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'databutex',children = ['D'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Data",
                                                target="databutex",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'exchdataD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'forecastbutex',children = ['F'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Forecasts",
                                                target="forecastbutex",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'exchforecastD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            html.Br()
                            
                            ])
                        
                        ],width = {'size':3})
                    
                    ])
                
                ]
        
        elif at == 'grossP':
            return [
                
                
                dbc.Row([
                    
                    
                    dbc.Col(id = 'grossPage',width = {'size':10}),
                    dbc.Col([
                        
                        html.Br(),
                        dcc.Tabs(
                            [
                                dcc.Tab(label="Fund growth", value="fundid2",id = 'fundtab2',style = {'background-color':'#035efc','color':'white'}),
                                dcc.Tab(label="Expense ratio", value="exchid",id = 'exchtab',style = {'background-color':'#035efc','color':'white'}),
                                dcc.Tab(label="Gross rate", value="grossrid",id = 'grossrtab',style = {'background-color':'#035efc','color':'white'})
    
                                ],
                            id="tabsgross",
                            vertical = True,
                            value = 'fundid2'),
                        dbc.Tooltip(
                                    "Evolution of fund",
                                    target="fundtab2",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "Foreign exchange conversion",
                                    target="exchtab",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "Gross rate computation",
                                    target="grossrtab",
                                    placement = 'top'
                                )
            
                        ],width = {'size':2})
                    
                    ])
                
                ]
    
    @app.callback(Output("contentReplyLoss", "children"), [Input("tabsLoss", "active_tab")])
    def switch_tabloss(at):
        
        if at == "inflP":
            
            return [
                
                html.Br(),
                dbc.Row([
                    
                    dbc.Col([
                        
                        html.Iframe(id = 'html_infla',src = 'assets/Inflation_forecast.pdf',height = '550px',width = '100%')
                        
                        ],width = {'size':9}),
                    dbc.Col([
                        
                        dbc.Card([
                            
                            dbc.CardHeader([
                                
                                html.H5([html.I(className = "fa-solid fa-download fa-bounce",style = {'color':'white'}),' Download'],style = {'text-align':'center','color':'white','font-weight':'bold'})
                                ],style = {'background-color':'#035efc'}),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id ='notebut2',children = ['N'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Notebook",
                                                target="notebut2",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'inflanoteD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'databut2',children = ['D'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Data",
                                                target="databut2",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'infladataD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'forecastbut2',children = ['F'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Forecasts",
                                                target="forecastbut2",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'inflaforecastD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            html.Br()
                            
                            ])
                        
                        ],width = {'size':3})
                    
                    ])
                
                ]
        
        elif at == "cpiP":
            
            return [
                
                html.Br(),
                dbc.Row([
                    
                    dbc.Col([
                        
                        html.Iframe(id = 'html_cpi',src = 'assets/cpi_forecast.pdf',height = '550px',width = '100%',style = {'color':'red'})
                        
                        ],width = {'size':9}),
                    dbc.Col([
                        
                        dbc.Card([
                            
                            dbc.CardHeader([
                                
                                html.H5([html.I(className = "fa-solid fa-download fa-bounce",style = {'color':'white'}),' Download'],style = {'text-align':'center','color':'white','font-weight':'bold'})
                                ],style = {'background-color':'#035efc'}),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id ='notebut',children = ['N'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Notebook",
                                                target="notebut",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'cpinoteD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'databut',children = ['D'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Data",
                                                target="databut",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'cpidataD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            dbc.Row([
                                
                                dbc.Col([
                                    dbc.Button(id = 'forecastbut',children = ['F'],style = {'border-radius':'100%','height':'40px'}),
                                    dbc.Tooltip(
                                                "Forecasts",
                                                target="forecastbut",
                                                placement = 'right'
                                            ),
                                    dcc.Download(id = 'cpiforecastD')
                                    ],width = {'size':3,'offset':5})
                                ]),
                            html.Br(),
                            html.Br()
                            
                            ])
                        
                        ],width = {'size':3})
                    
                    ])
                
                ]
        
        elif at == "lossP":
            
            return [
                
                
                dbc.Row([
                    
                    
                    dbc.Col(id = 'lossPage',width = {'size':10}),
                    dbc.Col([
                        
                        html.Br(),
                        dcc.Tabs(
                            [
                                dcc.Tab(label="Fund growth", value="fundid",id = 'fundtab',style = {'background-color':'#035efc','color':'white'}),
                                dcc.Tab(label="Losses", value="lossid",id = 'losstab',style = {'background-color':'#035efc','color':'white'})
                                ],
                            id="tabsloss",
                            vertical = True,
                            value = 'fundid'),
                        dbc.Tooltip(
                                    "Evolution of fund",
                                    target="fundtab",
                                    placement = 'top'
                                ),
                        dbc.Tooltip(
                                    "losses computation",
                                    target="losstab",
                                    placement = 'top'
                                )
            
                        ],width = {'size':2})
                    
                    ])
                
                ]
        
        return html.P("This shouldn't ever be displayed...")
    
    
    @app.callback(Output("grossPage", "children"), [Input("tabsgross", "value")])
    def switch_tab6(at):
        
        if at == 'fundid2':
            
            amountg = dbc.Row(
                [
                    dbc.Label("Amount, B(0)", html_for="example-amountg-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-amountg-row",type = 'number' ,value=950                    ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            growth_datag = dbc.Row(
                [
                    dbc.Label("Data, r/x", html_for="example-growthg-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-growthg-row",type = 'text', value='0.024,0.023,0.023,0.023,0.023,0.023'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            infVscpig = dbc.Row(
                           [
                               dbc.Label("Method", html_for="dropdownVsg",width = 2,id = 'methodlabelg'),
                               dbc.Col(
                                   dcc.Dropdown(
                                   id="dropdownVsg",
                                   value = 'inflation',
                                   options=[
                                       {"label": "inflation", "value": 'inflation'},
                                       {"label": "cpi", "value": 'cpi'},
                                   ],
                               ),width = 10),
                           ],
                           className="mb-3",
                           )
            
            yearg = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-yearg-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-yearg-row",type = 'number' ,value=2024
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            send_buttong = dbc.Row(
                [
                    dbc.Label("", html_for="button-rowg", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-rowg",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(id = 'markgrmethodg',target="button-rowg",placement = 'right'),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toastg",
                            header="Price forecast",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            return [
                
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion([
                        dbc.AccordionItem(
                            dbc.Row([
                                
                                dbc.Form([html.Br(),amountg,growth_datag,infVscpig,yearg,send_buttong],style = {'border-style':'ridge'})
                                
                                ]), title= 'Entry'
                        ),
                        dbc.AccordionItem(id = 'resultsAccordg', title= 'Results'
                        )
                        
                        ],start_collapsed=False,id = 'accordifundg')
                
                    ],width = {'size':12})
                ])
                    ]
        
        elif at == 'exchid':
            
            priceexr = dbc.Row(
                [
                    dbc.Label("Price (USD)", html_for="example-priceexr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-priceexr-row",type = 'text', value='972.8000000000001,995.1744,1018.0634112,1041.4788696576,1065.4328836597247'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            lossexr = dbc.Row(
                [
                    dbc.Label("Loss", html_for="example-lossexr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-lossexr-row",type = 'text', value='62002220.43453912,82883444.89454933,109881851.99929053,141138595.29511133,176552466.36796507'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            yearexr = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-yearexr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-yearexr-row",type = 'number' ,value=2025
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
        
            
            send_buttonexr = dbc.Row(
                [
                    dbc.Label("", html_for="button-rowexr", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-rowexr",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(id = 'markgrmethodexr',target="button-rowexr",placement = 'right',
                                    children = [html.H6(['Expense ratio'],style = {'color':'white'}),
                                    dcc.Markdown([
                                        
                                        '''
                                        $$
                                        ER_y = T_y/L_y
                                         $$
                                        '''
                                        
                                        ],mathjax = True)]
                                    ),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toastexr",
                            header="Expense ratios",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            return [
                
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion([
                        dbc.AccordionItem(
                            dbc.Row([
                                
                                dbc.Form([html.Br(),priceexr,lossexr,yearexr,send_buttonexr],style = {'border-style':'ridge'})
                                
                                ]), title= 'Entry'
                        ),
                        dbc.AccordionItem(id = 'resultsAccordexr', title= 'Results'
                        )
                        
                        ],start_collapsed=False,id = 'accordiexr')
                
                    ],width = {'size':12})
                ])
                    ]
        
        elif at == 'grossrid':
            
            ratiogr = dbc.Row(
                [
                    dbc.Label("Ratio", html_for="example-ratiogr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-ratiogr-row",type = 'text', value='0.3714121577444199,0.3508256888363034,0.33150968608710263,0.32358621436951024,0.3233195804302425'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            premiumgr = dbc.Row(
                [
                    dbc.Label("Pure premium", html_for="example-premiumgr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-premiumgr-row",type = 'text', value='28.881341228088576,36.99804295254969,48.497305257096244,59.472736510664326,73.87604373905131'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            exposuresgr = dbc.Row(
                [
                    dbc.Label("Exposures", html_for="example-exposuresgr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-exposuresgr-row",type = 'text', value='2177662.5468,2234246.7888,2291756.7114,2350073.8794,2409116.7672'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            yeargr = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-yeargr-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-yeargr-row",type = 'number' ,value=2025
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
        
            
            send_buttongr = dbc.Row(
                [
                    dbc.Label("", html_for="button-rowgr", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-rowgr",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(id = 'markgrmethodgr',target="button-rowgr",placement = 'right',
                                    children = [html.H6(['Gross rate'],style = {'color':'white'}),
                                    dcc.Markdown([
                                        
                                        '''
                                        $$
                                        Gr = Pp/(1 - Er)
                                         $$
                                        '''
                                        
                                        ],mathjax = True)]
                                    ),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toastgr",
                            header="Gross rate",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            return [
                
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion([
                        dbc.AccordionItem(
                            dbc.Row([
                                
                                dbc.Form([html.Br(),ratiogr,premiumgr,exposuresgr,yeargr,send_buttongr],style = {'border-style':'ridge'})
                                
                                ]), title= 'Entry'
                        ),
                        dbc.AccordionItem(id = 'resultsAccordrt', title= 'Results'
                        )
                        
                        ],start_collapsed=False,id = 'accordirt')
                
                    ],width = {'size':12})
                ])
                    ]
    
    @app.callback(Output("lossPage", "children"), [Input("tabsloss", "value")])
    def switch_tab5(at):
        
        if at == 'fundid':
            
            
            amount = dbc.Row(
                [
                    dbc.Label("Amount, B(0)", html_for="example-amount-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-amount-row",type = 'number' ,value=3500
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            growth_data = dbc.Row(
                [
                    dbc.Label("Data, r/x", html_for="example-growth-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-growth-row",type = 'text', value='0.20953967,0.30158578,0.10904419,0.28428562,0.15508666,0.15486050'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            infVscpi = dbc.Row(
                           [
                               dbc.Label("Method", html_for="dropdownVs",width = 2,id = 'methodlabel'),
                               dbc.Col(
                                   dcc.Dropdown(
                                   id="dropdownVs",
                                   value = 'inflation',
                                   options=[
                                       {"label": "inflation", "value": 'inflation'},
                                       {"label": "cpi", "value": 'cpi'},
                                   ],
                               ),width = 10),
                           ],
                           className="mb-3",
                           )
            
            year = dbc.Row(
                [
                    dbc.Label("Start year", html_for="example-year-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-year-row",type = 'number' ,value=2024
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            send_button = dbc.Row(
                [
                    dbc.Label("", html_for="button-row", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-row",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(id = 'markgrmethod',target="button-row",placement = 'right'),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toast",
                            header="Fund growth",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            return [
                
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion([
                        dbc.AccordionItem(
                            dbc.Row([
                                
                                dbc.Form([html.Br(),amount,growth_data,infVscpi,year,send_button],style = {'border-style':'ridge'})
                                
                                ]), title= 'Entry'
                        ),
                        dbc.AccordionItem(id = 'resultsAccord', title= 'Results'
                        )
                        
                        ],start_collapsed=False,id = 'accordifund')
                
                    ],width = {'size':12})
                ])
                    ]
        
        elif at == 'lossid':
            
            
            year2 = dbc.Row(
                [
                    dbc.Label("Year", html_for="example-year2-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-year2-row",type = 'number' ,value=2025
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            benefit = dbc.Row(
                [
                    dbc.Label("Benefit, B(y)", html_for="example-benefit-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-benefit-row",type = 'number', value=5510.118721862624
    
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            days = dbc.Row(
                [
                    dbc.Label("Days, D(s)", html_for="example-days-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-days-row",type = 'text', value='365'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            delays = dbc.Row(
                [
                    dbc.Label("Delays, R(s)", html_for="example-delays-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-delays-row",type = 'text', value='7'
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            ratio = dbc.Row(
                [
                    dbc.Label("Ratio, E(y)", html_for="example-ratio-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-ratio-row",type = 'number', value=0.1
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            capacity = dbc.Row(
                [
                    dbc.Label("Capacity, C", html_for="example-capacity-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            id="example-capacity-row",type = 'number', value=50
                        ),
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            send_button2 = dbc.Row(
                [
                    dbc.Label("", html_for="button-row2", width=2),
                    dbc.Col([
                        dbc.Button(
                            id="button-row2",children = ['Compute'],
                            color = 'primary',
                        ),
                        dbc.Tooltip(children = [
                            
                            html.H6(['Yearly Loss'],style = {'color':'white'}),
                            dcc.Markdown([
                                
                                '''
                                $$
                                L_y =\sum_{s=1}^{z} L_s * D_s
                                 $$
                                '''
                                
                                ],mathjax = True)
                            
                            ],target="button-row2",placement = 'right'),
                        dbc.Toast(
                            "Computed",
                            id="positioned-toast2",
                            header="Loss amount",
                            is_open=False,
                            duration = 4000, 
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                )],
                        width=10,
                    ),
                ],
                className="mb-3",
            )
            
            
            return  [
                
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Accordion([
                        dbc.AccordionItem(
                            dbc.Row([
                                
                                dbc.Form([html.Br(),year2,benefit,days,delays,ratio,capacity,send_button2],style = {'border-style':'ridge'})
                                
                                ]), title= 'Entry'
                        ),
                        dbc.AccordionItem(id = 'resultsAccord2', title= 'Results'
                        )
                        
                        ],start_collapsed=False,id = 'accordiloss')
                
                    ],width = {'size':12})
                ])
                    ]
        
        
    @app.callback(Output('resultsAccordtaX','children'),State('example-ratestaX-row', 'value'),State('example-trates-row', 'value'),State('example-expotaX-row', 'value'),State('example-yeartaX-row', 'value'),Input('button-rowtaX', 'n_clicks'))
    def resultsAccordFuntaX(r,t,e,y,n):      
        
        rates = np.array([float(i) for i in r.split(',')])
        trates= np.array([float(i) for i in t.split(',')])
        expo = np.array([float(i) for i in e.split(',')])
        
        year = list(range(y,y + len(rates)))
        
        pv_total_premium = pd.DataFrame({'Year':year,'Total gross rates':trates,'Rates shift()':rates})
        
        # defining pv gross rate column
        pv_total_premium['PV gross rates, year(-1)'] = pv_total_premium.apply(lambda col:Time_value.present_value(col['Total gross rates'],col['Rates shift()'],1),axis = 'columns')
        
        # defining pv annuity certain column
        pv_total_premium['PV annuity certain(1), year(-1)'] = pv_total_premium.apply(lambda col:Annuity(interest_rate = col['Rates shift()']/12,number_of_terms = 12,amount = 1).certain_present_value(),axis = 'columns')
        
        pv_total_premium['Exposures shift()'] = expo 
        
        tax_df = pv_total_premium
        
        # defining tax column(1), calculating tax
        tax_df['Tax, year(-1)'] = tax_df['PV gross rates, year(-1)'] / (tax_df['Exposures shift()'] * tax_df['PV annuity certain(1), year(-1)'])
        
        tax_df = tax_df[['Year','PV gross rates, year(-1)','PV annuity certain(1), year(-1)','Tax, year(-1)']]
        
        rowadd = pd.DataFrame({'Year':[y-1],'PV gross rates, year(-1)':np.nan,'PV annuity certain(1), year(-1)':np.nan,'Tax, year(-1)':np.nan})
        
        tax_df = pd.concat([rowadd,tax_df]) 
        
        # defining tax column(2), calculating tax
        tax_df['Tax'] = tax_df['Tax, year(-1)'].shift(-1)
        
        return  dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in tax_df.columns
                                ],
                                data = tax_df.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 5,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])     
        
    @app.callback(Output('resultsAccordef','children'),State('example-numberef-row', 'value'),Input('button-rowef', 'n_clicks'))
    def resultsAccordFuncef(ne,n):      
        # loading real interest rate
        real_interest = pd.read_csv('assets/realInte.csv')
        real_interest.columns = ['Year','Real interest (%)']
        real_interest.index = real_interest.Year
        real_interest.drop('Year',axis = 'columns',inplace = True)
        real_interest['Real interest (%)'] = [float(i) for i in real_interest['Real interest (%)']]
        
        # loading inflation data
        inflation_rate = pd.read_csv('assets/inflationRate.csv')
        inflation_rate.columns = ['Year','Inflation rate (%)']
        inflation_rate.index = inflation_rate.Year
        inflation_rate.drop('Year',axis = 'columns',inplace = True)
        inflation_rate['Inflation rate (%)'] = [float(i) for i in inflation_rate['Inflation rate (%)']]
        
        # joining real interest and inflation dataframe
        rates = real_interest.join([inflation_rate])
        
        # defining norminal interest rate column
        rates['Norminal rate (%)'] = rates.apply(lambda col: Interest_rates.compute.nominal_interest_rate(col['Real interest (%)'],col['Inflation rate (%)']),axis = 'columns')
        
        # defining effective rate column
        rates['Effective rate'] = rates.apply(lambda col: Interest_rates.compute.effective_interest_rate(col['Norminal rate (%)']/100,12),axis = 'columns')
        
        effective_rates = list(rates['Effective rate'].values)
        
        # using vasicek interest rate model to model evolution of effective rates
        vasicek = Interest_rates.vasicek(data = effective_rates,number_of_prediction_points = ne)
        
        # fitting model
        vasicek.fit()
        
        expected_effective_rates = pd.DataFrame({'Year': list(range(2023,2023 + len(vasicek.expectation()))),'Rates':vasicek.expectation()})
        
        return  dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in expected_effective_rates.columns
                                ],
                                data = expected_effective_rates.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 5,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])    
        
        
    @app.callback(Output('resultsAccordrt','children'),State('example-ratiogr-row', 'value'),State('example-premiumgr-row', 'value'),State('example-exposuresgr-row', 'value'),State('example-yeargr-row', 'value'),Input('button-rowgr', 'n_clicks'))
    def resultsAccordFuncrt(r,p,e,y,n):      
        
        ratio = np.array([float(i) for i in r.split(',')])
        pre = np.array([float(i) for i in p.split(',')])
        exp = np.array([float(i) for i in e.split(',')])
    
        year = list(range(y,y + len(ratio)))
        
        gross_rate_df = pd.DataFrame({'Year':year,'Ratio':ratio,'Pure premium':pre})
        
        # defining gross rate column
        gross_rate_df['Gross rate'] = gross_rate_df.apply(lambda col: Premium.gross_rate(pure_premium= col['Pure premium'],expense_ratio= col['Ratio']),axis = 'columns')
        gross_rate_df['Exposures shift()'] = exp
        
        # defining total gross rates column
        gross_rate_df['Total gross rates'] = gross_rate_df.apply(lambda col: Premium.gross_premium(col['Gross rate'],col['Exposures shift()']),axis = 'columns')
        
        gross_rate_df = gross_rate_df[['Year','Gross rate','Total gross rates']]
        
        return  dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in gross_rate_df.columns
                                ],
                                data = gross_rate_df.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 5,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])    
        
        
    
    @app.callback(Output('resultsAccordexr','children'),State('example-priceexr-row', 'value'),State('example-lossexr-row', 'value'),State('example-yearexr-row', 'value'),Input('button-rowexr', 'n_clicks'))
    def resultsAccordFuncexr(p,l,y,n):      
        
        price = np.array([float(i) for i in p.split(',')])
        loss = np.array([float(i) for i in l.split(',')])
        
        year = list(range(y,y + len(price)))
        
        price_df = pd.DataFrame({'Price':price},index = year)
    
        exchange_forecast = pd.read_csv('assets/exchange_forecast.csv')
        exchange_forecast.columns = ['Date','Buying']
        exchange_forecast.index = exchange_forecast.Date
        
        exchange_forecast.index = pd.to_datetime(exchange_forecast.index)
        
        exchange_forecast.drop('Date',axis = 'columns',inplace = True)
        
        exchange_forecast = exchange_forecast.loc[(exchange_forecast.index >= '2025-01-01')]
        
        # assuming payment for the service will be made on first day of every month
        exchange_forecast = exchange_forecast.loc[exchange_forecast.index.day == 1]
        
        # defining cost function
        cost = exchange_forecast
        
        # defining cost column to capture expenses made on the first day of every month
        cost['Cost'] = [np.nan for i in cost.index]
        
        # calculating the expenses by multplying the cost in usd dollars by the price of one us dollar as at that particular date
        for i in cost.index.year.unique():
            for x in cost.loc[cost.index.year == i].index:
                cost.loc[cost.index == str(x).split(' ')[0],'Cost'] = cost.loc[cost.index == str(x).split(' ')[0],'Buying'].values[0] * price_df.loc[price_df.index == (i,),'Price'].values[0]
        
        
        # defining year column
        cost['Year'] = cost.index.year
        
        # calculating total cost by year
        cost_by_year = cost.groupby('Year').sum('Cost')
        cost_by_year['Year'] = year
        
        cost_by_year = cost_by_year[['Year','Cost']]
        
        # loading original exchange data
        exchange_obs = pd.read_csv('assets/exchangesti.csv')
        
        # standard dev of the values of usd dollar against kwacha from 2012 to 2024, to help in correcting the forecast
        std = round(exchange_obs.Buying.std())
        
        cost_by_year['Price'] = price
        cost_by_year['Loss'] = loss
        
        # defining norminal interest rate column
        cost_by_year['Ratio'] = cost_by_year.apply(lambda col: Expenses(mean_expenses= col['Cost'],variance_expenses= std * col['Price'] * 12,fund_amount= col['Loss']).montecarlo(alpha = 5,number_of_replications = 1000)['optimal_ratio'],axis = 'columns')
        
        return [dbc.Row([
                       dbc.Col([
                           
                           dash_table.DataTable(id ='dashTable',columns = [
              
                               {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                               if i == 'year'
                               else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                               for i in cost_by_year.columns
                               ],
                               data = cost_by_year.to_dict('records'),
                               filter_action = 'native',
                               editable = False,
                               page_size = 5,
                               sort_action = 'native',
                               sort_mode = 'multi',
                               row_selectable = 'single',
                               selected_rows=[],
                               column_selectable = 'multi',
                               style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                               style_header = {'background-color':'#035efc','color':'white'})
                           
                           
                           ],width = {'size':12})
                       ])]
    
    @app.callback(Output('pure_results','children'),State('example-losses-row', 'value'),State('example-expo-row', 'value'),State('example-year4-row', 'value'),Input('button-row4', 'n_clicks'))
    def resultsAccordFunc4(l,e,y,n):      
        
        loss = np.array([float(i) for i in l.split(',')])
        expo = np.array([float(i) for i in e.split(',')])
        
        pure_pr =  loss / expo
        year = list(range(y,y + len(loss)))
        
        table_pure = pd.DataFrame({'Year':year,'Pure premium':pure_pr})
        
        return  dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_pure.columns
                                ],
                                data = table_pure.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 5,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])    
        
        
    @app.callback(Output('exposures_results','children'),State('example-eratio-row', 'value'),State('example-fratio-row', 'value'),State('example-pop-row', 'value'),State('example-year3-row', 'value'),Input('button-row3', 'n_clicks'))
    def resultsAccordFunc3(e,f,p,y,n):      
        
        emp = np.array([float(i) for i in e.split(',')])
        form = np.array([float(i) for i in f.split(',')])
        pop = np.array([float(i) for i in p.split(',')])
        
        exp =  emp * form * pop
        year = list(range(y,y + len(emp)))
        
        table_exp = pd.DataFrame({'Year':['31-12-{}'.format(i) for i in year],'Exposures':exp})
        
        return  dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_exp.columns
                                ],
                                data = table_exp.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 5,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])
        
        
    @app.callback(Output('resultsAccord2','children'),State('example-year2-row', 'value'),State('example-benefit-row', 'value'),State('example-days-row', 'value'),State('example-delays-row', 'value'),State('example-ratio-row', 'value'),State('example-capacity-row', 'value'),Input('button-row2', 'n_clicks'))
    def resultsAccordFunc2(y,b,d,d2,r,c,n):  
         
        days = [float(i) for i in d.split(',')]
        delays = [float(i) for i in d2.split(',')]
        
        loss = lgd(number_of_days = days,ratio_of_workers_to_population = r,carrying_capacity = c,benefit = b,expected_daily_delays_in_a_season = delays)
        daily_loss_obj = loss.daily_loss_compute(1000)
        
        table_daily_loss = pd.DataFrame(set(daily_loss_obj['expected_daily_loss'].items()),columns = ['Season','Average daily Loss'])
        table_daily_claims = pd.DataFrame(set(loss.expected_claims(time_frame = 'day').items()),columns = ['Season','Average daily Claims'])
        table_seasonal_loss = pd.DataFrame(set(loss.seasonal_loss_compute(loss.expected_daily_loss_in_season).items()),columns = ['Season','Loss'])  
        table_seasonal_claims = pd.DataFrame(set(loss.expected_claims(time_frame = 'season').items()),columns = ['Season','Claims'])
        
        loss_year = pd.DataFrame(loss.yearly_loss_compute(loss.expected_seasonal_loss).items(),columns = ['year','Loss']).Loss.values[0]
        claims_year = pd.DataFrame(set(loss.expected_claims(time_frame = 'year').items()),columns = ['Season','Claims']).Claims.values[0]
        
        table_year = pd.DataFrame({'Yearly Loss':[loss_year],'Yearly Claims':[claims_year]})
        
        return [
            
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_daily_loss.columns
                                ],
                                data = table_daily_loss.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ]),
            html.Br(),
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_daily_claims.columns
                                ],
                                data = table_daily_claims.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ]),
            html.Br(),
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_seasonal_loss.columns
                                ],
                                data = table_seasonal_loss.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ]),
            html.Br(),
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_seasonal_claims.columns
                                ],
                                data = table_seasonal_claims.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ]),
            html.Br(),
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTable',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_year.columns
                                ],
                                data = table_year.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ])
            
            ]
        
        
    @app.callback(Output('resultsAccord','children'),State('example-amount-row', 'value'),State('example-growth-row', 'value'),State('dropdownVs', 'value'),State('example-year-row', 'value'),Input('button-row', 'n_clicks'))
    def resultsAccordFunc(am,gr,d,y,n):
        
        growthdataList = [float(i) for i in gr.split(',')]
        
        benefit_amounts = Cola(initial_fund = am,data = growthdataList,method = d).fund_growth()
        
        year = list(range(y,y + len(growthdataList)))
        
        table_rates = pd.DataFrame({'Year' : ['31-12-{}'.format(i) for i in year],d:growthdataList})
        table_rates.index = pd.to_datetime(table_rates.index)
        
        table_benefits = pd.DataFrame({'Year' : ['31-12-{}'.format(i) for i in year],'Benefit':benefit_amounts})
        table_benefits.index = pd.to_datetime(table_benefits.index)
        
        return  [dbc.Row([
                    dbc.Col([
                        
                        dash_table.DataTable(id ='dashTable',columns = [
           
                            {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                            if i == 'year'
                            else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                            for i in table_benefits.columns
                            ],
                            data = table_benefits.to_dict('records'),
                            filter_action = 'native',
                            editable = False,
                            page_size = 2,
                            sort_action = 'native',
                            sort_mode = 'multi',
                            row_selectable = 'single',
                            selected_rows=[],
                            column_selectable = 'multi',
                            style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                            style_header = {'background-color':'#035efc','color':'white'})
                        
                        
                        ],width = {'size':12})
                    ]),
                 dbc.Row([
                         
                       dbc.Col([
                              dcc.Graph(id =  'growthvaluesGraph',style = {'border-style':'ridge'},figure = dict(data = [dict(x = table_rates.Year,y = table_rates[d],type = 'scatter')],layout = dict(title = '{} values'.format(d),xaxis = dict(title = 'Year'),yaxis = dict(title = d))))
                             ],width = {'size':6}),
                       dbc.Col([
                             dcc.Graph(id =  'fundgrowthGraph',style = {'border-style':'ridge'},figure = dict(data = [dict(x = table_benefits.Year,y = table_benefits.Benefit,type = 'scatter',line = dict(color = 'purple'))],layout = dict(title = 'benefit growth',xaxis = dict(title = 'Year'),yaxis = dict(title = 'benefit'))))
                             ],width = {'size':6})
                         
                         ])]
    
    
    
    @app.callback(Output('resultsAccordg','children'),State('example-amountg-row', 'value'),State('example-growthg-row', 'value'),State('dropdownVsg', 'value'),State('example-yearg-row', 'value'),Input('button-rowg', 'n_clicks'))
    def resultsAccordFuncg(am,gr,d,y,n):
        
        growthdataList = [float(i) for i in gr.split(',')]
        
        benefit_amounts = Cola(initial_fund = am,data = growthdataList,method = d).fund_growth()
        
        year = list(range(y,y + len(growthdataList)))
        
        table_rates = pd.DataFrame({'Year' : ['31-12-{}'.format(i) for i in year],d:growthdataList})
        table_rates.index = pd.to_datetime(table_rates.index)
        
        table_price = pd.DataFrame({'Year' : ['31-12-{}'.format(i) for i in year],'Price':benefit_amounts})
        table_price.index = pd.to_datetime(table_price.index)
        
        table_price_refined = pd.DataFrame({'Year': list(range(y + 1,y + len(growthdataList))),'Price (ref)':table_price.Price.shift().dropna().values})
        
        return  [dbc.Row([
                    dbc.Col([
                        
                        dash_table.DataTable(id ='dashTableg',columns = [
           
                            {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                            if i == 'year'
                            else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                            for i in table_price.columns
                            ],
                            data = table_price.to_dict('records'),
                            filter_action = 'native',
                            editable = False,
                            page_size = 2,
                            sort_action = 'native',
                            sort_mode = 'multi',
                            row_selectable = 'single',
                            selected_rows=[],
                            column_selectable = 'multi',
                            style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                            style_header = {'background-color':'#035efc','color':'white'})
                        
                        
                        ],width = {'size':12})
                    ]),
            html.Br(),
            dbc.Row([
                        dbc.Col([
                            
                            dash_table.DataTable(id ='dashTableg2',columns = [
               
                                {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                                if i == 'year'
                                else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                                for i in table_price_refined.columns
                                ],
                                data = table_price_refined.to_dict('records'),
                                filter_action = 'native',
                                editable = False,
                                page_size = 2,
                                sort_action = 'native',
                                sort_mode = 'multi',
                                row_selectable = 'single',
                                selected_rows=[],
                                column_selectable = 'multi',
                                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95},
                                style_header = {'background-color':'#035efc','color':'white'})
                            
                            
                            ],width = {'size':12})
                        ]),
            ]
    
    
    @app.callback(
        Output("markgrmethodg", "children"),
        [Input("dropdownVsg", "value")],
    )
    def methodMarkg(v):
        
        if v == 'cpi':
            
            return [
                
                html.H6(['CPI method'],style = {'color':'white'}),
                dcc.Markdown([
                    
                    '''
                    $$
                    B_{n,y} = \prod_{i=1}^{n} x_i B_0
                     $$
                    '''
                    
                    ],mathjax = True)
                
                ]
        
        elif v == 'inflation':
            
            return [
                
                html.H6(['Inflation method'],style = {'color':'white'}),
                dcc.Markdown([
                    
                    '''
                    $$
                    B_{n,y} = \prod_{i=1}^{n} B_0(1 + r_i)
                     $$
                    '''
                    
                    ],mathjax = True)
                
                ]
    
    
    @app.callback(
        Output("markgrmethod", "children"),
        [Input("dropdownVs", "value")],
    )
    def methodMark(v):
        
        if v == 'cpi':
            
            return [
                
                html.H6(['CPI method'],style = {'color':'white'}),
                dcc.Markdown([
                    
                    '''
                    $$
                    B_{n,y} = \prod_{i=1}^{n} x_i B_0
                     $$
                    '''
                    
                    ],mathjax = True)
                
                ]
        
        elif v == 'inflation':
            
            return [
                
                html.H6(['Inflation method'],style = {'color':'white'}),
                dcc.Markdown([
                    
                    '''
                    $$
                    B_{n,y} = \prod_{i=1}^{n} B_0(1 + r_i)
                     $$
                    '''
                    
                    ],mathjax = True)
                
                ]
    
    
    @app.callback(
        Output("positioned-toast", "is_open"),
        [Input("button-row", "n_clicks")],
    )
    def open_toast(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toast2", "is_open"),
        [Input("button-row2", "n_clicks")],
    )
    def open_toast2(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toast3", "is_open"),
        [Input("button-row3", "n_clicks")],
    )
    def open_toast3(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toast4", "is_open"),
        [Input("button-row4", "n_clicks")],
    )
    def open_toast4(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toastg", "is_open"),
        [Input("button-rowg", "n_clicks")],
    )
    def open_toastg(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toastexr", "is_open"),
        [Input("button-rowexr", "n_clicks")],
    )
    def open_toastexr(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toastgr", "is_open"),
        [Input("button-rowgr", "n_clicks")],
    )
    def open_toastgr(n):
        if n:
            return True
        return False
    
    @app.callback(
        Output("positioned-toastef", "is_open"),
        [Input("button-rowef", "n_clicks")],
    )
    def open_toastef(n):
        if n:
            return True
        return False

    @app.callback(
        Output("positioned-toastOv", "is_open"),
        [Input("button-rowOv", "n_clicks")],
    )
    def open_toastoV(n):
        if n:
            return True
        return False
    
    @app.callback(Output("inflanoteD", "data"),Input("notebut2", "n_clicks"),prevent_initial_call=True)
    def inflNoteDownload(n_clicks):
        return dcc.send_file("assets/Inflation_forecast.ipynb")
    
    @app.callback(Output("infladataD", "data"),Input("databut2", "n_clicks"),prevent_initial_call=True)
    def inflDataDownload(n_clicks):
        return dcc.send_file("assets/inflation_data.xls")
    
    @app.callback(Output("inflaforecastD", "data"),Input("forecastbut2", "n_clicks"),prevent_initial_call=True)
    def inflforecastDownload(n_clicks):
        return dcc.send_file("assets/inflation_forecast.csv")
    
    @app.callback(Output("cpinoteD", "data"),Input("notebut", "n_clicks"),prevent_initial_call=True)
    def cpiNoteDownload(n_clicks):
        return dcc.send_file("assets/cpi_forecast.ipynb")
    
    @app.callback(Output("cpidataD", "data"),Input("databut", "n_clicks"),prevent_initial_call=True)
    def cpiDataDownload(n_clicks):
        return dcc.send_file("assets/cpi_malawi.xls")
    
    @app.callback(Output("cpiforecastD", "data"),Input("forecastbut", "n_clicks"),prevent_initial_call=True)
    def cpiforecastDownload(n_clicks):
        return dcc.send_file("assets/cpi_forecast.csv")
    
    @app.callback(Output("exchnoteD", "data"),Input("notebutex", "n_clicks"),prevent_initial_call=True)
    def exNoteDownload(n_clicks):
        return dcc.send_file("assets/fe_forecast.ipynb")
    
    @app.callback(Output("exchdataD", "data"),Input("databutex", "n_clicks"),prevent_initial_call=True)
    def exDataDownload(n_clicks):
        return dcc.send_file("assets/ExchangeRates.xlsx")
    
    @app.callback(Output("exchforecastD", "data"),Input("forecastbutex", "n_clicks"),prevent_initial_call=True)
    def exforecastDownload(n_clicks):
        return dcc.send_file("assets/exchange_forecast.csv")
    
    @app.callback(Output("taxnoteD", "data"),Input("notebuttax", "n_clicks"),prevent_initial_call=True)
    def taxNoteDownload(n_clicks):
        return dcc.send_file("assets/trip_delay_pricing.ipynb")
    
    @app.callback(Output("contentReply5", "children"), [Input("tabs5", "active_tab")])
    def switch_tab55(at):
        
        
        if at == "aboutP":
            
            pcont = open('assets/about_phew.txt','r').read()
            
            return [
                
                html.Br(),
                dcc.Markdown([pcont])
                ]
            
        
        elif at == "documentation":
            
            dcont = open('assets/documentation.txt','r').read()
            
            return [
                
                html.Br(),
                dcc.Markdown([dcont])
                
                ]
        
        return html.P("This shouldn't ever be displayed...")


    return app
