from app.main import create_app
import uvicorn
import typer
from config import Settings


class DevSettings(Settings):
    dev: bool = True

app = create_app(DevSettings)

def main(dev: bool = False):
    if dev:
        print("running dev mode")
        uvicorn.run("weatherApp:app", host="0.0.0.0", port=8080, reload=True)
    else:
        weatherApp = create_app(Settings)
        uvicorn.run(weatherApp, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()