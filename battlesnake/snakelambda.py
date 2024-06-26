import random
import typing
import json

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#702963",  # TODO: Choose color
        "head": "all-seeing",  # TODO: Choose head
        "tail": "hook",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def enemy_imminent(target_location, head_locations):
    surrounding = [
        (target_location[0]+1,target_location[1]),
        (target_location[0]-1,target_location[1]),
        (target_location[0],target_location[1]+1),
        (target_location[0],target_location[1]-1),
        (target_location[0],target_location[1])
        ]
    imminent = False
    for i in head_locations:
        if i in surrounding:
            print(f"SNAKE NEAR FOOD. SNAKE AT {i}")
            imminent = True
    return imminent
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print("MOVING")
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width-1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height-1:
        is_move_safe["up"] = False
    
    # Prevent the snake from hitting hazards
    hazards = game_state['board']['hazards']
    for i in hazards:
        if i["y"] == my_head["y"]:
            if i["x"] == my_head["x"]-1:
                is_move_safe["left"] = False
            if i["x"] == my_head["x"]+1:
                is_move_safe["right"] = False
        if i["x"] == my_head["x"]:
            if i["y"] == my_head["y"]-1:
                is_move_safe["down"] = False
            if i["y"] == my_head["y"]+1:
                is_move_safe["up"] = False
    
    # Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    # print(opponents)
    head_locations = []
    for snake in opponents:
        if snake['id'] != game_state['you']['id']:
            head_locations.append((snake["head"]["x"],snake["head"]["y"]))
        for i in snake["body"]:
            if i["y"] == my_head["y"]:
                if i["x"] == my_head["x"]-1:
                    is_move_safe["left"] = False
                if i["x"] == my_head["x"]+1:
                    is_move_safe["right"] = False
            if i["x"] == my_head["x"]:
                if i["y"] == my_head["y"]-1:
                    is_move_safe["down"] = False
                if i["y"] == my_head["y"]+1:
                    is_move_safe["up"] = False
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    food_distance = {}
    for index,value in enumerate(food):
        distancex = abs(value["x"]-my_head["x"])
        distancey = abs(value["y"]-my_head["y"])
        food_distance[index] = distancex+distancey
    closest = min(food_distance, key=food_distance.get)
    print(f"CLOSEST FOOD AT: {food[closest]}\nCURRENT HEAD AT: {my_head}\nSNAKES AT {head_locations}")
    priority = {}
    next_move = ''
    sketchy_moves = []
    if enemy_imminent((my_head["x"],my_head["y"]+1), head_locations) and "up" in safe_moves:
        safe_moves.remove("up")
        sketchy_moves.append("up")
    if enemy_imminent((my_head["x"],my_head["y"]-1), head_locations) and "down" in safe_moves:
        safe_moves.remove("down")
        sketchy_moves.append("down")
    if enemy_imminent((my_head["x"]+1,my_head["y"]), head_locations) and "right" in safe_moves:
        safe_moves.remove("right")
        sketchy_moves.append("right")
    if enemy_imminent((my_head["x"]-1,my_head["y"]), head_locations) and "left" in safe_moves:
        safe_moves.remove("left")
        sketchy_moves.append("left")
        
    if food[closest]["y"] == my_head["y"]+1 and food[closest]['x'] == my_head['x'] and "up" in safe_moves:
        next_move = "up"
    elif food[closest]["y"] == my_head["y"]-1 and food[closest]['x'] == my_head['x'] and "down" in safe_moves:
        next_move = "down"
    elif food[closest]["x"] == my_head["x"]+1 and food[closest]['y'] == my_head['y'] and "right" in safe_moves:
        next_move = "right"
    elif food[closest]["x"] == my_head["x"]-1 and food[closest]['y'] == my_head['y'] and "left" in safe_moves:
        next_move = "left"
    elif food[closest]["y"] > my_head["y"] and "up" in safe_moves:
        priority["up"] = abs(food[closest]["y"]-my_head["y"])
    elif food[closest]["y"] < my_head["y"] and "down" in safe_moves:
        priority["down"] = abs(food[closest]["y"]-my_head["y"])
    elif food[closest]["x"] > my_head["x"] and "right" in safe_moves:
        priority["right"] = abs(food[closest]["x"]-my_head["x"])
    elif food[closest]["x"] < my_head["x"] and "left" in safe_moves:
        priority["left"] = abs(food[closest]["x"]-my_head["x"])
    
    if next_move != '':
        pass
    elif priority:
        print(f'PRIORITY IS \n{priority}')
        next_move = min(priority, key=priority.get)
    elif safe_moves:
        print("Random Safe Move")
        next_move = random.choice(safe_moves)
    else:
        next_move = random.choice(sketchy_moves)
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def main(event, context):
    if event.get("body"):
        print(event['body'])
        gamestate = json.loads(event['body'])
    match event['rawPath']:
        case "/":
            return json.dumps(info())
        case "/move":
            return json.dumps(move(gamestate))
        case "/start":
            return json.dumps(start(gamestate))
        case "/end":
            return json.dumps(end(gamestate))
    return event