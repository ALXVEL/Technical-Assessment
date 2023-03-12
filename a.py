import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

df = pd.read_csv('BI_Analyst_Dataset_1_FY21.csv')

#grouping data by unique client id and then summing its columns
revenues_df = df.groupby('client_unique_id').sum()[['odi_cad', 'nii_cad', 'payment_revenue_cad', 'service_revenue_cad', 'total_revenue']]

#sorting the df by total revenue
revenues_df = revenues_df.sort_values('total_revenue', ascending=False)

# ---------------- CODE FOR BEST CLIENTS (top 10) ------------------
best_clients_graph = go.Figure()
#odi_cad column
best_clients_graph.add_trace(go.Bar(x= revenues_df.index[:10], y= revenues_df['odi_cad'][:10], name='Other Direct Income'))
#nii_cad column
best_clients_graph.add_trace(go.Bar(x= revenues_df.index[:10], y= revenues_df['nii_cad'][:10], name='Net Interest Income'))
#payment_revenue_cad column
best_clients_graph.add_trace(go.Bar(x= revenues_df.index[:10], y= revenues_df['payment_revenue_cad'][:10], name='Payment Revenue'))
#service_revenue_cad column
best_clients_graph.add_trace(go.Bar(x= revenues_df.index[:10], y= revenues_df['service_revenue_cad'][:10], name='Service Revenue'))

# setting up the stacked bar graph
best_clients_graph.update_layout(barmode='stack', title='Best 10 Clients by Revenue', xaxis_title = 'Clients Unique ID', yaxis_title='Revenue (CAD)')


# ----------------- CODE FOR WORST CLIENTS (bottom 10) ------------------------

worst_clients = revenues_df[revenues_df['total_revenue'] > 0].tail(10)

worst_clients_graph = go.Figure()
#odi_cad column
worst_clients_graph.add_trace(go.Bar(x= worst_clients.index, y= worst_clients['odi_cad'][-10:], name= 'Other Direct Income'))
#nii_cad
worst_clients_graph.add_trace(go.Bar(x= worst_clients.index, y= worst_clients['nii_cad'][-10:], name= 'Net Interest Income'))
#payment_revenue_cad
worst_clients_graph.add_trace(go.Bar(x= worst_clients.index, y= worst_clients['payment_revenue_cad'][-10:], name= 'Payment Revenue'))
#service_revenue_cad
worst_clients_graph.add_trace(go.Bar(x= worst_clients.index, y= worst_clients['service_revenue_cad'][-10:], name= 'Service Revenue'))

#set up
worst_clients_graph.update_layout(barmode='stack', title='Worst 10 Clients by Revenue (Non-Zero)', xaxis_title = 'Clients Unique ID', yaxis_title= 'Revenue (CAD)')


# ------------- List of 0 revenues (Actual Worst Clients) ----------------------
actual_worst_clients = revenues_df[revenues_df['total_revenue'] == 0]
awc_list = []
for client in actual_worst_clients.index:
    awc_list.append(html.Li(client))

# dash app
app = dash.Dash()

app.layout =html.Div( children=[
    html.H1('Best and Worst Clients by Revenue - GTB (FY 2021)'),
    dcc.Graph(id='top-10-revenue', figure=best_clients_graph),
    dcc.Graph(id='bottom-10-revenue', figure=worst_clients_graph),
    html.H2('List of 0 Revenues (Actual Worst Clients)'),
    html.Ul(children=awc_list)
])

#running
if __name__ == '__main__':
    app.run_server(debug= True)
