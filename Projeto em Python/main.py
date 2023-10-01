import pyxel as px  # importa a blibioteca pyxel
import math
import random
# Importe a classe Sounds e Sound_Track no arquivo effectts_sounds
from effects_sounds import Sounds, Sound_Track
# Importe a classes do arquivo settings
from settings import Character, MobPlayer1, MobPlayer2, PlayerAttack, Player2Attack, Ball, Portions_hp, Portions_pv

# defina o escore do player1 inicimente 0 usando para variavel global player
player1_score = 0
# defina o escore do player2 inicimente 0 usando para variavel global player
player2_score = 0
global_angle = 0  # define o angulo inicial 0 usando para variavel global angle


class Game:
    def __init__(self):
        # configurações de estado
        self.is_menu_open = False
        self.menu_options = [
            "Resume (Tab)", "Resolution", "Audio", "Tutorial", "Game Settings"]  # lista de opções para o menu
        self.selected_option = 0  # seleção inicial e 0
        self.game_state = "INICIANDO"  # estado do jogo de inicio
        self.is_game_running = False  # inicialmente o o jogo esta em false
        self.is_waiting_for_restart = False  # restard do jogo em false
        # ----------------------------------------------------------------
        # codernadas x, y, image_id, u, v, w, h, name, level, hp, pv
        self.player = Character(
            545, 280, 0, 0, 60, 30, 41, "Player 1", 1, 200, 100
        )
        self.player2 = Character(
            545, 320, 0, 0, 0, 28, 37, "Player 2", 1, 200, 100
        )
        # ----------------------------------------------------------------
        # listas
        self.mobs1 = []  # listas de mobs1
        self.mobs2 = []  # listas de mobs2
        self.player_bullets = []
        self.player2_bullets = []
        self.player_attacks = []  # listas de atacks do player1
        self.player2_attacks = []  # lista de atacks do player2
        self.portions_hp = []  # lista de porções de hp
        self.portions_pv = []  # listas de porções de pv
        self.portions_list = []  # Inicializa a lista geral de porções
        # Adicione as porções de HP à lista geral de porções
        self.portions_list.extend(self.portions_hp)
        # Adicione as porções de PV à lista geral de porções
        self.portions_list.extend(self.portions_pv)
        self.balls = []  # litas de bolinhas
        self.mob1_positions = []  # lista para rastrear a posição do mob1
        self.mob2_positions = []  # lista para rastrear a posição do mo2

        # configurações para o update
        self.spawn_timer = 0  # tempo inicial dos spawn do mob1 e 0
        self.spawn_timer2 = 0  # tempo inicial do spaw do mob2 e 0
        self.score = 0  # escore do player1 inicia com 0
        self.score2 = 0  # escore do player2 inicia com 0

        # chamo as imagens usadas para meu jogo
        px.image(0).load(0, 0, "pixel_npc_red_animation.jpg")
        px.image(1).load(0, 0, "oryx_creatures_preview_2x.gif")
        px.image(2).load(0, 0, "portions_and_super_atacks.png")
        px.run(self.update, self.draw)

    def update(self):
        if self.game_state == "INICIANDO":  # estado inicial do meu jogo
            if px.btnp(13):  # quando enter e apertado  inicia meu jogo
                self.is_game_running = True  # mudo a execução para verdadeiro
                self.game_state = "EM_EXECUCAO"  # jogo entra e um estado de execução
                self.is_menu_open = False  # abrir meu menu continua faslso

        elif self.game_state == "EM_EXECUCAO":  # game em execução
            if not self.is_game_running:
                return

            if px.btnp(9):  # abro o menu quando aperto Tab
                self.is_menu_open = not self.is_menu_open
                if self.is_menu_open:
                    sounds_manager_track.pause()  # Pausa a música ao abrir o menu
                else:
                    sounds_manager_track.resume()  # Retoma a música ao fechar o menu
            # navegação no menu
            if self.is_menu_open:
                if px.btnp(px.KEY_W) and self.selected_option > 0:
                    self.selected_option -= 1
                elif px.btnp(px.KEY_S) and self.selected_option < len(self.menu_options) - 1:
                    self.selected_option += 1
                elif px.btnp(13):  # Tecla Enter
                    if self.menu_options[self.selected_option] == "Resolution":
                        self.game_state = "RESOLUTION_MENU"

            else:
                # com meu game no estado de execução inicio as seguintes configurações:

                # Para o player1:
                # Usamos para permitir remover itens durante a iteração na lista de porções de hp
                for portion in self.portions_hp:
                    if portion.check_collision_and_apply_effect_player1(self.player):
                        # Remove a porção da lista se foi coletada
                        self.portions_hp.remove(portion)
                # agora para a lista de porções de pv
                for portion in self.portions_pv:
                    if portion.check_collision_and_apply_effect_player1(self.player):
                        # Remove a porção da lista se foi coletada
                        self.portions_pv.remove(portion)
                # Para o player2:
                for portion in self.portions_hp:
                    if portion.check_collision_and_apply_effect_player2(self.player2):
                        # Remove a porção da lista se foi coletada
                        self.portions_hp.remove(portion)
                for portion in self.portions_pv:
                    if portion.check_collision_and_apply_effect_player2(self.player2):
                        # Remove a porção da lista se foi coletada
                        self.portions_pv.remove(portion)

                # inicio minha track de fundo quando meu jogo entra em execução
                sounds_manager_track.sound_track.play()

                # Atualize a posição do jogador, passando os limites da tela
                self.player.update((px.btn(px.KEY_D) - px.btn(px.KEY_A)) * 2,
                                   (px.btn(px.KEY_S) - px.btn(px.KEY_W)) * 2, px.width, px.height)
                self.player2.update((px.btn(px.KEY_RIGHT) - px.btn(px.KEY_LEFT)) * 2,
                                    (px.btn(px.KEY_DOWN) - px.btn(px.KEY_UP)) * 2, px.width, px.height)

                # ----------------------------------------------------------------
                # ataque do player1
                global global_angle
                if px.btnp(px.KEY_Q):
                    global_angle += 90
                    if global_angle >= 360:
                        global_angle = 0

                if px.btnp(px.KEY_E):
                    global_angle -= 90
                    if global_angle < 0:
                        global_angle = 360 - 90

                if px.btnp(px.KEY_X):  # laçamneto do ataque
                    # som de atack iniciado quando x e pressionado
                    sounds_manager.play_hit_sound_player()

                    # Converta o ângulo para radianos
                    angle_radians = math.radians(global_angle)
                    # Calcule a nova direção com base no ângulo
                    direction = (math.cos(angle_radians), -
                                 math.sin(angle_radians))

                    # Crie o ataque com a nova direção
                    start_x = self.player.x + self.player.w // 2
                    start_y = self.player.y + self.player.h // 2
                    attack = PlayerAttack(start_x, start_y, 2, direction)
                    # guardo na lista de ataques do player1
                    self.player_attacks.append(attack)

                # ataque do player2
                if px.btnp(px.KEY_V):
                    global_angle += 90
                    if global_angle >= 360:
                        global_angle = 0

                if px.btnp(px.KEY_B):
                    global_angle -= 90
                    if global_angle < 0:
                        global_angle = 360 - 90

                if px.btnp(px.KEY_SPACE):
                    sounds_manager.play_hit_sound_player()

                    # Converta o ângulo para radianos
                    angle_radians = math.radians(global_angle)
                    # Calcule a nova direção com base no ângulo
                    attack_direction = (
                        math.cos(angle_radians), -math.sin(angle_radians))
                    # Crie o ataque com a nova direção

                    start_x = self.player2.x + self.player2.w // 2
                    start_y = self.player2.y + self.player2.h // 2
                    attack_speed = 3
                    player2_attack = Player2Attack(
                        start_x, start_y, attack_speed, attack_direction)
                    # guado na lista de attack do player2
                    self.player2_attacks.append(player2_attack)

                # ----------------------------------------------------------------

                # Verifica colisão dos ataques do jogador com os mobs
                # Cria uma lista para armazenar os ataques que devem ser removidos
                player_attacks_to_remove = []

                for attack in self.player_attacks:
                    attack.move()
                    mobs_hit = []  # Crie uma lista para armazenar os mobs atingidos por este ataque

                    for mob in self.mobs1 + self.mobs2:
                        if mob is not None and (
                            attack.x + 5 > mob.x and
                            attack.x < mob.x + mob.w and
                            attack.y + 5 > mob.y and
                            attack.y < mob.y + mob.h
                        ):
                            # Ataque atingiu o mob, causar dano
                            # Ajusta a quantidade de dano conforme necessário
                            mob.take_damage(20)
                            # Adicione o mob à lista de mobs1 atingidos
                            mobs_hit.append(mob)
                            sounds_manager.play_hit_sound_mob()  # som quando um mob leva hit

                    # Após verificar todos os mobs, verifique se o ataque atingiu algum mob
                    if mobs_hit:
                        # Adicione o ataque à lista de remoção
                        player_attacks_to_remove.append(attack)

                # Remova os ataques que atingiram os mobs da lista
                for attack in player_attacks_to_remove:
                    self.player_attacks.remove(attack)

                # Verifique colisão dos ataques do player2 com os mobs
                # Cria uma lista para armazenar os ataques do player2 que devem ser removidos
                player2_attacks_to_remove = []

                for player2_attack in self.player2_attacks:
                    player2_attack.is_vertical = global_angle in []
                    player2_attack.move()
                    mobs_hit = []  # Crie uma lista para armazenar os mobs atingidos por este ataque do player2

                    for mob in self.mobs1 + self.mobs2:
                        if mob is not None and (
                            player2_attack.x + 10 > mob.x and
                            player2_attack.x < mob.x + mob.w and
                            player2_attack.y + 2 > mob.y and
                            player2_attack.y < mob.y + mob.h
                        ):
                            # Ataque do player2 atingiu o mob, causar dano
                            # Ajusta a quantidade de dano conforme necessário
                            mob.take_damage(20)
                            # Adicione o mob à lista de mobs atingidos
                            mobs_hit.append(mob)
                            sounds_manager.play_hit_sound_mob()  # som quando um mob leva hit

                    # Após verificar todos os mobs, verifique se o ataque do player2 atingiu algum mob
                    if mobs_hit:
                        # Adicione o ataque do player2 à lista de remoção
                        player2_attacks_to_remove.append(player2_attack)

                # Remova os ataques do player2 que atingiram os mobs da lista
                for player2_attack in player2_attacks_to_remove:
                    self.player2_attacks.remove(player2_attack)

                # -------------------------------------------------------------------
                # lógica para dano dos mobs sobre jogadores
                if self.player.is_alive():
                    for mob in self.mobs1:
                        if mob is not None and mob.is_alive():
                            mob.move_towards_player(
                                self.player.x, self.player.y, 0.6)
                            mob.deal_damage_to_player(self.player)

                if self.player2.is_alive():
                    for mob in self.mobs2:
                        if mob is not None and mob.is_alive():
                            mob.move_towards_player(
                                self.player2.x, self.player2.y, 0.1)
                            mob.deal_damage_to_player(self.player2)

                # -------------------------------------------------------------------
                # define a lista mobs_to_remove
                mobs_to_remove = []
                # loop que verifica a morte dos mobs
                for mob in self.mobs1 + self.mobs2:
                    if mob is not None and not mob.is_alive():
                        # Adiciona o mob à lista de mobs para remoção
                        mobs_to_remove.append(mob)

                        # dropamento das porções de hp ou pv
                        if mob.dropped_item == "Portions_pv":
                            portion = Portions_pv(
                                mob.x, mob.y, self.player, self.player2)
                            self.portions_pv.append(portion)
                            if mob in self.mobs1:
                                self.mob1_positions.append((mob.x, mob.y))
                            elif mob in self.mobs2:
                                self.mob2_positions.append((mob.x, mob.y))
                        elif mob.dropped_item == "Portions_hp":
                            portion = Portions_hp(
                                mob.x, mob.y, self.player, self.player2)
                            self.portions_hp.append(portion)
                            if mob in self.mobs1:
                                self.mob1_positions.append((mob.x, mob.y))
                            elif mob in self.mobs2:
                                self.mob2_positions.append((mob.x, mob.y))

                        # cria as bolinhas quunado meus mobs morrem
                        elif mob in self.mobs1 + self.mobs2:
                            # Crie uma bolinha branca com valor 16
                            ball_color = 7
                            balls_to_add = [
                                Ball(mob.x, mob.y + 2, 16, ball_color),
                                Ball(mob.x - 6, mob.y + 10, 16, ball_color),
                                Ball(mob.x + 6, mob.y + 10, 16, ball_color),
                            ]
                            # Adicione as bolinhas à lista de bolinhas
                            self.balls.extend(balls_to_add)
                # Após o loop, remova os mobs que estão na lista de mobs para remoção
                for mob in mobs_to_remove:
                    if mob in self.mobs1:
                        self.mobs1.remove(mob)
                    elif mob in self.mobs2:
                        self.mobs2.remove(mob)
                # ----------------------------------------------------------------
                # loop que verifica a colisão dos ataques com as bolinhas
                balls_to_remove = []  # Cria uma lista para armazenar as bolinhas que devem ser removidas
                for ball in self.balls:
                    if (
                        self.player.is_alive() and
                        self.player.x + self.player.w > ball.x and
                        self.player.x < ball.x + 8 and
                        self.player.y + self.player.h > ball.y and
                        self.player.y < ball.y + 8
                    ):
                        # Player 1 pegou a bolinha
                        if ball.color == 7:  # Bolinha branca
                            self.score += 1
                        balls_to_remove.append(ball)

                    if (
                        self.player2.is_alive() and
                        self.player2.x + self.player2.w > ball.x and
                        self.player2.x < ball.x + 8 and
                        self.player2.y + self.player2.h > ball.y and
                        self.player2.y < ball.y + 8
                    ):
                        # Player 2 pegou a bolinha
                        if ball.color == 7:  # Bolinha branca
                            self.score2 += 1
                        balls_to_remove.append(ball)

                # Remova as bolinhas que foram pegas
                for ball in balls_to_remove:
                    if ball in self.balls:
                        self.balls.remove(ball)
                # ----------------------------------------------------------------
                # loop de vericações:
                for mob in self.mobs1:
                    mob.move_towards_player(self.player.x, self.player.y, 0.5)

                for mob2 in self.mobs2:
                    mob2.move_towards_player(
                        self.player2.x, self.player2.y, 0.5)

                for bullet in self.player_bullets:
                    bullet.update()

                for bullet2 in self.player2_bullets:
                    bullet2.update()
                # ----------------------------------------------------------------
                # chama as configurações dos status das barras de hp e pv dos meus players
                self.player.update_status_bars()
                self.player2.update_status_bars()
                # ------------------------------------------------------------------
                # condição para iniciar o estado de Game-Over
                if not self.player.is_alive() and not self.player2.is_alive():
                    self.is_game_running = False
                    self.game_state = "GAME_OVER"
                # ----------------------------------------------------------------
                # variveias para controlar o tempo de spawn dos mobs
                self.spawn_timer -= 1
                self.spawn_timer2 -= 1

                if self.spawn_timer <= 0:
                    self.spawn_mob()
                    self.spawn_timer = 800

                if self.spawn_timer2 <= 0:
                    self.spawn_mob2()
                    self.spawn_timer2 = 800
                # ----------------------------------------------------------------------

        elif self.game_state == "GAME_OVER":  # jogo entra em estado de Game-Over
            sounds_manager_track.pause()  # pausa a musica
            if px.btnp(13):  # se aperta enter
                self.restart_game()  # chama a função para reneciar o jogo

    # função para configurar o desenho do menu
    def draw_menu(self):
        px.rect(400, 150, 420, 280, 1)  # Retângulo de fundo do menu
        for i, option in enumerate(self.menu_options):
            color = px.COLOR_WHITE if i == self.selected_option else px.COLOR_GRAY
            px.text(575, 210 + i * 30, option, color)

    # função para renecio do jogo
    def restart_game(self):
        global player1_score, player2_score
        player1_score = 0
        player2_score = 0

        self.player = Character(
            545, 280, 0, 0, 60, 30, 41, "Player 1", 1, 200, 100
        )
        self.player2 = Character(
            545, 320, 0, 0, 0, 28, 37, "Player 2", 1, 200, 100
        )

        self.mobs1 = []
        self.mobs2 = []
        self.player_bullets = []
        self.player2_bullets = []
        self.player_attacks = []
        self.player2_attacks = []
        self.portions_hp = []
        self.portions_pv = []
        self.balls = []
        self.mob1_positions = []
        self.mob2_positions = []

        self.spawn_timer = 0
        self.spawn_timer2 = 0
        self.score = 0
        self.score2 = 0

        self.is_game_running = False
        self.is_waiting_for_restart = False
        self.mob_position = None
        self.mob2_position = None
        self.game_state = "INICIANDO"

    def draw(self):
        if self.game_state == "INICIANDO":  # Game em estado de iniciando
            # desenho:
            px.cls(0)
            px.text(545, 250, "Pressione Enter para iniciar",
                    px.frame_count % 16)

        elif self.game_state == "EM_EXECUCAO":  # Game em estado de execução
            # Desenho:
            px.cls(0)

            # Desenho para os ataques dos players:
            for attack in self.player_attacks:
                attack.move()
                px.circ(attack.x, attack.y, 5,  px.frame_count %
                        16)  # circulo para o atack do player1
            for player2_attack in self.player2_attacks:
                player2_attack.is_vertical = global_angle in [90, 270]
                player2_attack.move()
                if player2_attack.is_vertical:
                    # Desenhe a barra vertical (eixo y)
                    px.rectb(player2_attack.x, player2_attack.y,
                             2, 10, px.frame_count % 16)
                else:
                    px.rect(player2_attack.x, player2_attack.y,
                            10, 2,  px.frame_count % 16)

            # Desenhe da bolinha de score:
            for ball in self.balls:
                if ball.value == 16:
                    color = 10  # Cor roxa
                elif ball.value == 32:
                    color = 7  # Cor branca
                else:
                    color = 11  # Outra cor padrão, se necessário
                # desenha a bolinha com essas caracteristicas
                px.circ(ball.x, ball.y, 4, color)

            # Desenha minhas porções:
            for portion_hp in self.portions_hp:
                portion_hp.draw()

            for portion_pv in self.portions_pv:
                portion_pv.draw()

            # Desenha os meus players:
            self.player.draw()
            self.player2.draw()

            # ------------------------------------------------------------------
            # Desenha os mobs e as barras de status de hp e pv em cima das suas cabeças
            for mob in self.mobs1:
                if mob is not None:
                    px.blt(mob.x, mob.y, mob.image_id,
                           mob.u, mob.v, mob.w, mob.h, 0)
                    px.rect(mob.x - 10, mob.y - 10, mob.shield_bar_width, 4, 3)
                    px.rect(mob.x - 10, mob.y - 15, mob.hp_bar_width, 4, 8)
                    px.text(mob.x - len(mob.name) * 2, mob.y -
                            25, f"{mob.name} lvl {mob.level}", 7)

            for mob in self.mobs2:
                if mob is not None:
                    px.blt(mob.x, mob.y, mob.image_id,
                           mob.u, mob.v, mob.w, mob.h, 0)
                    px.rect(mob.x - 10, mob.y - 10, mob.shield_bar_width, 4, 3)
                    px.rect(mob.x - 10, mob.y - 15, mob.hp_bar_width, 4, 8)
                    px.text(mob.x - len(mob.name) * 2, mob.y -
                            25, f"{mob.name} lvl {mob.level}", 7)
            # ------------------------------------------------------------------
            # Desenha as barras de status dos players:
            px.rect(10, 10, 48, 8, 5)
            px.rect(10, 20, 85, 8, 5)
            px.rect(1082, 10, 48, 8, 5)
            px.rect(1082, 20, 85, 8, 5)
            px.rect(12, 12, self.player.hp_bar_width, 4, 8)
            px.rect(12, 22, self.player.shield_bar_width, 4, 6)
            px.rect(1084, 12, self.player2.hp_bar_width, 4, 8)
            px.rect(1084, 22, self.player2.shield_bar_width, 4, 6)
            # Desenha o Score:
            px.text(15, 40, f"Player 1 Score: {self.score}", 7)
            px.text(1084, 40, f"Player 2 Score: {self.score2}", 7)
            # ----------------------------------------------------------------------
        # Jogo em estado de Game-Over
        elif self.game_state == "GAME_OVER":
            px.cls(0)
            px.text(520, 240, "GAME OVER", 7)
            px.text(520, 260, f"Player 1 Score: {self.score}", 7)
            px.text(520, 280, f"Player 2 Score: {self.score2}", 7)
            px.text(520, 300, "Pressione Enter para jogar novamente", 7)

        # Desenha o Menu:
        if self.is_menu_open:
            self.draw_menu()
    # ----------------------------------------------------------------------
    # Função para definiar as configurações de spawn dos mobs
    # Mob1:

    def spawn_mob(self):
        # Crie 6 mobs "Elfos" com posições específicas
        mob = [
            (0, -50), (-100, 200),
            (680, -150), (940, -120),
            (0, 800), (400, 800)
        ]
        for x, y in mob:
            mob = MobPlayer1(x, y, 1, 195, 90, 28, 30, "Elfo", 1, 100, 50)
            # Determinar se o mob deve dropar uma Portion_pv, uma Portion_hp ou nada
            drop_chance = random.randint(1, 100)  # Chance aleatória de 1 a 100
            if drop_chance <= 15:  # 15% de chance de dropar algo
                # Escolha aleatoriamente entre Portion_pv e Portion_hp
                drop_item = random.choice(["Portions_pv", "Portions_hp"])
                if drop_item == "Portions_pv":
                    mob.dropped_item = "Portions_pv"
                else:
                    mob.dropped_item = "Portions_hp"
            # guarda na lista de mobs:
            self.mobs1.append(mob)
    # Mob2:

    def spawn_mob2(self):
        # Crie 5 mobs "Mummy" com posições específicas
        mob2 = [
            (1310, 280), (1350, 400),
            (1300, 600), (700, 800),
            (0, -200), (-100, 400)
        ]

        for x, y in mob2:
            mob2 = MobPlayer2(x, y, 1, 195, 232, 29, 30, "Mumy", 1, 200, 50)
            self.mobs2.append(mob2)
            # Determinar se o mob deve dropar uma Portion_pv, uma Portion_hp ou nada
            drop_chance = random.randint(1, 100)  # Chance aleatória de 1 a 100
            if drop_chance <= 15:  # 15% de chance de dropar algo
                # Escolha aleatoriamente entre Portion_pv e Portion_hp
                drop_item = random.choice(["Portions_pv", "Portions_hp"])
                if drop_item == "Portions_pv":
                    mob2.dropped_item = "Portions_pv"
                else:
                    mob2.dropped_item = "Portions_hp"
            # guarda na lista de mobs:
            self.mobs2.append(mob2)


