import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Загрузка данных
df = pd.read_csv(r'C:\Users\Admin\PycharmProjects\pythonProject\TextFile1.csv')

# Создание экземпляра приложения
app = dash.Dash(__name__)

# Определение структуры дашборда
app.layout = html.Div([
    html.Div([
        html.H1('Дашборд анализа данных об ушедших и вернувшихся клиентах', style={'textAlign': 'center'}),
        html.P('Этот дашборд предоставляет информацию об ушедших клиентах в тот или иной период времени',
               style={'textAlign': 'center'}),
        html.Div([
            html.Label('Отзыв:', style={'fontSize': 18}),
            dcc.Dropdown(
                id='date-dropdown',
                options=[{'label': date, 'value': date} for date in df['отзыв']],
                value=df['отзыв'].iloc[0],
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    ], style={'marginBottom': '30px'}),

    html.Div([
        # Линейный график
        dcc.Graph(id='line-chart'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Гистограмма
        dcc.Graph(id='histogram'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Круговая диаграмма
        dcc.Graph(id='pie-chart'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Ящик с усами
        dcc.Graph(id='box-plot'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Точечный график
        dcc.Graph(id='scatter-plot'),
    ], style={'width': '48%', 'display': 'inline-block'}),

], style={'padding': '20px'})

# Определение логики дашборда
@app.callback(
    Output('line-chart', 'figure'),
    Output('histogram', 'figure'),
    Output('pie-chart', 'figure'),
    Output('box-plot', 'figure'),
    Output('scatter-plot', 'figure'),
    [Input('date-dropdown', 'value')]
)
def update_charts(selected_date):
    # Линейный график
    line_chart = go.Figure(go.Scatter(x=df['Дата'], y=df['кол-во ушедших клиентов']))
    line_chart.update_layout(title='Линейный график',
                             xaxis_title='Дата',
                             yaxis_title='кол-во ушедших клиентов',
                             plot_bgcolor='rgb(230, 230, 230)')

    # Гистограмма
    histogram = go.Figure(go.Histogram(x=df['Дата']))
    histogram.update_layout(title='Гистограмма',
                            xaxis_title='Дата',
                            yaxis_title='кол-во ушедших клиентов',
                            plot_bgcolor='rgb(230, 230, 230)')

    # Круговая диаграмма
    pie_chart = px.pie(df, names='Дата', values='кол-во вернувшихся',
                       title='Круговая диаграмма')

    # Boxplot
    box_plot = px.box(df, x='Дата', y='кол-во вернувшихся',
                      title='Boxplot')

    # Точечный график
    scatter_plot = px.scatter(df, x='Дата', y='кол-во вернувшихся',
                             title='Точечный график')

    return line_chart, histogram, pie_chart, box_plot, scatter_plot

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)

'''
Дата,Доходы,Расходы,Активы,Пассивы,Чистая прибыль
2020-06-16,11519.73,9892.48,212959.18,771014.77,2137.26
2020-09-16,37152.40,6760.33,738481.08,140477.16,18795.82
2022-12-27,28900.35,25150.60,801812.63,392318.33,12909.06
2021-12-21,17944.15,19808.55,450793.88,730729.59,17666.50
2020-10-13,14767.11,14609.46,711727.09,602819.96,1485.17ё

'''