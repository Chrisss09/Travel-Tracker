# Travel Tracker

This is my 3rd project for Data Centric Development, I have chosen to use Bootstrap 4 to structure my app.
This is a website to share and review your holiday experiences or you can plan where you are going to go in the future.

The user's can create, read, and share information. When the user logs into the site they can view other user's reviews - just like a trip advisor.

## **UX**

This website was made for people that like to travel and go on holiday. I have created this website so that people can create, read, update, and delete information.

The website can be used as a planner and a website to review countries. The user can add times and dates of flights, and plan key attractions on where they would like to go. You can also go back to your post and review it or you can add a new post for a country you have already been to and review it.

If the user wanted to plan their holiday or post a review, they can register as a new user or login. Then they can click on the add button and fill out the required fields to create a post.

The user will then be able to edit and delete their post but will not be able to on another user's post and all users can read every post.

I have also implemented a map for the user to use. This can track your location, measure distances. I have got some information off the internet and added it onto the map for data vizulisation. The user will be able to plan (if they wanted to) visit the top 10 restaurants, attractions, and countries in the world.

## **Features**

### Existing features

On my homepage I have designed a stylish page to engage the user. I have used a Bootstrap 4 carousel with some beautiful photos.
When you scroll down I have said what the website is about and at the bottom I have created a getting started section.

The user after selling it to them can then register, then once a username has been created they will be diverted to the planner board where they can then view and share information.

Also at the bottom of the homepage the user can click on the map and also click on the planner if already a user.

Once the user has clicked on the map, one of the features is that it can track your current location, this can be vital to a user if they are in a foreign country they may get lost or you can use it to plan your journey. All the user will need to do is click on the marker on the left handside and allow the app to track your location.

You can also use the map to measure distances which can come in handy with the location tracker and measure the distances from your current location or anything else that you want to do. You can do all this by clicking on the measuring ruler on the right handside.

Also just under that you can click on the little box and you can then view your map on full screen.

Under that I have created a layer control key so a user can identify the markers on the map and then they can personalise them by unchecking the boxes.

I got the data from Google by searching top 10 restaurants, top 10 countries and top 10 attractions and I put them in a text document using their latitudes and longitudes I was able to add markers.

This will come in handy for a user whilst they are planning a trip or out and about and they want to find where is closest.

### Future additions

At the time of writing this, it is at the end of this project, I have vizualised and planned this as I wanted it to look.

There are some features that I had to find a plan B for that still worked really well and then building further ideas on to that for the future.

My first example is when creating my map - I would like to replace this with Google Maps. I chose to create my map using Folium and I created an algorithum for when a user logs a country to their planner a marker would be added to the map. After I wrote the algoritham I found out that you cannot automatically update the map, so I needed to stop and start the script for updates to take effect, which is not advisable.
My plan B was then to get some information off the internet and just add markers on the map plus add some features to my map.

My website was originally going to be more of a planner where the user would have their own personal logs but due to time restraints I went for plan B and made my site more like a trip advisor site.

In the future I would like my map to be made with Google Maps so a user can automatically add, edit and delete markers. Also I would still like the user review site but also add a personal planner profile page.

## **Technologies used**

To create my app I have used a number of technologies which are the following:

* Virtual Environment
  * To setup my project I have used a virtual environment to install all the dependencies that I need to run my app.

* Python
  * To write my app I have used the Python programming language.

* Flask
  * To create my website I have used the Flask framework.

* MongoDB
  * The database I have chosen to use for the data side of this project is MongoDB to allow the user to use CRUD.

* Environment Variable - Python-dotenv
  * To connect to MongoDB and also store my secret key I have used python-dotenv to create a dot env file and I have hidden this in my gitignore file. For the majority of the project I have stored my MongoDB connection link in my bashrc file to locally store my link but when I have deployed my site using Heroku I have installed python-dotenv and updated my requirements.txt file.

* PyMongo
  * In my project I have installed PyMongo which helps me interact with my MongoDB database.

* ObjectId
  * I have used ObjectId so that I can interact with MongoDB's automatically generated ID key.

* Folium
  * I have installed Folium to create a free map to use with data visualisation.

* Plugins and MeasureControl
  * With Folium I have imported Plugins and MeasureControl for additional features on my map such as to track user's location, measure distances, and giving an option to the user so they can make the map full screen.

* Pandas
  * I have installed Pandas to my app so that I can display data on my Folium map.

* Bootstrap
  * To style and structure my website I have used Bootstrap so I could create grids and easily style and structure my work.

* Bootstrap Carousel
  * One of the things I planned to have on my site was to have an image slider so I used a Bootstrap one. After choosing my images from Google I found they were all different sizes, so I used a free site which was [pixlr.com](https://pixlr.com/editor/) after watching a Youtube video and I made them all the same size and they work effectively.

## **Testing**

## **Deployment**

## **Credits**

### Content

### Media

### Acknowledgements
