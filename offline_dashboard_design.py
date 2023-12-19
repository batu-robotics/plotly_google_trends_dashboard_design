#%% Python Dashboard Design
# Created by: Batuhan Atasoy, Ph.D. Machine Learning

#%% Importing Libaries
import pandas as pd
import plotly.express as px
from dash import Dash,dcc,html

#%% Creating an Offline Data Class
class Data:
    
    # Costructors
    def __init__(self,file_1,file_2):
        self.dataframe_1=pd.read_csv(file_1)
        self.dataframe_2=pd.read_csv(file_2)
        
        # Filling NaN Values with 0
        self.dataframe_2.fillna(0,inplace=True)

    # Analysing Time Series Data
    def time_series(self):
        
        return self.dataframe_1,self.dataframe_2
    
    # Sorting the Dataframe with respect to the 10 Countries of Highest Research in the Related Area
    def sort_data(self):
        
        return [self.dataframe_2.sort_values(by=self.dataframe_2.columns[i],
                ascending=False).iloc[:10,:] for i in range(1,len(self.dataframe_2.columns))]
    
#%% Creating a Plotly Dashboard
app=Dash("__name__")

file1='football,rugby,tennis.csv'
file2='geoMap_football,rugby,tennis.csv'
d=Data(file1,file2)

# Constructing the Dataframes
df1,df2=d.time_series()

# Plotly Figures of football,rugby and tennis
fig_1=px.line(df1,x=df1.columns[0],
              y=df1.columns[1:],
              title='Timeline of Google Trends Data Interest')

# Detecting the Sum of the Trends 
# with respect to the Sport Types for the Pie Chart
df_sum=df1.iloc[:,1:].sum().T
df_total=df_sum.sum()

# Pie Chart Desin with Plotly
fig_2=px.pie(df_sum, values=df_sum, 
             names=df1.columns[1:],hole=0.5,
             title='Google Trends Data Interest Pie Chart')

# Bar Chart with respect to the Most Interested Sport Types
sorted_data=d.sort_data()

#Plotting Football Data
fig_3=px.bar(sorted_data[0], x=sorted_data[0].columns[0], y=sorted_data[0].columns[1:],
             barmode="group",
             title='Top 10 Countries Having the Most Interest with respect to the Football')

#Plotting Rugby Data
fig_4=px.bar(sorted_data[1], x=sorted_data[1].columns[0], y=sorted_data[1].columns[1:],
             barmode="group",
             title='Top 10 Countries Having the Most Interest with respect to the Rugby')

#Plotting Tennis Data
fig_5=px.bar(sorted_data[-1], x=sorted_data[-1].columns[0], y=sorted_data[-1].columns[1:],
             barmode="group",
             title='Top 10 Countries Having the Most Interest with respect to the Tennis')

# Dashboard Layout
app.layout = html.Div([
    html.H2('Google Trends Dataset Analysis for the Last 3 Months of Worldwide Football, Rugby and Tennis Data'),
    dcc.Graph(figure=fig_1),
    dcc.Graph(figure=fig_2),
    dcc.Graph(figure=fig_3),
    dcc.Graph(figure=fig_4),
    dcc.Graph(figure=fig_5),
    ])


if __name__=="__main__":
    app.run_server(debug=True)