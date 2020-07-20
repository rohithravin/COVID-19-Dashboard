# COVID-19 Dashboard

With all the news outlet talking about coronavirus, it gets hard (personally) to decide which outlet is truthful or just manipulating the data. This dashboard was created with the idea to create an objective view of the coronavirus with real-time time data updated daily from proper officals. 

This dashboard focuses mainly on California and then World since in the begining I was for personal, but later on it could be expanded. 

Hope you guys enjoy it! 

> ## Data Source 

The most important part of this project was the data source. The data used for this project comes to validated and the proper sources. 

The California data is from the publicly avaiable dataset hosted by the California Gov't:

`https://data.ca.gov/dataset/covid-19-cases`

The World data is aquired from the` Our World In Data` which relies on the Europen CDC:

`https://ourworldindata.org/coronavirus-source-data`

> ## Project Archecture

![project-arch](img/project-arch.png)


> ## Run Project

To run this project locally you need to run ther server and the angular project. You will also need to set up a MySQL database, but that documentation is yet to come. 

### Run NodeJS Server

In your terminal run the follow commands:

```
cd COVID-19-Dashboard/corona-dashboard-server
npm install
npm start
```

### Run Angular Project
```
cd COVID-19-Dashboard/corona-dashboard
npm install
ng serve --open=true
```

> ## California Dashboard
> This dashboard is specific to the state of California. Based on your zipcode, the corresponding data will be curated to visualized for you to view. You can also different visualizations of the state data as well. Below is the youtube video demo showcasing the dashboard.


[![California Dashboard](http://img.youtube.com/vi/zRc0mbsVl8Y/0.jpg)](http://www.youtube.com/watch?v=zRc0mbsVl8Y "California Dashboard")

> ## World Dashboard
> This dashboard is specific to the world. Data is currated so you can see the top countries affected and toggle through the plots. You can also search specfic countries to view data specific to that country.

[![World Dashboard](http://img.youtube.com/vi/J1ynNYSbHQs/0.jpg)](http://www.youtube.com/watch?v=J1ynNYSbHQs "World Dashboard")


