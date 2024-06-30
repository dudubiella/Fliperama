import pygame
from passaro import *
from cano import *
from chao import *

# Determina o tamanho da tela
TELA_L, TELA_A = 500, 800
# Define a fonte dos  textos exibidos
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

# Desenha a tela com todos os objetos a cada frame
def desenha_tela(tela, passaros, canos, chao, pontos):
    # Define a imagem que será o plano de fundo
    IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','bg.png')))

    # Define o plano de fundo
    tela.blit(IMG_BACKGROUND, (0, 0))

    # Desenha cada Passaro 
    for passaro in passaros:
        passaro.desenhar(tela)
    
    # Desenha cada Cano 
    for cano in canos:
        cano.desenhar(tela)
    
    # Desenha o Chão
    chao.desenhar(tela)

    # Define o texto da pontuação apresntada
    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit (texto, (TELA_L - 10 - texto.get_width(), 10))

    # Atualiza a Tela apresentada
    pygame.display.update()

# Roda o Jogo
def main():
    # Cria os Passaros
    passaros = [Passaro(230, 350)]
    # Cria o Chão
    chao = Chao(TELA_A - 70)
    # Cria os Canos
    canos = [Cano(TELA_L + 200)]
    # Cria a Tela
    tela = pygame.display.set_mode((TELA_L, TELA_A))
    # Define a pontuação inicial
    pontos = 0
    # Define o relógio interno do jogo
    relogio = pygame.time.Clock()

    # Define o que ocorre a cada frame
    rodando = True
    while rodando:
        # Determina o FPS
        relogio.tick(30)

        # Intereação com o usuário
        for evento in pygame.event.get():
            # Verifica se o usuário saiu do jogo
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return pontos

            # Verifica se o usuário apertou alguma tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        ## Mover os objetos
        # Move o Passaro
        for passaro in passaros:
            passaro.mover()
        # Move o Chão
        chao.mover()
        # Move os Canos
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            # Compara a situação de cada Cano com cada Passaro
            for i, passaro in enumerate(passaros):
                # Verifica se há colisão com o Passaro
                if cano.colidir(passaro):
                    passaros.pop(i)
                # Verifica se o Passaro passou do Cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            
            # Move o cano
            cano.mover()
            
            # Verifica se o cano saiu da tela
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        # Adiciona um novo Cano
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(TELA_L + 100))

        # Remove os Canos
        for cano in remover_canos:
            canos.remove(cano)

        # Verifica se os Passaros sairam da tela
        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.img.get_height() > TELA_A - 70  or passaro.y < 0:
                passaros.pop(i)

        # Quando não tem mais passaros vivos apresenta sua pontuação
        if passaros == []:
            print(f"Você fez {pontos} pontos")
        
        # Apresenta a Tela com todas as informações
        desenha_tela(tela, passaros, canos, chao, pontos)
    
# Roda o jogo
if __name__ == '__main__':
    main()