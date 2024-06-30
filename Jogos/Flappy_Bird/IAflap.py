import neat.config
import pygame
from passaro import *
from cano import *
from chao import *
import neat

ai_jogando = True
geracao = 0

# Constantes do tamanho da tela e imagens utilizadas
TELA_L, TELA_A = 500, 800

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

def desenha_tela(tela, passaros, canos, chao, pontos):
    IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','bg.png')))
    tela.blit(IMG_BACKGROUND, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit (texto, (TELA_L - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit (texto, (10, 10))

    chao.desenhar(tela)

    pygame.display.update()

def main(genomas = None, config = None):
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        list_gen = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            list_gen.append(genoma)
            passaros.append(Passaro(230, 350))
            
    else:
        passaros = [Passaro(230, 350)]

    chao = Chao(TELA_A - 70)
    canos = [Cano(TELA_L + 200, random.randrange(0, int(input("Defina a dificuldade:\n 0 - Facil\n 1 - Medio\n 2 - dificil\n\n")) + 1))]
    tela = pygame.display.set_mode((TELA_L, TELA_A))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # Intereação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return pontos

            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        if ai_jogando:
            indece_cano = 0
            if len(passaros) > 0:
                if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].CANO_TOPO.get_width():
                    indece_cano = 1
            else:
                rodando = False
                break

        # Mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            list_gen[i].fitness += 0.1
            output = redes[i].activate((passaro.y, abs(passaro.y - canos[indece_cano].altura), abs(passaro.y - canos[indece_cano].pos_base)))
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()
        
        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        list_gen[i].fitness -= 1
                        list_gen.pop(i)
                        redes.pop(i)

                if not cano.passou and passaro.x > cano.x + cano.IMAGEM.get_height() / 10:
                    cano.passou = True
                    adicionar_cano = True
            
            cano.mover()
            
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
            
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(TELA_L + 100, 1))
            for genima in list_gen:
                genima.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.img.get_height() > TELA_A - 70  or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    list_gen[i].fitness -= 0.5
                    list_gen.pop(i)
                    redes.pop(i)

        if passaros == []:
            print(f"Você fez {pontos} pontos PARABÉNS")
            
        desenha_tela(tela, passaros, canos, chao, pontos)
    print(pontos)
    
def rodar(caminho):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    
    if ai_jogando:
        populacao.run(main)
    else:
        main()

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, "config.txt")
    rodar(caminho_config)