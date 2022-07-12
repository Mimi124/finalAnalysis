from hashlib import new
from dash import Dash, html, dcc,  Input, Output, State
from matplotlib.pyplot import text
import plotly.express as px
import pandas as pd
import psycopg2 as pg
import os
from sqlalchemy import create_engine
import plotly.graph_objs as go

app = Dash(__name__)

path = 'newFile' 
files= os.path.join(path, 'newProcessedFile.csv')

newdf= pd.read_csv(files)  
# print("##########################################")
# print(newdf.head())


questions= ['which category is best selling and more profitable', 'which is the best selling and more profitable sub-category',
                'which is the top selling sub-category','which customer segment is more profitable','which is the most prefered ship Mode','which region is the most profitable',
                'which city has the highest number of sales']


app.layout = html.Div(children=[
    html.H1('DATA ANALYSIS FOR GLOBAL SUPERSTORE'),
     dcc.Dropdown(id='question-dropdown',

                options=[
                 {'label':i, 'value':i} for i in questions],
                 placeholder="Select a question",
                 
            )
            ,


   

    dcc.Graph(
        id='bar-graph',
        
    ),
    
])

@app.callback(
    Output('bar-graph', 'figure'),
     Input('question-dropdown', 'value')
)
def display_graph(question):
    if question=='which category is best selling and more profitable':
        category_info = newdf.groupby(['Category'])[['Sales', 'Profit_Margin']].sum()
        category_info1= category_info.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        fig1 = px.bar(category_info1,x=category_info1.index,y=[category_info1.Profit_Margin,category_info1.Sales], title= "Bar graph for the Best selling and more profitable Category",barmode='group')

        return fig1
       
        

    elif question=='which is the best selling and more profitable sub-category':
        subcategory1 = newdf.groupby(['Sub_Category'])[['Sales', 'Profit_Margin']].sum()
        subcategory_sales = subcategory1.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        fig1 = px.bar( subcategory_sales,x=subcategory_sales.index,y=[subcategory_sales.Profit_Margin,subcategory_sales.Sales], title= "Bar graph for the Best selling and more profitable Sub-Category",barmode='group')
        
        return fig1
       

    elif question=='which is the top selling sub-category':
       subcategory = newdf.groupby(['Sub_Category'])[['Quantity']].sum()#.sort_values('Quantity',ascending=False)
       fig = px.bar(subcategory,x=subcategory.index,y=subcategory.Quantity, title= "Bar graph for the top selling Sub-Category",color=subcategory.index)
       return fig     


    elif question=='which customer segment is more profitable':
        segment_profit = newdf.groupby(['Segment'])[['Profit_Margin']].sum()
        fig = px.bar(segment_profit,x=segment_profit.index,y=segment_profit.Profit_Margin, title= "Bar graph for the Most Profitable Segment",color=segment_profit.index)
        return fig


    elif question=='which is the most prefered ship Mode':
        shipmode=newdf.groupby(['Ship Mode'])['Sales'].sum().reset_index(name="counts")
        fig = px.bar(shipmode,x='Ship Mode',y='counts', title= "Bar graph for the Most Prefered Ship mode",color='Ship Mode')

        return fig   


    elif question=='which region is the most profitable':  
        region_profit = newdf.groupby(['Region'])['Profit_Margin'].sum().reset_index()
        fig = px.bar(region_profit,x=region_profit.Region,y=region_profit.Profit_Margin, title= "Bar graph for the Most Profitable Region",color=region_profit.Region)
        return fig          

    else:
        city_sales = newdf.groupby(['City'])['Sales', 'Quantity'].sum().sort_values('Quantity',ascending=False)
        city_sales1 = city_sales[:10]
        fig = px.bar(city_sales1,x=city_sales1.index,y=city_sales1.Quantity, title= "Bar graph for the top 10 selling City",color=city_sales1.index)
        return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)