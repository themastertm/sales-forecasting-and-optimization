from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

def render_sales_trends(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]

    # Sales Trends Content
    weekly_sales = filtered_df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    monthly_sales = filtered_df.groupby('Month')['Weekly_Sales'].sum().reset_index()
    holiday_sales = filtered_df.groupby('Holiday_Flag')['Weekly_Sales'].mean().reset_index()
    holiday_sales['Holiday_Type'] = holiday_sales['Holiday_Flag'].map({0: 'Non-Holiday', 1: 'Holiday'})

    return html.Div([
        # Weekly Sales Over Time Graph
        dcc.Graph(
            figure={
                'data': [
                    {'x': weekly_sales['Date'], 'y': weekly_sales['Weekly_Sales'], 'type': 'line', 'name': 'Weekly Sales'}
                ],
                'layout': {
                    'title': 'Weekly Sales Over Time',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales'},
                    'hovermode': 'x unified'
                }
            }
        ),

        # Row for Monthly Sales and Holiday vs Non-Holiday Sales
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': monthly_sales['Month'], 'y': monthly_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Monthly Sales'}
                        ],
                        'layout': {
                            'title': 'Sales by Month',
                            'xaxis': {'title': 'Month'},
                            'yaxis': {'title': 'Sales'}
                        }
                    }
                ),
            ], width=6),

            dbc.Col([
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': holiday_sales['Holiday_Type'], 'y': holiday_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Holiday vs Non-Holiday'}
                        ],
                        'layout': {
                            'title': 'Average Sales: Holiday vs Non-Holiday',
                            'xaxis': {'title': 'Holiday'},
                            'yaxis': {'title': 'Average Weekly Sales'}
                        }
                    }
                ),
            ], width=6)
        ])
    ])
