import imgkit # make sure this is installed

def generate(users_scores, cur_user_rank, background_url = 'https://www.smartprimer.org:8443/pictures/leaderboard_background.png'):
    """Generates a leaderboard using the provided input.

    Args: (see if __name__ == "__main__" for example)
        users_scores ([(str, int)]): list of names/scores, with the current user's name/score at the end.
        cur_user_rank (int): the rank of the current user.
        background_url (str): the URL of the background image (must be hosted online for some reason?).

    Returns:
        None: instead the image leaderboard.png is generated in the same folder.

    """
    font = '<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">'
    css = '<style>.fifth,.first,.fourth,.second,.third,.you{position:absolute}.container{font-size:1.8em;font-family:Raleway,sans-serif}.top-rank,.your-rank{left:60px;font-size:1.2em}.first{top:220px}.second{top:319px}.third{top:418px}.fourth{top:517px}.fifth{top:616px}.you{top:745px}.name,.score,.top-rank,.your-rank{position:relative}.your-rank{color:orange}.name{left:150px;bottom:35px}.score{left:350px;bottom:70px}</style>'
    body ='<div class="container"><img src="'+background_url+'"/>' + \
        '<div class="first"><div class="top-rank">1</div><div class="name">'+str(users_scores[0][0])+'</div><div class="score">'+str(users_scores[0][1])+'</div></div>' + \
        '<div class="second"><div class="top-rank">2</div><div class="name">'+str(users_scores[1][0])+'</div><div class="score">'+str(users_scores[1][1])+'</div></div>' + \
        '<div class="third"><div class="top-rank">3</div><div class="name">'+str(users_scores[2][0])+'</div><div class="score">'+str(users_scores[2][1])+'</div></div>' + \
        '<div class="fourth"><div class="top-rank">4</div><div class="name">'+str(users_scores[3][0])+'</div><div class="score">'+str(users_scores[3][1])+'</div></div>' + \
        '<div class="fifth"><div class="top-rank">5</div><div class="name">'+str(users_scores[4][0])+'</div><div class="score">'+str(users_scores[4][1])+'</div></div>' + \
        '<div class="you"><div class="your-rank">'+str(cur_user_rank)+'</div><div class="name">'+str(users_scores[5][0])+'</div><div class="score">'+str(users_scores[5][1])+'</div></div></div>'
    html = font + css + body
    options = {
        'format': 'png',
        'crop-h': '445',    # assume height = 890px (see zoom)
        'crop-w': '250',    # assume dimensions = 500px (see zoom)
        'crop-x': '4',
        'crop-y': '4',
        'zoom': 0.5,        # reduce dimensions in half
        # 'xvfb': ''
    }
    imgkit.from_string(html, 'leaderboard.png', options=options) # output leaderboard.png

if __name__ == "__main__":
    users_scores = [('Dave', 13400), ('Dan', 12000), ('Melissa', 11023), ('Daniel', 11002), ('Arthur', 9002), ('Brian', 1052)]
    cur_user_rank = 52
    generate(users_scores, cur_user_rank)
