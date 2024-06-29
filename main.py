import pygame, sys
from botao import Button
import os

pygame.init()

TELA_L, TELA_A = 1280, 720

TELA = pygame.display.set_mode((TELA_L, TELA_A))
pygame.display.set_caption("Menu")

BG = pygame.image.load("imgs/BackGround.png")

def add_fonte(tamanho):
    return pygame.font.Font("imgs/font.ttf", tamanho)

def muda_opcao(atual, acao, max):
    atual + acao
    if atual > max:
        atual = 0
    elif atual < 0:
        atual = max
    return atual

def le_creditos(local):
    fd = os.open(local, os.O_RDONLY)
    tamanho_arquivo = os.path.getsize(local)
    content = os.read(fd, tamanho_arquivo)
    os.close(fd)
    return content.decode('utf-8')
    
def play():
    pygame.display.set_caption("Games")
 
    while True:
        TELA.blit(BG, (0, 0))
        pygame.display.update()

def creditos():
    pygame.display.set_caption("Creditos")

    opcao = 0
    
    botoes = []
    conteudos = []
    
    local_pasta = os.getcwd()
    lista_colaboradores = os.listdir(local_pasta + "\\creditos")

    for i, nome_arq in enumerate(lista_colaboradores):
        local = local_pasta + "\\creditos" + "\\" + nome_arq
        conteudos.append(le_creditos(local))
        nome = os.path.splitext(nome_arq)[0]
        botoes.append(Button(imagem = pygame.image.load("imgs/Options Rect.png"), pos = (640, 200 + 130 * i),
                             texto = nome, fonte = add_fonte(70), cor = "Black", cor_selecionada = "Green", opcao = i))

    creditos_sair = Button(imagem = pygame.image.load("imgs/Quit Rect.png"), pos = (640, 460),
                           texto = "SAIR", fonte = add_fonte(75), cor = "Black", cor_selecionada = "Green", opcao = i + 1)
    
    while True:
        TELA.fill("white")

        creditos_sair.muda_cor(opcao)

        creditos_sair.atualiza(TELA)
        
        for botao in botoes:
            botao.muda_cor(opcao)
            botao.atualiza(TELA)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if opcao <= 0:
                        opcao = 2
                    else:
                        opcao -= 1
                elif evento.key == pygame.K_DOWN:
                    if opcao >= 2:
                        opcao = 0
                    else:
                        opcao += 1

                elif evento.key == pygame.K_SPACE:
                    ##se for realizar algo ao selecionar alguem nos créditos
                    #if BetaMixs.verifica_entrada(opcao):
                    #    mostra_creditos("BetaMixt")
                    #if Biella.verifica_entrada(opcao):
                    #    mostra_creditos("Biella")

                    if creditos_sair.verifica_entrada(opcao):
                        main_menu()
        
        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Menu")
    
    opcao = 0
    
    while True:
        TELA.blit(BG, (0, 0))

        texto_menu = add_fonte(100).render("MENU", True, "#b68f40")
        menu_certo = texto_menu.get_rect(center = (640, 100))
        
        but_play = Button(imagem = pygame.image.load("imgs/Play Rect.png"), pos = (640,250),
                          texto = "PLAY", fonte = add_fonte(75), cor = "#d7fcd4", cor_selecionada = "white", opcao = 0)
        but_creditos = Button(imagem = pygame.image.load("imgs/Options Rect.png"), pos = (640,400),
                          texto = "CREDITS", fonte = add_fonte(75), cor = "#d7fcd4", cor_selecionada = "white", opcao = 1)
        but_sair = Button(imagem = pygame.image.load("imgs/Quit Rect.png"), pos = (640,550),
                          texto = "SAIR", fonte = add_fonte(75), cor = "#d7fcd4", cor_selecionada = "white", opcao = 2)

        TELA.blit(texto_menu, menu_certo)

        for button in [but_play, but_creditos, but_sair]:
            button.muda_cor(opcao)
            button.atualiza(TELA)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if opcao <= 0:
                        opcao = 2
                    else:
                        opcao -= 1
                elif evento.key == pygame.K_DOWN:
                    if opcao >= 2:
                        opcao = 0
                    else:
                        opcao += 1

                elif evento.key == pygame.K_SPACE:
                    if but_play.verifica_entrada(opcao):
                        play()
                    if but_creditos.verifica_entrada(opcao):
                        creditos()
                    if but_sair.verifica_entrada(opcao):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

main_menu()