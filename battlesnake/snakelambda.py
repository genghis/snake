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
        
    # Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for snake in opponents:
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
    print(f"CLOSEST FOOD AT: {food[closest]}\nCURRENT HEAD AT: {my_head}")
    priority = {}
    next_move = ''
    
    if food[closest]["y"] == my_head["y"]+1 and "up" in safe_moves:
        next_move = "up"
    elif food[closest]["y"] == my_head["y"]-1 and "down" in safe_moves:
        next_move = "down"
    elif food[closest]["x"] == my_head["x"]+1 and "right" in safe_moves:
        next_move = "right"
    elif food[closest]["x"] == my_head["x"]-1 and "left" in safe_moves:
        next_move = "left"
    elif food[closest]["y"] > my_head["y"]+1 and "up" in safe_moves:
        priority["up"] = abs(food[closest]["y"]-my_head["y"])
    elif food[closest]["y"] < my_head["y"]-1 and "down" in safe_moves:
        priority["down"] = abs(food[closest]["y"]-my_head["y"])
    elif food[closest]["x"] > my_head["x"]+1 and "right" in safe_moves:
        priority["right"] = abs(food[closest]["x"]-my_head["x"])
    elif food[closest]["x"] < my_head["x"]-1 and "left" in safe_moves:
        priority["left"] = abs(food[closest]["x"]-my_head["x"])
    
    if next_move != '':
        pass
    elif priority:
        print(f'PRIORITY IS \n{priority}')
        next_move = min(priority, key=priority.get)
    else:
        next_move = random.choice(safe_moves)
    # certainty = []
    # possibilities = {}
    # for move in safe_moves:
    #     match move:
    #         case "up":
    #             if food[closest]["y"] > my_head["y"]:
    #                 possibilities["up"] = abs(food[closest]["y"] - my_head["y"])
    #         case "down":
    #             if food[closest]["y"] < my_head["y"]:
    #                 possibilities["down"] = abs(food[closest]["y"] - my_head["y"])
    #         case "left":
    #             if food[closest]["x"] < my_head["x"]:
    #                 possibilities["left"] = abs(food[closest]["x"] - my_head["x"])
    #         case "right":
    #             if food[closest]["x"] > my_head["x"]:
    #                 possibilities["right"] = abs(food[closest]["x"] - my_head["x"])
    
    # if possibilities:
    #     next_move = min(possibilities, key=possibilities.get)
    # else:
    #     next_move = random.choice(safe_moves)
    
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