from dash import Dash, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# Small function to format numbers
def format_number(number):
    """Format large numbers into a readable format with appropriate suffix (B for billions, M for millions)."""
    if number >= 1_000_000_000:
        return "${:.2f}B".format(number / 1_000_000_000)
    elif number >= 1_000_000:
        return "${:.2f}M".format(number / 1_000_000)
    else:
        return "${:,.2f}".format(number)

# Function to generate the overview tab content
def render_overview(selected_year, df):
    """Render the Overview tab for the selected year"""
    
    # Filter the dataframe for the selected year
    filtered_df = df[df['Year'] == selected_year]

    # Calculate KPIs
    total_sales_value = filtered_df['Weekly_Sales'].sum()
    average_sales_value = filtered_df['Weekly_Sales'].mean()
    top_store_id = filtered_df.groupby('Store')['Weekly_Sales'].sum().idxmax()

    # Apply formatting
    total_sales = format_number(total_sales_value)
    average_sales = format_number(average_sales_value)
    top_store_text = f"Store {top_store_id}"

    # Prepare charts (Sales Trend, Sales by Department, Promo vs Non-Promo)
    weekly_sales = filtered_df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    department_sales = filtered_df.groupby('Dept')['Weekly_Sales'].sum().reset_index()
    promo_sales = filtered_df[filtered_df['IsPromoWeek'] == 1].groupby('Date')['Weekly_Sales'].sum().reset_index()
    non_promo_sales = filtered_df[filtered_df['IsPromoWeek'] == 0].groupby('Date')['Weekly_Sales'].sum().reset_index()

    # Build the Overview tab layout
    return html.Div([

        # Header for the overview
        html.H3("Overview of Sales Performance", className="text-center mb-4"),

        # KPI Cards Section
        dbc.Row([

            # Card for Total Sales
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Sales", className="card-title"),
                        html.P(total_sales, className="card-text total-sales", style={'fontSize': '24px'})
                    ])
                ], className="card shadow-sm")
            ], width=4),

            # Card for Average Weekly Sales
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Average Weekly Sales", className="card-title"),
                        html.P(average_sales, className="card-text avg-sales", style={'fontSize': '24px'})
                    ])
                ], className="card shadow-sm")
            ], width=4),

            # Card for Top Store
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Top Store", className="card-title"),
                        html.P(top_store_text, className="card-text top-store", style={'fontSize': '24px'})
                    ])
                ], className="card shadow-sm")
            ], width=4)

        ], className="my-4"),

        # Sales Trend Chart (Weekly Sales Over Time)
        dbc.Row([dbc.Col([dcc.Graph(
            figure={
                'data': [{'x': weekly_sales['Date'], 'y': weekly_sales['Weekly_Sales'], 'type': 'line', 'name': 'Weekly Sales'}],
                'layout': {'title': 'Weekly Sales Over Time', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Sales'}}
            }
        )], width=12)]),

        # Sales by Store/Department (Bar Chart)
        dbc.Row([dbc.Col([dcc.Graph(
            figure={
                'data': [{'x': department_sales['Dept'].astype(str), 'y': department_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Sales by Department'}],
                'layout': {'title': 'Sales by Department', 'xaxis': {'title': 'Department'}, 'yaxis': {'title': 'Sales'}}
            }
        )], width=6),

        # Promo vs Non-Promo Performance (Comparison Bar Chart)
        dbc.Col([dcc.Graph(
            figure={
                'data': [
                    {'x': promo_sales['Date'], 'y': promo_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Promo Sales'},
                    {'x': non_promo_sales['Date'], 'y': non_promo_sales['Weekly_Sales'], 'type': 'bar', 'name': 'Non-Promo Sales'}
                ],
                'layout': {'title': 'Promo vs Non-Promo Performance', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Sales'}}
            }
        )], width=6)])

    ])
