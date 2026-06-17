import os
import sys

from dotenv import load_dotenv
load_dotenv()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
