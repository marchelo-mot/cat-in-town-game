import pygame
import sys
import math
from pygame.locals import QUIT
from random import randint
import subprocess

# Inicializar o Pygame
pygame.init()

# Configurações da tela e do cenário
largura_tela, altura_tela = 1200, 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo com Poção de Velocidade e Efeito Temporário")

# Cores
COR_TEXTO = (255, 255, 255)

# Carregar imagens
protagonista_img = pygame.image.load("protagonista.png")
inimigo_img_original = pygame.image.load("inimigo.png")
inimigo2_img_original = pygame.image.load("inimigo2.png")
gato_img_original = pygame.image.load("gato.png")
pocao_img_original = pygame.image.load("poção.png")
fundo_img = pygame.image.load("fundo.png")
fundo_img = pygame.transform.scale(fundo_img, (largura_tela, altura_tela))

# Redimensionar imagens
protagonista = pygame.transform.scale(protagonista_img, (40, 40))
tamanho_inimigo = (40, 40)
tamanho_gato = (30, 30)
tamanho_pocao = (30, 30)
gato_img = pygame.transform.scale(gato_img_original, tamanho_gato)
pocao_img = pygame.transform.scale(pocao_img_original, tamanho_pocao)

# Definir posição inicial e variáveis do protagonista
pos_protagonista = [largura_tela // 2, altura_tela // 2]
velocidade_protagonista = 5
vidas_protagonista = 3
invulneravel = False
tempo_invulneravel = 2000  # Tempo em milissegundos
ultimo_tempo_dano = 0

# Fonte para o contador de vidas, tempo e gatos
fonte = pygame.font.SysFont(None, 30)

# Configurações dos tiros
tiros = []
velocidade_tiro = 10
intervalo_tiro = 500  # Intervalo inicial de 0,5 segundos entre tiros
ultimo_tiro = pygame.time.get_ticks()

# Listas de inimigos e controle de tempo para novos inimigos
inimigos_lentos = []
inimigos_rapidos = []
tempo_inimigo_lento = pygame.time.get_ticks()
tempo_inimigo_rapido = pygame.time.get_ticks()
contador_inimigos_derrotados = 0  # Contador para a poção

# Configurações da poção de velocidade
pos_pocao = None
pocao_ativa = False
tempo_pocao_ativada = 0
duracao_pocao = 3000  # 3 segundos de duração do efeito

# Tempo de início do jogo
tempo_inicio = pygame.time.get_ticks()

# Contador de gatos
contador_gatos = 0

# Definir posição inicial do gato
pos_gato = [randint(0, largura_tela - tamanho_gato[0]), randint(0, altura_tela - tamanho_gato[1])]

# Função para calcular a direção dos inimigos
def mover_inimigos(inimigos, pos_protagonista, velocidade):
    for inimigo in inimigos:
        dx, dy = pos_protagonista[0] - inimigo["pos"][0], pos_protagonista[1] - inimigo["pos"][1]
        distancia = math.hypot(dx, dy)
        if distancia != 0:
            inimigo["pos"][0] += int(dx / distancia * velocidade)
            inimigo["pos"][1] += int(dy / distancia * velocidade)

# Função para adicionar um novo inimigo lento
def adicionar_inimigo_lento():
    x = randint(0, largura_tela - 40)
    y = randint(0, altura_tela - 40)
    inimigos_lentos.append({
        "pos": [x, y],
        "imagem": pygame.transform.scale(inimigo_img_original, tamanho_inimigo),
        "vida": 5
    })

# Função para adicionar um novo inimigo rápido
def adicionar_inimigo_rapido():
    x = randint(0, largura_tela - 40)
    y = randint(0, altura_tela - 40)
    inimigos_rapidos.append({
        "pos": [x, y],
        "imagem": pygame.transform.scale(inimigo2_img_original, tamanho_inimigo),
        "vida": 3
    })

# Loop principal do jogo
clock = pygame.time.Clock()
jogo_ativo = True
while jogo_ativo:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # Movimento do protagonista com as teclas WASD
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a] and pos_protagonista[0] > 0:
        pos_protagonista[0] -= velocidade_protagonista
    if teclas[pygame.K_d] and pos_protagonista[0] < largura_tela - 40:
        pos_protagonista[0] += velocidade_protagonista
    if teclas[pygame.K_w] and pos_protagonista[1] > 0:
        pos_protagonista[1] -= velocidade_protagonista
    if teclas[pygame.K_s] and pos_protagonista[1] < altura_tela - 40:
        pos_protagonista[1] += velocidade_protagonista

    # Disparar automaticamente na direção do mouse a cada intervalo de tiro
    agora = pygame.time.get_ticks()
    if agora - ultimo_tiro >= intervalo_tiro:
        pos_mouse = pygame.mouse.get_pos()
        dx = pos_mouse[0] - pos_protagonista[0]
        dy = pos_mouse[1] - pos_protagonista[1]
        distancia = math.hypot(dx, dy)
        direcao_tiro = (dx / distancia, dy / distancia)
        tiros.append({
            "pos": pos_protagonista[:],
            "direcao": direcao_tiro
        })
        ultimo_tiro = agora

    # Adicionar inimigos
    if pygame.time.get_ticks() - tempo_inimigo_lento > 5000:
        adicionar_inimigo_lento()
        tempo_inimigo_lento = pygame.time.get_ticks()
    if pygame.time.get_ticks() - tempo_inimigo_rapido > 4000:
        adicionar_inimigo_rapido()
        tempo_inimigo_rapido = pygame.time.get_ticks()

    # Movimentação dos inimigos
    mover_inimigos(inimigos_lentos, pos_protagonista, velocidade=2)
    mover_inimigos(inimigos_rapidos, pos_protagonista, velocidade=3)

    # Movimentação dos tiros
    for tiro in tiros[:]:
        tiro["pos"][0] += int(tiro["direcao"][0] * velocidade_tiro)
        tiro["pos"][1] += int(tiro["direcao"][1] * velocidade_tiro)
        if (tiro["pos"][0] < 0 or tiro["pos"][0] > largura_tela or
                tiro["pos"][1] < 0 or tiro["pos"][1] > altura_tela):
            tiros.remove(tiro)

    # Verificar colisão entre o protagonista e o gato
    rect_protagonista = pygame.Rect(pos_protagonista[0], pos_protagonista[1], 40, 40)
    rect_gato = pygame.Rect(pos_gato[0], pos_gato[1], tamanho_gato[0], tamanho_gato[1])
    if rect_protagonista.colliderect(rect_gato):
        contador_gatos += 1
        pos_gato = [randint(0, largura_tela - tamanho_gato[0]), randint(0, altura_tela - tamanho_gato[1])]

    # Verificar colisão entre o protagonista e inimigos
    if not invulneravel:
        for inimigo in inimigos_lentos + inimigos_rapidos:
            rect_inimigo = pygame.Rect(inimigo["pos"][0], inimigo["pos"][1], 40, 40)
            if rect_protagonista.colliderect(rect_inimigo):
                vidas_protagonista -= 1
                ultimo_tempo_dano = pygame.time.get_ticks()
                invulneravel = True
                if vidas_protagonista <= 0:
                    jogo_ativo = False  # Fim de jogo
                break

    # Desativar invulnerabilidade após 2 segundos
    if invulneravel and pygame.time.get_ticks() - ultimo_tempo_dano > tempo_invulneravel:
        invulneravel = False

    # Verificar colisão entre os tiros e os inimigos
    for tiro in tiros[:]:
        rect_tiro = pygame.Rect(tiro["pos"][0], tiro["pos"][1], 5, 5)
        for inimigo in inimigos_lentos[:]:
            rect_inimigo = pygame.Rect(inimigo["pos"][0], inimigo["pos"][1], 40, 40)
            if rect_tiro.colliderect(rect_inimigo):
                inimigo["vida"] -= 1
                tiros.remove(tiro)
                if inimigo["vida"] <= 0:
                    inimigos_lentos.remove(inimigo)
                    contador_inimigos_derrotados += 1
                break
        for inimigo in inimigos_rapidos[:]:
            rect_inimigo = pygame.Rect(inimigo["pos"][0], inimigo["pos"][1], 40, 40)
            if rect_tiro.colliderect(rect_inimigo):
                inimigo["vida"] -= 1
                tiros.remove(tiro)
                if inimigo["vida"] <= 0:
                    inimigos_rapidos.remove(inimigo)
                    contador_inimigos_derrotados += 1
                break

    # Lógica da poção
    if contador_inimigos_derrotados >= 5 and not pos_pocao:
        pos_pocao = [randint(0, largura_tela - tamanho_pocao[0]), randint(0, altura_tela - tamanho_pocao[1])]
        contador_inimigos_derrotados = 0
    if pos_pocao:
        rect_pocao = pygame.Rect(pos_pocao[0], pos_pocao[1], tamanho_pocao[0], tamanho_pocao[1])
        if rect_protagonista.colliderect(rect_pocao):
            pos_pocao = None
            pocao_ativa = True
            tempo_pocao_ativada = pygame.time.get_ticks()
            velocidade_protagonista *= 2
            intervalo_tiro /= 2
    if pocao_ativa and pygame.time.get_ticks() - tempo_pocao_ativada > duracao_pocao:
        pocao_ativa = False
        velocidade_protagonista /= 2
        intervalo_tiro *= 2
  

    # Atualizar e exibir o cenário
    tela.blit(fundo_img, (0, 0))
    tela.blit(protagonista, pos_protagonista)
    tela.blit(gato_img, pos_gato)
    if pos_pocao:
        tela.blit(pocao_img, pos_pocao)

    for inimigo in inimigos_lentos:
        tela.blit(inimigo["imagem"], inimigo["pos"])
    for inimigo in inimigos_rapidos:
        tela.blit(inimigo["imagem"], inimigo["pos"])

    for tiro in tiros:
        pygame.draw.circle(tela, (0, 0, 255), (int(tiro["pos"][0]), int(tiro["pos"][1])), 5)

    # Contador de vidas, tempo e gatos
    texto_vidas = fonte.render(f'Vidas: {vidas_protagonista}', True, COR_TEXTO)
    tela.blit(texto_vidas, (largura_tela - 100, altura_tela - 30))

    tempo_jogo = (pygame.time.get_ticks() - tempo_inicio) // 1000
    texto_tempo = fonte.render(f'Tempo: {tempo_jogo}s', True, COR_TEXTO)
    tela.blit(texto_tempo, (largura_tela // 2 - texto_tempo.get_width() // 2, 20))

    texto_gatos = fonte.render(f'Gatos: {contador_gatos}', True, COR_TEXTO)
    tela.blit(texto_gatos, (20, altura_tela - 30))

    pygame.display.flip()
    clock.tick(30)

if vidas_protagonista <= 0:
    subprocess.Popen(["python", "gameover.py"])

