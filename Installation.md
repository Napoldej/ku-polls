# Installation Guide
1. Git clone application
    ```python
    git clone https://github.com/Napoldej/ku-polls.git

    ```
2. Change directory into the repo
    ```python
    cd ku-polls
    ```

3. Create Virtual Environment
    ``` python
    python -m venv env
    ```


4. Activate The Virtual Environment
    ```python
    # On Linux or MacOS:
    source env/bin/activate

    # On Windows:
    env\Scripts\activate
    ```

5. Download the requirement package for running this application
    ```python
    pip install -r requirements.txt
    ```

6. Create a .env file by copying the contents of sample.env
    ```
    # On MacOS/Linux:
    cp sample.env .env

    # On Windows:
    copy sample.env .env
    ```


7. Run migrations
    ```
    python manage.py migrate
    ```
8. Download data fixtures
    ```
    python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
    
    ```

9. Run test
    ```
    python manage.py test
    ```
