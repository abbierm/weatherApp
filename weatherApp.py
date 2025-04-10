from app.main import create_app
import uvicorn
import typer
from config import Settings

cli = typer.Typer()


class DevSettings(Settings):
    dev: bool = True

app = create_app(DevSettings)

@cli.command()
def dev(reload: bool = True):
    uvicorn.run("weatherApp:app", host="0.0.0.0", port=8080, reload=reload)


@cli.command()
def run(reload: bool = False):
    weatherApp = create_app(Settings)
    uvicorn.run(weatherApp, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    cli()