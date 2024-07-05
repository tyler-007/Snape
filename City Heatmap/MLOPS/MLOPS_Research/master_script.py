import Script_fetch_from_db
import Parse
import process
import dataprocess
import laggeddata
import weatherunion_script
import model_predict
import app
import Script_fetch_from_db

import subprocess

def main():
    # Execute your series of scripts
    Script_fetch_from_db.run()
    Parse.run()
    process.run()
    dataprocess.run()
    laggeddata.run()
    weatherunion_script.run()
    model_predict.run()
    streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])
    streamlit_process.wait()  

if __name__ == "__main__":
    main()




