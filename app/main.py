import bottle
import os


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = 'http://i.imgur.com/tWoo7jR.png' 
    
    return {
        'color': '#00ff77',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json
    # TODO: Do things with data
    return {
        'taunt': 'Hide yo kidsssssssssss'
    }


@bottle.post('/move')
def move():
     # TODO: Do things with data
    return {
        'move': avoid_walls(),
        'taunt': 'LETS GOOOOOOOOOOOOOOOOOOOOOOO'
    }

@bottle.post('/end')
def end():
    data = bottle.request.json
    # TODO: Do things with data
    return {
        'taunt': 'kony has trained another hundred child soldiers during this game'
    }

def getSnake():
    data = bottle.request.json
    our_id = 'f023067e-5411-407e-b445-04fad300ef6c'
    allsnakes = data['snakes']
    our_snake = None
    
    for i in range(len(allsnakes)):

        curr_snake = allsnakes[i]
        if curr_snake['id'] == our_id:
            our_snake = allsnakes[i]
            break
    return our_snake;


def avoid_walls():
    data = bottle.request.json
    height = data['height']
    width = data['width']
    snake = getSnake()
    coordinates = snake['coords']
    direction = ''
    print coordinates[0]
    if coordinates[0][0] == 1:
        direction = 'north'
    if coordinates[0][0] == width-1:
        direction = 'south'
    if coordinates[0][1] == 1:
        direction = 'east'
    if coordinates[0][1] == height-1:
        direction = 'west' 
    else:
        direction = 'east'            

    return direction
  
def get_enemycoords():
    data = bottle.request.json
    enemy_coords = []
    our_id = 'f023067e-5411-407e-b445-04fad300ef6c'
    allsnakes = data['snakes']

    for i in range(len(allsnakes)):
        curr_snake = allsnakes[i]
        if curr_snake['id'] != our_id:
            enemy_coords.append(curr_snake['coords'])

    return enemy_coords 

    

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
