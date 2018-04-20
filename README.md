# 507finalproject
[Overview & Preparation]
For this project, when you type into the city’s name for searching, it will return the results and detailed information of available restaurants, events within that city. I use Tripadvisor and Yelp for my data sources, and Yelp requires my API key, and that’s for the authentication.

The API key should be placed in a file called "secret.py", and the content should be like: "api_kei = 'your Yelp API key'"

[How it works]
When you type in the city’s name following the instruction, and the system will ask for the data presentation method you prefer. So if you type in 1, it will show a map in plotly that tells you the location of the available restaurants. if you go with 3, it will shows the detailed information of the events that are happening in the city you search for by using flask.

When you want to see which restaurants have their information both on Yelp and TripAdvisor, you can get the results basing on this relationship and type 5 for corresponding data visualization.

[Stucture]
For the main functions, make_request_from_ta(geo_code, city_name) will srcap the data from TripAdvisor, main() and main2() will request the data from Yelp, for restaurants and events. create_tournament_db() and populate_tournament_db() will generate the database for the projects. plot_yelp_resturant() and plot_yelp_event() will help to present the data from yelp in plotly. run_flask() will help to present the data in html format. Also, there are cache dictions for the response for Yelp and TripAdvisor.

[Unit Testing]
For the tests I try to test whether I got the expected data from each sources, so I check whether it is true that some names of the restaurants or events do exist in the list of each kind of objects. I also test whether the plotly and flask work as well as expected by checking the status of it and run the functions.