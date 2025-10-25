from app.init import create_app
from app.utils import try_load_initial_data

app = create_app()

@app.cli.command('load-data')
def load_data_command():
    if try_load_initial_data():
        print('Initial data loaded')
    else:
        print('An error occurred while trying to upload initial data')


if __name__ == '__main__':
    app.run(debug=True)
