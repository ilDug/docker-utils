import uvicorn
import certifi
import os

print(certifi.where())

if __name__ == "__main__":
    if os.environ['MODE'] == "dev":
        print("il Server si avvia in modalità DEVELOPMENT")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

    if os.environ['MODE'] == "prod":
        print("il Server si avvia in modalità PRODUCTION")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)

    else:
        print("ERROR: nessuna modalità di run (PROD/DEV) è stata definita nella variabili d'ambiente")
