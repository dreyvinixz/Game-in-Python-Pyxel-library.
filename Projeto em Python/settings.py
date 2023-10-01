import pyxel as px
import math


class Character:
    def __init__(self, x, y, image_id, u, v, w, h, name, level, hp, pv):
        self.x = x
        self.y = y
        self.image_id = image_id
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.health = hp  # Valor inicial de vida
        self.shield = pv  # Valor inicial de escudo
        self.name = name  # Nome do personagem
        self.level = level  # Nível do personagem
        self.hp = 200  # Pontos de vida do personagem
        self.pv = 100  # Pontos de escudo do personagem
        self.shield_bar_width = 40  # Largura total da barra de escudo
        self.hp_bar_width = 40  # Largura total da barra de vida
        self.angle = 0  # angle inicial

    def update(self, dx, dy, screen_width, screen_height):
        new_x = self.x + dx
        new_y = self.y + dy

        # Verifique se o jogador saiu dos limites da tela
        if new_x < 0:
            new_x = screen_width - self.w  # Aparece do lado direito da tela
        elif new_x > screen_width - self.w:
            new_x = 0  # Aparece do lado esquerdo da tela

        if new_y < 0:
            new_y = screen_height - self.h  # Aparece na parte de baixo da tela
        elif new_y > screen_height - self.h:
            new_y = 0  # Aparece na parte de cima da tela

        self.x = new_x
        self.y = new_y

    # Função para determinar as coliçoes de obajetos na tela:
    def check_collision_with_trees(self, x, y):
        tree_positions = [
            (0, 0, 37, 37)
            # (6, y + 5, 37, 37),  # primeira linha à esquerda
            # (x, px.height - 515, 37, 37),  # linha de árvores inferior
            # (x, px.height - 46, 37, 37),  # linha de árvores inferior
        ]
        for tree_x, tree_y, tree_w, tree_h in tree_positions:
            if (
                x + self.w > tree_x and
                x < tree_x + tree_w and
                y + self.h > tree_y and
                y < tree_y + tree_h
            ):
                return True
        return False

    def draw(self):
        px.blt(
            self.x,
            self.y,
            self.image_id,
            self.u,
            self.v,
            self.w,
            self.h,
            px.COLOR_WHITE,
        )

    # funçao que determina os ataques dos mobs sobre os jogadores
    def take_damage(self, damage):
        if self.shield > 0:
            # Reduza o escudo se estiver ativo
            self.shield -= damage
            # Certifique-se de que o escudo nunca seja menor que 0
            self.shield = max(0, self.shield)
            self.shield_bar_width = int((self.shield / 50) * 40)
        else:
            # Se o escudo estiver zerado, reduza a vida
            self.health -= damage
            # Certifique-se de que a vida nunca seja menor que 0
            self.hp = max(0, self.health)
            self.hp_bar_width = int((self.hp / 200) * 40)

    # Função para a configuraçõses das barras
    def update_status_bars(self):
        self.shield_bar_width = int((self.pv / 50) * 40)

    # Função que delimita a confição para meus players estarem vivos ou mortos
    def is_alive(self):
        return self.health > 0

    # Função para os meus mobs seguirem a posiçaão dos meus players
    def move_towards_player(self, player_x, player_y, speed):
        dx = player_x - self.x
        dy = player_y - self.y
        angle = math.atan2(dy, dx)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        self.x += dx
        self.y += dy

# heranças de classe aplicada:


class MobPlayer1(Character):
    def __init__(self, x, y, image_id, u, v, w, h, name, level, hp, pv):
        super().__init__(x, y, image_id, u, v, w, h, name, level, hp, pv)
        self.hp_bar_width = 40  # Largura total da barra de vida
        self.hp = 100  # MobPlayer1 tem 100 de vida
        self.pv = 75  # MobPlayer1 tem 75 de escudo
        self.dropped_item = None  # Inicialmente, o mob não tem um item para dropar

    def update(self, player):
        distance_to_player1 = math.sqrt(
            (player.x - self.x) ** 2 + (player.y - self.y) ** 2)

        if distance_to_player1 <= 40:
            # Se o player1 estiver dentro da distância de ataque, cause dano ao player1
            self.deal_damage_to_player(player)

    def deal_damage_to_player(self, player):
        distance = math.sqrt((player.x - self.x) ** 2 +
                             (player.y - self.y) ** 2)

        if distance <= 40:
            if player.pv > 0:
                # Reduz o escudo se estiver ativo
                player.pv -= 0.2
                player.shield_bar_width = max(0, int((player.pv / 50) * 40))
            else:
                if player.hp > 0:
                    # Se o escudo estiver zerado, reduza a vida (se a vida ainda for maior que 0)
                    player.take_damage(0.2)  # dano do mob


class MobPlayer2(Character):
    def __init__(self, x, y, image_id, u, v, w, h, name, level, hp, pv):
        super().__init__(x, y, image_id, u, v, w, h, name, level, hp, pv)
        self.hp_bar_width = 40  # Largura total da barra de vida
        self.hp = 100  # MobPlayer2 tem 100 de vida
        self.pv = 75  # MobPlayer2 tem 75 de escudo
        self.dropped_item = None

    def update(self, player2):
        distance_to_player2 = math.sqrt(
            (player2.x - self.x) ** 2 + (player2.y - self.y) ** 2)

        if distance_to_player2 <= 40:
            # Se o player2 estiver dentro da distância de ataque, cause dano ao player2
            self.deal_damage_to_player(player2)

    def deal_damage_to_player(self, player):
        distance = math.sqrt((player.x - self.x) ** 2 +
                             (player.y - self.y) ** 2)
        if distance <= 40:
            if player.pv > 0:
                # Reduz o escudo se estiver ativo
                player.pv -= 0.2
                player.shield_bar_width = max(0, int((player.pv / 50) * 40))
            else:
                if player.hp > 0:
                    # Se o escudo estiver zerado, reduza a vida (se a vida ainda for maior que 0)
                    player.take_damage(0.2)  # dano do mob


