## KU Polls: Online Survey Questions

[![Django CI](https://github.com/Napoldej/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/Napoldej/ku-polls/actions/workflows/django.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation

- In the wiki:
Check the installation instructions [here](../../wiki/Installation-and-Configuration)

- In the file:
Check the installation instruction  <a href="Installation.md">Installation.md</a> file 

## Running the Application

1. Activate the virtual environment
   ```
   # On Linux or MacOS:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```
   
2. Start the django server
    ```python
    python manage.py runserver

    #if you get the message that tell this port is unavailable. replace any number to xxxxx
    python manage.py runserver xxxxx
    ```

3. Access the app in a web browser, which is showed on terminal
    ```python
    #example http://127.0.0.1:8000/
    ```

4. Exit the virtual environment by closing the window or by typing:
   ```
   deactivate
   ```

## Demo Accounts

Sample polls and user data are included. There are 3 demo accounts:

| Username | Password |
|:---------|:---------:|
|  demo1   | hackme11 |
|  demo2   | hackme22 |
|  demo3   | hackme33 |


## Documents
All project documents are in the [Project Wiki](../../wiki).

- [Vision Statement](../../wiki/Vision-and-Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project-plan)
- [Domain Model](../../wiki/Domain-Model)

## Iteration Plans and Boards
1. [Iteration plan 1](../../wiki/iteration-1-plan) and [Board](https://github.com/users/Napoldej/projects/4)
2. [Iteation plan 2](../../wiki/iteration-2-plan) and [Board](https://github.com/users/Napoldej/projects/4/views/2)
3. [Iteration plan 3](../../wiki/iteration-3-plan) and [Board](https://github.com/users/Napoldej/projects/4/views/3)
