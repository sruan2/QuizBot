import imgkit # make sure this is installed
import uuid

def generate(top_5_users, current_user, background_url = 'https://www.smartprimer.org:8443/pictures/leaderboard_background.png'):
    """Generates a leaderboard using the provided input.
    Args: (see if __name__ == "__main__" for example)
        top_5_users ([(str, str, int)]): list of tuples for the top 5 users in the form (firstname, lastname, score).
        current_user ((str str, int, int)): the current user in the form (firstname, lastname, score, rank).
        background_url (str): the URL of the background image (must be hosted online for some reason?).
    Returns:
        output_url (str): URL of the output image.
    """
    length = max(5, len(top_5_users))
    names = [top_5_users[i][0]+' '+top_5_users[i][1] for i in range(length)]
    font = '<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">'
    css = '<style>.place5,.place1,.place4,.place2,.place3,.you{position:absolute}.container{font-size:1.8em;font-family:Raleway,sans-serif}.top-rank,.your-rank{left:60px;font-size:1.2em}.place1{top:220px}.place2{top:319px}.place3{top:418px}.place4{top:517px}.place5{top:616px}.you{top:745px}.name,.score,.top-rank,.your-rank{position:relative}.your-rank{color:orange}.name{left:130px;bottom:34px}.score{left:350px;bottom:68px}</style>'
    body ='<div class="container"><img src="'+background_url+'"/>' 

    for i in range(length):
        body +=  '<div class="place1"><div class="top-rank">1</div><div class="name">'+names[i]+'</div><div class="score">'+str(top_5_users[i][2])+'</div></div>'

    body += '<div class="you"><div class="your-rank">'+str(int(current_user[3]))+'</div><div class="name">'+current_user[0]+' '+current_user[1]+'</div><div class="score">'+str(current_user[2])+'</div></div></div>'
    html = font + css + body
    options = {
        'format': 'png',
        'crop-h': '445',    # must have height = 890px (see zoom)
        'crop-w': '250',    # must have width = 500px (see zoom)
        'crop-x': '4',
        'crop-y': '4',
        'zoom': 0.5,        # reduce dimensions in half
        # 'xvfb': ''
    }
    output_name = 'leaderboard_'+uuid.uuid4().hex+'.png'
    output_location = 'https://www.smartprimer.org:8443/tmp/pictures/'
    imgkit.from_string(html, "./tmp/pictures/"+output_name, options=options)
    print (output_location + output_name)
    return output_location + output_name

if __name__ == "__main__":
    top_5_users = [('Dave', 'Johnson', 13400), ('Dan', 'Abraham', 12000), ('Melissa', 'Mack', 11023), ('Daniel', 'Hayes', 11002), ('Arthur', 'Audrey', 9002)]
    current_user = ('Brian', 'Chen', 1052, 52)
    background_url = 'https://i.imgur.com/fv11FXD.png'
    output_url = generate(top_5_users, current_user, background_url)
    print(output_url)
