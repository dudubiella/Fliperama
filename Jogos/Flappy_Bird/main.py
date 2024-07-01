import pygame, sys, os
from passaro import *
from cano import *
from chao import *
from botao import *

# Determina o tamanho da tela
TELA_L, TELA_A = 500, 800
# Define a fonte dos  textos exibidos
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

def desenha_tela(tela, passaros, canos, chao, pontos):
    IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','bg.png')))
    tela.blit(IMG_BACKGROUND, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)
    
    chao.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit (texto, (TELA_L - 10 - texto.get_width(), 10))
    pygame.display.update()

def escolha(tela):
    opcao = 0
    
    facil = Button(imagem = None, pos = (TELA_L / 2, 300),
                           texto = "FACIL", fonte = pygame.font.Font(None, 40), cor = "Black", cor_selecionada = "Green", opcao = 0)
    medio = Button(imagem = None, pos = (TELA_L / 2, 400),
                           texto = "MEDIO", fonte = pygame.font.Font(None, 40), cor = "Black", cor_selecionada = "Green", opcao = 1)
    dificil = Button(imagem = None, pos = (TELA_L / 2, 500),
                           texto = "DIFICIL", fonte = pygame.font.Font(None, 40), cor = "Black", cor_selecionada = "Green", opcao = 2)
    sair_escolha = Button(imagem = None, pos = (TELA_L / 2, 600),
                           texto = "SAIR", fonte = pygame.font.Font(None, 40), cor = "Black", cor_selecionada = "Green", opcao = 3)
    
    while True:
        tela.fill("white")

        texto_dificuldade = pygame.font.Font(None, 50).render("ESCOLHA A DIFICULDADE:", True, "#6699CC")
        dificuldade_certo = texto_dificuldade.get_rect(center = (TELA_L / 2, 100))
        
        tela.blit(texto_dificuldade, dificuldade_certo)

        facil.muda_cor(opcao)
        facil.atualiza(tela)
        
        medio.muda_cor(opcao)
        medio.atualiza(tela)
        
        dificil.muda_cor(opcao)
        dificil.atualiza(tela)

        sair_escolha.muda_cor(opcao)
        sair_escolha.atualiza(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: 
                    opcao -= 1
                    if opcao < 0:
                        opcao = 3
                elif evento.key == pygame.K_DOWN:
                    opcao += 1
                    if opcao > 3:
                        opcao = 0

                elif evento.key == pygame.K_SPACE:
                    return opcao
        pygame.display.update()

def main(arquivo):
    tela = pygame.display.set_mode((TELA_L, TELA_A))

    dificuldade = escolha(tela)
    if dificuldade == 3:
        rodando = False
        with open(arquivo, 'w') as file:
            file.write("-1")
        pygame.quit()
        return -1

    passaros = [Passaro(230, 350)]
    chao = Chao(TELA_A - 70)
    canos = [Cano(TELA_L + 200, dificuldade)]
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        # Determina o FPS
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                with open(arquivo, 'w') as file:
                    file.write(str(pontos))
                pygame.quit()
                return pontos

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        for passaro in passaros:
            passaro.mover()
        chao.mover()
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(TELA_L + 100, dificuldade))

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.img.get_height() > TELA_A - 70  or passaro.y < 0:
                passaros.pop(i)

        if not passaros:
            with open(arquivo, 'w') as file:
                file.write(str(pontos))
            return pontos
        
        desenha_tela(tela, passaros, canos, chao, pontos)
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "output.txt"
    main(arquivo)