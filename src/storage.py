from datetime import datetime
from os import makedirs

def save_file(file, name, directory, type):
    # Filename template: '<playlist-name>_<current_datetime>.pdf'
    filename = "{}_{}.{}".format(name.replace(' ', '_'), datetime.now().isoformat().replace(':', '.'), type)
    tmp_path = "{}/{}".format(directory, filename)

    # Ensure that the directory exists
    makedirs(directory, exist_ok=True)

    # write tmp file
    with open(tmp_path, 'xb') as saver:
        saver.write(file)

    return tmp_path