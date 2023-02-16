from datetime import datetime

def save_file(file, name, type):
    # Filename template: '<playlist-name>_<current_datetime>.pdf'
    filename = "{}_{}.{}".format(name.replace(' ', '_'), datetime.now().isoformat().replace(':', '.'), type)
    tmp_path = "__tmp__/{}".format(filename)

    # write tmp file
    with open(tmp_path, 'xb') as saver:
        saver.write(file)

    return tmp_path