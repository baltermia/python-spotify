from fpdf import FPDF

def from_millis(millis):
    """ 
    Task an amount of milliseconds and returns the calculated hours, seconds and minutes from it
    """
    # calc
    seconds = (millis /1000 ) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24

    # return tuple
    return hours, minutes, seconds

def millis_to_string(millis):
    """
    Takes an amount of milli seconds and into a string formmated like this: 0h 0min 0s
    """

    # get from main method
    hours, minutes, seconds = from_millis(millis)

    # add seconds
    result = "%ds" % (seconds)

    # add minutes if there are some
    if minutes >= 1:
        result = "%dmin " % (minutes) + result

    # add hours if there are some
    if hours >= 1:
        result = "%dh " % (hours) + result

    return result

def latinify(str):
    """
    Removes special characters like emojis from the string (fpdf cant handle them) and returns it
    """
    return str.encode('ascii', 'ignore').decode('ascii')

def create_pdf(json):
    # Create default pdf setttings and add first page
    pdf = FPDF()
    pdf.set_font('Helvetica', '', 16)
    pdf.add_page()
    pdf.image('src/res/background.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
    pdf.set_text_color(255, 255, 255)

    # Set default variables
    tracks = json["tracks"]["items"]

    # Get playlist url
    pl_url = json["external_urls"]["spotify"]

    # Add playlist cover to pdf
    img_url = json["images"][0]["url"]
    pdf.image(name = img_url, x = 20, y = 20, h = 75, link = pl_url)

    # Add playlist name
    pl_name = latinify(json["name"])

    pdf.set_font('Helvetica', 'B', 44)
    pdf.text(x = 100, y = 45, txt = pl_name)

    # Add playlist properties
    user_name = latinify(json["owner"]["display_name"])
    song_count = json["tracks"]["total"]
    song_likes = json["followers"]["total"]
    duration = 0

    # get total ms
    for track in tracks:
        duration += track["track"]["duration_ms"]

    # get duration string from milliseconds
    duration = millis_to_string(duration)

    # Create playlist properties next to playlist cover
    pdf.set_font('Helvetica', '', 20)
    pdf.text(x = 100, y = 65, txt = "by " + user_name)
    pdf.text(x = 100, y = 75, txt =  str(song_likes) + (" Likes" if song_likes != 1 else " Like"))
    pdf.text(x = 100, y = 85, txt = str(song_count) + (" Songs" if song_count != 1 else " Song"))
    pdf.text(x = 100, y = 95, txt = duration)