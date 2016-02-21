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
    height = data['height']
    width = data['width']
    print "width: ", width, "height: ", height
    return {
        'taunt': 'Hide yo kidsssssssssss'
    }


@bottle.post('/move')
def move():
    snake = getSnake()
    if snake['health'] < 15:
        hungry = True
    else:
        hungry = False
        
    if(hungry): 
        return {
            'move': get_food(),
            'taunt': 'MY BATTALION REQUIRES NOURISHMENT'
        }
    else:
        return {
            'move': avoid_walls(),
            'taunt': 'HIDE YO KIDS'
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

def get_food():
    data = bottle.request.json
    height = data['height']
    width = data['width']
    turn = data['turn']
    food = data['food']
    snake = getSnake()
    coordinates = snake['coords']
    direction = ''
    foodfound = False
    
    snakehead = coordinates[0]
    for i in range(snakehead[0]-2, snakehead[0]+3):
        for j in range(snakehead[1]-2, snakehead[1]+3):
            if [i,j] in food:
                nextfood = [i,j]
                foodfound = True
                
    coords = snake['coords']
                
    if foodfound:
        if snakehead[0] < nextfood[0]:
            if coords[1][0] != snakehead[0]+1:
                return 'east'
        if snakehead[0] > nextfood[0]:
            if coords[1][0] != snakehead[0]-1:
                return 'west'
        if snakehead[1] < nextfood[1]:
            if coords[1][1] != snakehead[1]-1:
                return 'north'
        if snakehead[1] > nextfood[1]:
            if coords[1][1] != snakehead[1]+1:
                return 'south'
    else: 
        return avoid_walls()    

def avoid_walls():
    data = bottle.request.json
    height = data['height']
    width = data['width']
    turn = data['turn']
    snake = getSnake()
    coordinates = snake['coords']
    direction = ''
    
    
    
    snakehead = coordinates[0]
    
    print "curr coords: ", coordinates[0]
    #case snake hits left wall
    direction = 'east'

    if snakehead[0] == 0:
        if snakehead[1] == 0:
            return 'east'
        print "on turn ", turn, " we hit the left wall and go north"
        return 'north'
    #case snake hits right wall
    if snakehead[0] == width-1:
        if snakehead[1] == height-1:
            return 'west'
        print "on turn ", turn, " we hit the right wall and go south"
        return 'south'
    #case snake hits top
    if snakehead[1] == 0:
        if snakehead[0] == width-1:
            return 'south'
        print "on turn ", turn, " we hit the top and go east"
        return 'east'
    #case snake hits bottom
    if snakehead[1] == height-1:
        if snakehead[0] == 0:
            return 'north'
        print "on turn ", turn, " we hit the bottom and go west"
        return 'west' 
    # snake hits nothing
    
    print "on turn ", turn, " we continue in last direction"
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
