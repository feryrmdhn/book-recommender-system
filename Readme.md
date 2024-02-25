1. Install virtual env (venv)
    a. python3 -m venv env
    b. source env/bin/activate
2. pip3 install poetry
    a. poetry init
3. uvicorn main:app --reload
4. poetry add fastapi
5. poetry add "uvicorn[standard]"
6. poetry add pandas and other dependency
7. deactivate (for exit from venv)