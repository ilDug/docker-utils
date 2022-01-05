import uvicorn
import os

if __name__ == "__main__":
    if os.environ["MODE"] == "DEVELOPMENT":
        print("il Server si avvia in modalità DEVELOPMENT")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

    elif os.environ["MODE"] == "PRODUCTION":
        print("il Server si avvia in modalità PRODUCTION")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)

    else:
        print(
            "ERROR: nessuna modalità di run (PRODUCTION/DEVELOPMENT) è stata definita nella variabili d'ambiente"
        )
