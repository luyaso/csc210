Lucy Yang
lyang25

Project 2 | CSC210

Project dependencies:
Flask
Flask-SQLAlchemy
Flask-Session
Flask-Login
(i recommend using venv)

Hello! My project is a little bit of a posting forum type thing, where users can sign up and post online, kind of like a twitter-type situation. The navigation can be found mostly within the tabs at the top of the screen, which are tailored for each webpage to (hopefully) be the best fit for what each user needs to find, instead of just cramming every single thing into the bar above. There are also some extra navigation things at the bottom of the page, one of which is constant across all pages- the terms & conditions page (which doesn't really have anything too important on it)

the configuration of my database tables is basically as such: there is one table called "User", which contains all the users on it, and another called "Post", which contains the posts of the website, all of which are linked to a user that wrote it.

EXTRA REQUIREMENTS:
I have user authentication, with the ability to log in/out, and pages requiring log in or out.
I have additional database interaction, with one additional database table, and the ability for users to add/delete a user from the website, as well as the ability to add a post to the table.