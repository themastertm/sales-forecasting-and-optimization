from dash import Dash, dcc, html
import plotly.express as px

def render_department_performance(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]
    
    # Performance by Department Content
    department_sales = filtered_df.groupby('Dept')['Weekly_Sales'].sum().reset_index().sort_values(by='Weekly_Sales', ascending=False)

    return html.Div([
        dcc.Graph(
            figure={
                'data': [
                    {'x': department_sales['Dept'].astype(str), 'y': department_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Sales by Department'}
                ],
                'layout': {
                    'title': 'Department Performance',
                    'xaxis': {'title': 'Department'},
                    'yaxis': {'title': 'Total Sales'}
                }
            }
        ),
    ])
