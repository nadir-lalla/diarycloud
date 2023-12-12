# DiaryCloud

![Logo for website](/static/logo.png)

#### Video Demo: https://youtu.be/bVmudMXybjs

## Introduction

Welcome to CloudDiary. A place where you can keep track of your daily thoughts, moods and emotions. You are able to visualise your thoughts, moods and emotions

## How it works

+ In the Diary tab, you can make an entry into your personal diary and also select your moods/emotions. This is your priavte data and cannot be seen by other users
+ Your homepage will generate a WordCloud using your diary entries and notes, the size of the words will be determined by how many times each word occurs in your entries
+ You are able to view your diary entires as well as your moods and emotions. You can filter by day, month and year
+ You are able to change the month and year to see a WordCloud for the selected period. By default, the WordCloud will be for the current year.

## Getting started

Navigate to the project folder containing the app.py file:

    cd [PATH]/project

Next, import the packages needed. Run the following in the terminal:

    pip install -r requirements.txt

Execute a flask session using the following command:

    flask run

You will be prompted with a URL in the terminal. Hold CTRL and click the link to be redirect to the website

***

<details>

#### Description

My project is a digital diary at its core, but it also has a fun element to it. ie. a WordCloud Generator built in. I have seen other digital diaries online and I've also seen various WordCloud Generators, but I've never seen both combined. That is where I got the idea and the name of my web application. The "Cloud" in the name refers to it being a digital/online diary, and also that it is able to generate a WordCloud.

In the node_modules folder of the project, there are files provided from the [wordcloud2.js](https://wordcloud2-js.timdream.org/#love) project. 

In the static folder, first there is a subfolder for favicon, this folder contains the icon used for the title of the webpage, as well as a pointer icon used for the cloud container. Next in the static folder there are 2 logo image files, created by myself. One used in the navigation bar, and the other used as the login page logo. Next there are 2 javascript files:
1. *wordcloud2*.js is provided from the project above to generate the wordcloud.
2. *script.js* is the file used to generate the correctly formatted input for the wordcloud. The script first defines a list of common words that are excluded from the word cloud. The app.py file provides a single string of texts into the script. The script then removes all unwanted character and splits it into a list. Thereafter all the common words are removed from the dictionary and set to uppercase. The list is then passed into a counter to count each unique word. This is the format required as per the documentation of wordcloud2.js. Thereafter, an array of option is defined manually as per the documentation of wordcloud2. This is an adaptaion of the original where there user is able to edit the options in real-time. This was done to provide the user with a more consisted output that can work on various screen sizes.
Lastly, the WordCloud function is called, that points to the output container and a wordcloud is generated.

Lastly in the static folder, a "*styles.css*" file is used to customise the website and elements to the way I found most attractive.

In the templates folder there are various html files for each of the web pages:
1. The layout of the pages is set by "*layout.html*", which also points to the relevant stylesheets and scripts used.
2. "*login.html*" displays a logo contained in the static folder. The login page allows the user to read about the site without the need to log in. On this page you are also able to redirect to the register page
3. "*register.html*" is a basic form that allows the user to create an account to login. Here there is a need for a display name, which will be displayed as entered.
4. "*index.html*" is displayed upon login, this is the homepage where the wordcloud can be viewed There is a form element that can be used to select the date (month and year) period required.
5. "*diary.html*" is the backbone of the website. This page contains a single form element that creates a database entry using the date (user selected), diary entry, and a list of moods/emotions entered by the user.
6. "*view.html*" generates a table of the users diary entries. By default, it will display the current date. Users can use the form element to filter wish time period they wish to view.
7. "*about.html*" is a basic text based page that gives the user information on how the site works.

In the root folder of the project there are various files that are required to run the website:
1. "*app.py*" the main file for the website
2. "*helpers.py*" used to create a function that is requires a user to be logged in.
3. "*user.db*" a database that contains all the information for login details and diary entries.
4. "*requirements.txt*" a text file that is used to install packages need to run the application using

        pip install -r requirements.txt
5. "*package.json*" and "*package-lock.json*", files installed from the wordcloud2.js package.

</details>


