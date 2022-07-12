from dash import Dash, html, dcc,  Input, Output, State
from matplotlib.pyplot import text
import plotly.express as px
import pandas as pd
import psycopg2 as pg
import os
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
    html.H1(' GLOBAL SUPERSTORE DATA ANALYSIS'),
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
def display_graph(qs):
    if qs=='which category is best selling and more profitable':
        categorydf = newdf.groupby(['Category'])[['Sales', 'Profit_Margin']].sum()
        categorydf1= categorydf.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        fig1 = px.bar(categorydf1,x=categorydf1.index,y=[categorydf1.Profit_Margin,categorydf1.Sales], title= "Bar graph for the Best selling and more profitable Category",barmode='group')

        return fig1
       
        

    elif qs=='which is the best selling and more profitable sub-category':
        subcategorydf = newdf.groupby(['Sub_Category'])[['Sales', 'Profit_Margin']].sum()
        subcategory_salesdf = subcategorydf.sort_values(by=['Profit_Margin'],ascending=False).head().sort_values(by=['Sales'],ascending=False)
        fig1 = px.bar( subcategory_salesdf,x=subcategory_salesdf.index,y=[subcategory_salesdf.Profit_Margin,subcategory_salesdf.Sales], title= "Bar graph for the Best selling and more profitable Sub-Category",barmode='group')
        
        return fig1
       

    elif qs=='which is the top selling sub-category':
       topsubcategory = newdf.groupby(['Sub_Category'])[['Quantity']].sum()#.sort_values('Quantity',ascending=False)
       fig = px.bar(topsubcategory,x=topsubcategory.index,y=topsubcategory.Quantity, title= "Bar graph for the top selling Sub-Category",color=topsubcategory.index)
       return fig     


    elif qs=='which customer segment is more profitable':
        segment_profitdf = newdf.groupby(['Segment'])[['Profit_Margin']].sum()
        fig = px.bar(segment_profitdf,x=segment_profitdf.index,y=segment_profitdf.Profit_Margin, title= "Bar graph for the Most Profitable Segment",color=segment_profitdf.index)
        return fig


    elif qs=='which is the most prefered ship Mode':
        shipmodedf=newdf.groupby(['Ship Mode'])['Sales'].sum().reset_index(name="counts")
        fig = px.bar(shipmodedf,x='Ship Mode',y='counts', title= "Bar graph for the Most Prefered Ship mode",color='Ship Mode')

        return fig   


    elif qs=='which region is the most profitable':  
        region_profitdf = newdf.groupby(['Region'])['Profit_Margin'].sum().reset_index()
        fig = px.bar(region_profitdf,x='Region',y='Profit_Margin', title= "Bar graph for the Most Profitable Region",color='Region')
        return fig          

    else:
        city_salesdf = newdf.groupby(['City'])['Sales', 'Quantity'].sum().sort_values('Quantity',ascending=False)
        city_salesdf1 = city_salesdf[:10]
        fig = px.bar(city_salesdf1,x=city_salesdf1.index,y=city_salesdf1.Quantity, title= "Bar graph for the top 10 selling City",color=city_salesdf1.index)
        return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)