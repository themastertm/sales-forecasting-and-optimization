from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from overview import render_overview  # Import the Overview tab
from sales_trends import render_sales_trends  # Import the Sales Trends tab
from department_performance import render_department_performance  # Import the Department Performance tab
from seasonality_analysis import render_seasonality_analysis  # Import the Seasonality Analysis tab

# Load data
df = pd.read_csv('../walmart_cleaned.csv')

# Prepare Date column (same as in your previous code)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + df['WeekOfYear'].astype(str) + '0', format='%Y%W%w')

# Get list of available years
years_available = df['Year'].unique()
years_available.sort()

# Start Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

# Layout
app.layout = html.Div([

    # Logo Section
    html.Div([
        html.Img(src='/assets/walmart-logo.png', style={'width': '400px', 'height': 'auto'}),
    ], className='logodiv'),

    # Main Container
    dbc.Container([

        # Title Section
        html.H1('Walmart Sales Dashboard', className='text-center my-4'),

        # Tabs Section
        dcc.Tabs(id="tabs", value='tab-overview', children=[
            dcc.Tab(label='Overview', value='tab-overview'),
            dcc.Tab(label='Sales Trends', value='tab-sales-trends'),
            dcc.Tab(label='Performance by Department', value='tab-department-performance'),
            dcc.Tab(label='Seasonality Analysis', value='tab-seasonality-analysis')
        ]),

        # Dropdown Section
        dbc.Row([
            dbc.Col([
                html.Label('Select Year:', className="fw-bold"),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in years_available],
                    value=years_available[0],
                    clearable=False
                ),
            ], width=4)
        ], className="mb-4"),

        # Dynamic Content Section
        html.Div(id='tabs-content')

    ], fluid=True)
])

# Callback to render content based on selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('year-dropdown', 'value')
)
def render_content(tab, selected_year):
    if tab == 'tab-overview':
        return render_overview(selected_year, df)
    elif tab == 'tab-sales-trends':
        return render_sales_trends(selected_year, df)
    elif tab == 'tab-department-performance':
        return render_department_performance(selected_year, df)
    elif tab == 'tab-seasonality-analysis':
        return render_seasonality_analysis(selected_year, df)

if __name__ == '__main__':
    app.run(debug=True)
