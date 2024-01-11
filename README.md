Quickstart
----------

First, clone the project on your local machine: ::

git clone https://github.com/HamzaMohammadRdaideh/Assignment.git

Then activate poetry by typing: ::

    poetry shell

If the poetry not installed, install it before implementing the previous command: ::

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
    export PATH="$HOME/.poetry/bin:$PATH"
    poetry install
    poetry shell

Finally to run the app::

    uvicorn app.main:app --reload
    or

    uvicorn app.main:app --reload --port {PORT_NUMBER}



