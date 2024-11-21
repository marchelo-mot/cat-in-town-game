import pygame
import sys
import subprocess

# Inicializar o Pygame
pygame.init()

# Configurações da tela
largura_tela, altura_tela = 1200, 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Menu")

# Imagens do menu
menu_img = pygame.image.load("menu.png")
botao_jogar_img = pygame.image.load("botaojogar.png")

# Redimensionar imagens
menu_img = pygame.transform.scale(menu_img, (largura_tela, altura_tela))
botao_jogar = pygame.transform.scale(botao_jogar_img, (200, 100))

# Posições do botão
pos_botao_jogar = ((largura_tela - botao_jogar.get_width()) // 2, altura_tela // 2)

# Função para exibir o menu
def mostrar_menu():
    while True:
        # Desenhar o menu
        tela.blit(menu_img, (0, 0))
        tela.blit(botao_jogar, pos_botao_jogar)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Verifica se clicou no botão "Jogar"
                mouse_pos = pygame.mouse.get_pos()
                if (pos_botao_jogar[0] <= mouse_pos[0] <= pos_botao_jogar[0] + botao_jogar.get_width() and
                        pos_botao_jogar[1] <= mouse_pos[1] <= pos_botao_jogar[1] + botao_jogar.get_height()):
                    # Executa o arquivo main.py
                    subprocess.Popen(["python", "main.py"])
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Mostrar o menu
mostrar_menu()
