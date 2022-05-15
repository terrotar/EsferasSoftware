
# Esferas Software

This project is a challenge of the company [Esferas Software](https://esferas.com.br/) and the deadline was of 4 days.
It's a CRUD API with one table named "Contatos" and with a few columns, such as CPF, phones and emails. It was made with Python, framework FastAPI, ORM SQLAlchemy, Database SQLite3, HTML, CSS, log files, and others technologies.

Feel free to use it and contact me for any feedback!

Thanks and hope you enjoy it!


## How Run the Project

First of all, you should install all dependencies found in Pipfile(if you use pipenv) or requirements.txt(any other package manager).

    pipenv install
or

    pip install -r requirements.txt


Then, you just need to open a terminal and move to directory "/app" and run the uvicorn server:

    uvicorn main:app --reload


The application will start in localhost and can be open with any browser. There's two default API documentation that can be accessed with endpoint "/docs" and "/redoc".

Also, the project has a docker image, which could be used to run the program more easier. To do so, simply check my [DockerHub](https://hub.docker.com/r/terrotar/esferas_software_challenge) repository, pull the image and run the command below:

    sudo docker run -p 8000:8080 terrotar/esferas_software_challenge:v1

## About

The development of the project was a very harsh momment. Due to it's few days to develop, I had to spend almost all days until deadline to accomplish it as I imagined to do it. The front-end wasn't part of the objectives, but I thougth it would be a nice bonus feature to implement. The company website was used as a reference to develop the style and format of API front-end part, such as buttons, colors, patterns and more.

The project has 2 groups of endpoints, "Contacts" and "HTML Pages". The second was developed to combine the API and front-end, to return a HTML page as response, enabling the front-end development. It could be used a front-end framework, such as ReactJS or any other but I've worked a little with front-end frameworks and the time didn't make it possible to give a try. Although the front-end development was made inside the same application, it's quite simple to transfer it to any other technology and it gives a nice idea of client's side and it'x user experience.

It was a very nice challenge to do and I think I accomplish most of the tasks. Hope you enjoy it!