# inicialização do pyxel:
if __name__ == "__main__":
    px.init(1200, 680, fps=60)  # Inicialize o Pyxel aqui
    sounds_manager = Sounds()  # Crie uma instância da classe Sounds
    # Crie uma instância da classe Sounds_Tracks
    sounds_manager_track = Sound_Track(volume=0.1)
    Game()  # inicia a classe Game

# ------------------------------------------------------------------------------
# partes a serem desenvollvidas posteriomente

    # self.Potion_Animation_Player = Character(
    #     300, 200, 0, 0, 93, 30, 30, "Potion_Aniamtion", 1, 100, 200
    # )
    # self.Potion_Animation_Player2 = Character(
    #     400, 200, 0, 0, 30, 30, 30, "Potion_Animation", 1, 100, 50
    # )
    # self.Super_Atacks_1 = Character(
    #     200, 400, 2, 0, 0, 45, 35, "Super_atacks", 1, 100, 100
    # )
    # self.Super_Atacks_2 = Character(
    #     300, 400, 2, 45, 0, 45, 35, "Super_atacks", 1, 100, 100
    # )

    # self.Potion_Animation_Player.draw()
    # self.Potion_Animation_Player2.draw()
    # self.Super_Atacks_1.draw()
    # self.Super_Atacks_2.draw()

# a ideia e criar super atacks como poderes e uma animação de para quando as porções forem usadas

# ------------------------------------------------------------------------------------------------------
