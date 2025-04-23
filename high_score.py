import config

def load_high_score():
    try:
        with open(config.HIGH_SCORE_FILE, 'r') as file:
            score = int(file.read().strip())
            return score
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Erro ao carregar o recorde: {e}")
        return 0

def save_high_score(score):
    try:
        with open(config.HIGH_SCORE_FILE, 'w') as file:
            file.write(str(score))
        print(f"Novo recorde salvo: {score}")
    except Exception as e:
        print(f"Erro ao salvar o recorde: {e}")

def update_high_score(current_score):
    if current_score > config.high_score:
        config.high_score = current_score
        save_high_score(current_score)
        print(f"Novo recorde estabelecido: {current_score}!")
        return True
    return False