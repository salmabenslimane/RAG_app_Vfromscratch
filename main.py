from dotenv import load_dotenv
load_dotenv()
#environment variables aka computer parameters that don't get pushed on repository

import os 
print(os.getenv('PATH'))