class Player(Character):
    def __init__(self, x, y, image_id, u, v, w, h, name, level):
        super().__init__(x, y, image_id, u, v, w, h, name, level)
        self.hp = 100
        self.pv = 50


class Player2(Character):
    def __init__(self, x, y, image_id, u, v, w, h, name, level):
        super().__init__(x, y, image_id, u, v, w, h, name, level)
        self.hp = 100
        self.pv = 50


class Portions_hp:  # Função que define as configurações e desenhp para minha porção de hp
    def __init__(self, x, y, player, player2):
        self.x = x
        self.y = y
        self.player = player
        self.player2 = player2
        self.image_id = 2  # ID da imagem
        self.u = 0  # Coordenada U da imagem
        self.v = 35  # Coordenada V da imagem
        self.w = 38  # Largura da imagem
        self.h = 32  # Altura da imagem
        self.name = "Portions_hp"  # nome
        self.level = 1  # nivel

    def draw(self):
        px.blt(self.x + 5, self.y + 5, 2, self.u, self.v,
               self.w, self.h, 0)  # desenha a porção

    # define as colisões com meu player1
    def check_collision_and_apply_effect_player1(self, player):
        if (
            self.player.is_alive() and
            self.x + self.w > player.x and
            self.x < player.x + player.w and
            self.y + self.h > player.y and
            self.y < player.y + player.h
        ):
            if self.name == "Portions_hp":
                # Restaure +100 de HP, limitado a 200
                player.health += 20
            # A porção foi coletada, retorne True para indicar que deve ser removida
            return True
        # A porção não foi coletada, retorne False
        return False

    # define as colisões com meu player2
    def check_collision_and_apply_effect_player2(self, player2):
        if (
            self.player2.is_alive() and
            self.x + self.w > player2.x and
            self.x < player2.x + player2.w and
            self.y + self.h > player2.y and
            self.y < player2.y + player2.h
        ):
            if self.name == "Portions_pv":
                # Restaure +100 de HP, limitado a 200
                player2.pv += 20
            # A porção foi coletada, retorne True para indicar que deve ser removida
            return True
        # A porção não foi coletada, retorne False
        return False


class Portions_pv:  # Função que define as configurações e desenho para minha porção de pv
    def __init__(self, x, y, player, player2):
        self.x = x
        self.y = y
        self.player = player
        self.player2 = player2
        self.image_id = 2  # ID da imagem
        self.u = 0  # Coordenada U da imagem
        self.v = 35  # Coordenada V da imagem
        self.w = 32  # Largura da imagem
        self.h = 32  # Altura da imagem
        self.name = "Portions_pv"  # nome
        self.level = 1  # nivel

    def draw(self):
        px.blt(self.x + 5, self.y + 5, 2, 35, 35, 38, 32, 0)

    # define as colisões com meu player2
    def check_collision_and_apply_effect_player1(self, player):
        if (
            self.player.is_alive() and
            self.x + self.w > player.x and
            self.x < player.x + player.w and
            self.y + self.h > player.y and
            self.y < player.y + player.h
        ):
            if self.name == "Portions_pv":
                # Restaure +100 de HP, limitado a 200
                player.pv += 20
            # A porção foi coletada, retorne True para indicar que deve ser removida
            return True
        # A porção não foi coletada, retorne False
        return False

    # define as colisões com meu player2
    def check_collision_and_apply_effect_player2(self, player2):
        if (
            self.player2.is_alive() and
            self.x + self.w > player2.x and
            self.x < player2.x + player2.w and
            self.y + self.h > player2.y and
            self.y < player2.y + player2.h
        ):
            if self.name == "Portions_pv":
                # Restaure +100 de HP, limitado a 200
                player2.pv += 20
            # A porção foi coletada, retorne True para indicar que deve ser removida
            return True
        # A porção não foi coletada, retorne False
        return False


class PlayerAttack:  # atacck dos meu player1
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]


class Player2Attack:  # atack do meu player2
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]


class Ball:
    def __init__(self, x, y, value, color):
        self.x = x
        self.y = y
        self.value = value
        self.color = color

# ----------------------------------------------------------------
# aplicações a serem relizadas posteriomente:

# class Potion_Animation_Player(Character):
#     def __init__(self, x, y, image_id, u, v, h, name, level):
#         super().__init__(x, y, image_id, u, v, h, name, level)


# class Potion_Animation_Player2(Character):
#     def __init__(self, x, y, image_id, u, v, h, name, level):
#         super().__init__(x, y, image_id, u, v, h, name, level)

# class Super_Atacks_1(Character):
#     def __init__(self, x, y, image_id, u, v, h, name, level):
#         super().__init__(x, y, image_id, u, v, h, name, level)


# class Super_Atacks_2(Character):
#     def __init__(self, x, y, image_id, u, v, h, name, level):
#         super().__init__(x, y, image_id, u, v, h, name, level)

# ----------------------------------------------------------------
