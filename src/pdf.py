from fpdf import FPDF

def __from_millis(millis):
    """ 
    Task an amount of milliseconds and returns the calculated hours, seconds and minutes from it
    """
    # calc
    seconds = (millis /1000 ) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24

    # return tuple
    return hours, minutes, seconds

def __millis_to_string(millis):
    """
    Takes an amount of milli seconds and into a string formmated like this: 0h 0min 0s
    """

    # get from main method
    hours, minutes, seconds = __from_millis(millis)

    # add seconds
    result = "%ds" % (seconds)

    # add minutes if there are some
    if minutes >= 1:
        result = "%dmin " % (minutes) + result

    # add hours if there are some
    if hours >= 1:
        result = "%dh " % (hours) + result

    return result

def __millis_to_duration(millis):
    """
    Taskes an amount of milli seconds and turns it into a string formatted like this: mins:seconds
    """

    # get from main method (minutes are calculated from hour, so they're not assigned to a variable)
    hours, _, seconds = __from_millis(millis)

    return ("%d:%d" if seconds >= 10 else "%d:0%d" ) % (60 * hours, seconds)

def __latinify(str):
    """
    Removes special characters like emojis from the string (fpdf cant handle them) and returns it
    """
    return str.encode('ascii', 'ignore').decode('ascii')

def create_pdf(json):
    # Create default pdf setttings and add first page
    pdf = FPDF()
    pdf.set_font('Helvetica', '', 16)
    pdf.add_page()
    pdf.image('res/background.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
    pdf.set_text_color(255, 255, 255)

    # Set default variables
    tracks = json["tracks"]["items"]

    # Get playlist url
    pl_url = json["external_urls"]["spotify"]

    # Add playlist cover to pdf
    img_url = json["images"][0]["url"]
    pdf.image(name = img_url, x = 20, y = 20, h = 75, link = pl_url)

    # Add playlist name
    pl_name = __latinify(json["name"])

    pdf.set_font('Helvetica', 'B', 44)
    pdf.text(x = 100, y = 45, txt = pl_name)

    # Add playlist properties
    user_name = __latinify(json["owner"]["display_name"])
    song_count = json["tracks"]["total"]
    song_likes = json["followers"]["total"]
    duration = 0

    # get total ms
    for track in tracks:
        duration += track["track"]["duration_ms"]

    # get duration string from milliseconds
    duration = __millis_to_string(duration)

    # Create playlist properties next to playlist cover
    pdf.set_font('Helvetica', '', 20)
    pdf.text(x = 100, y = 65, txt = "by " + user_name)
    pdf.text(x = 100, y = 75, txt =  str(song_likes) + (" Likes" if song_likes != 1 else " Like"))
    pdf.text(x = 100, y = 85, txt = str(song_count) + (" Songs" if song_count != 1 else " Song"))
    pdf.text(x = 100, y = 95, txt = duration)

    # vars for for loop
    current_track = 1
    page_track = 1
    first_page = True

    for track in tracks:
        track = track["track"]

        # Get json properties
        track_name = __latinify(track["name"])
        track_duration = __millis_to_duration(track["duration_ms"])
        track_url = track["external_urls"]["spotify"]
        track_img_url = track["album"]["images"][1]["url"]
        track_artists = ""

        # Join artists into string
        for artist in track["artists"]:
            if track_artists != "":
                track_artists += ", "

            track_artists += __latinify(artist["name"])

        if len(track_artists) >= 38:
            track_artists = track_artists[0:38] + "..."

        # add new page if no space is avaliable for more tracks
        if (first_page and page_track > 8) or page_track > 13:
            pdf.add_page()
            pdf.image('res/background.png', x = 0, y = 0, w = 210, h = 297, type = '', link = '')
            page_track = 1
            first_page = False

        # calculate y pos for track
        height = page_track * 20 + (105 if first_page else 10)
        
        # Add track number
        pdf.text(x = 20, y = height, txt = str(current_track))
        
        # Add cover
        pdf.image(name = track_img_url, x = 35, y = height - 10, h = 15, link = track_url)

        # Track name 
        pdf.set_font('Helvetica', '', 16)
        pdf.text(x = 60, y = height - 3, txt = track_name)
        
        # track artis under name
        pdf.set_font('Helvetica', '', 14)
        pdf.set_text_color(179, 179, 179)
        pdf.text(x = 60, y = height + 3, txt = track_artists)
        pdf.set_text_color(255, 255, 255)
        
        # Add duration
        pdf.set_font('Helvetica', '', 20)    
        pdf.text(x = 180, y = height, txt = track_duration)

        page_track += 1
        current_track += 1

    # Return base64 string of pdf
    return pdf.output(dest="S")