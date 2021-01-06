from play import play

def player_status():
    player = []
    player.append(['MY','human'])
    player.append(['C1','com'])
    player.append(['C2','com'])
    player.append(['MY','com'])
    return player

if __name__ == "__main__":
    one_game = play.OneGame(player_status(),6,500)
    one_game.play()