from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

def render_seasonality_analysis(selected_year, df):
    filtered_df = df[df['Year'] == selected_year]

    # Sales by Season (Sales grouped by 'Season')
    sales_by_season = filtered_df.groupby('Season')['Weekly_Sales'].sum().reset_index()

    # Create a bar chart for Sales by Season
    seasonality_fig = px.bar(sales_by_season, x='Season', y='Weekly_Sales',
                             title='Sales by Season', labels={'Weekly_Sales': 'Sales'})
    seasonality_fig.update_layout(title_x=0.5)

    # Promo vs Non-Promo Sales (Using 'IsPromoWeek' column)
    promo_sales = filtered_df.groupby('IsPromoWeek')['Weekly_Sales'].mean().reset_index()
    promo_sales['Promo'] = promo_sales['IsPromoWeek'].map({False: 'Non-Promo', True: 'Promo'})

    # Create a bar chart for Promo vs Non-Promo Sales
    promo_fig = px.bar(promo_sales, x='Promo', y='Weekly_Sales',
                       title='Promo vs Non-Promo Sales', labels={'Weekly_Sales': 'Average Sales'})

    return html.Div([
        # Sales by Season Chart
        dbc.Row([dbc.Col([dcc.Graph(figure=seasonality_fig)], width=12)]),
        
        # Promo vs Non-Promo Sales Chart
        dbc.Row([dbc.Col([dcc.Graph(figure=promo_fig)], width=12)]),
    ])
