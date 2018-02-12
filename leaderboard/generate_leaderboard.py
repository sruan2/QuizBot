import imgkit # make sure this is installed

background_url = 'https://i.imgur.com/fv11FXD.png' # image must be hosted

top_users = [('Dave', 13400), ('Dan', 12000), ('Melissa', 11023), ('Daniel', 11002), ('Arthur', 9002)]
cur_user = (52, 'Brian', 1052) # (rank, name, score)

font = '<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">'
css = '<style>.fifth,.first,.fourth,.second,.third,.you{position:absolute}.container{font-size:1.8em;font-family:Raleway,sans-serif}.top-rank,.your-rank{left:60px;font-size:1.2em}.first{top:220px}.second{top:319px}.third{top:418px}.fourth{top:517px}.fifth{top:616px}.you{top:745px}.name,.score,.top-rank,.your-rank{position:relative}.your-rank{color:orange}.name{left:150px;bottom:35px}.score{left:350px;bottom:70px}</style>'

body ='<div class="container"><img src="'+background_url+'"/>' + \
    '<div class="first"><div class="top-rank">1</div><div class="name">'+str(top_users[0][0])+'</div><div class="score">'+str(top_users[0][1])+'</div></div>' + \
    '<div class="second"><div class="top-rank">2</div><div class="name">'+str(top_users[1][0])+'</div><div class="score">'+str(top_users[1][1])+'</div></div>' + \
    '<div class="third"><div class="top-rank">3</div><div class="name">'+str(top_users[2][0])+'</div><div class="score">'+str(top_users[2][1])+'</div></div>' + \
    '<div class="fourth"><div class="top-rank">4</div><div class="name">'+str(top_users[3][0])+'</div><div class="score">'+str(top_users[3][1])+'</div></div>' + \
    '<div class="fifth"><div class="top-rank">5</div><div class="name">'+str(top_users[4][0])+'</div><div class="score">'+str(top_users[4][1])+'</div></div>' + \
    '<div class="you"><div class="your-rank">'+str(cur_user[0])+'</div><div class="name">'+str(cur_user[1])+'</div><div class="score">'+str(cur_user[2])+'</div></div></div>'

html = font + css + body

options = {
    'format': 'png',
    'crop-h': '890', # assume dimensions
    'crop-w': '500', # assume dimensions
    'crop-x': '8',
    'crop-y': '8'
}
imgkit.from_string(html, 'leaderboard.png', options=options) # output leaderboard.png
