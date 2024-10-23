# run.py

import os

if __name__ == "__main__":
    os.system("uvicorn app.main:app --reload")

