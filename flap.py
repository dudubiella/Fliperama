import pygame
import os
import random

# Determina o tamanho da tela
TELA_L, TELA_A = 500, 800

# Busca nesta pasta as imagens utilizadas
caminho = os.path.dirname(__file__) + '\\imgs'
IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'pipe.png')))
IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'base.png')))
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bg.png')))
IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird3.png')))
]

# Define a fonte dos  textos exibidos
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)

class Passaro:
    # Define a imagem deste objeto
    IMGS = IMGS_PASSARO

    # Constantes da animação da rotação
    ROTACAO_MAX = 25
    VEL_ROTACAO = 20
    TEMPO_ANIMAÇAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.cont_img = 0
        self.img = self.IMGS[0]
    
    # Almenta a velocidade para cima do Passaro
    def pular(self):
        self.velocidade = -10.5
        # Tempo da função da queda
        self.tempo = 0
        self.altura = self.y

    # Move o Passaro
    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        # S = So + Vo * t + a * t ** 2 / 2 
        deslocamento = self.velocidade * self.tempo + 1.5 * (self.tempo ** 2)

        ## Restringir o deslocamento
        # Vel Max
        if deslocamento > 16:
            deslocamento = 16

        # Impulso no pulo

        elif deslocamento < 0:
            deslocamento -= 2

        # Desloca o Passaro
        self.y += deslocamento

        # define a angulação para cima e o mantem por um tempo assim
        if deslocamento < 0 or self.y < self.altura + 50:
            # Limita a angulação maxima
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
            
            # Limita a angulação mínima
        else:
            if self.angulo > -90:
                self.angulo -= self.VEL_ROTACAO

    def desenhar(self, tela):
        # Definir qual imagem do passado usar
        self.cont_img += 1

        # Cria a animação de bater de assas
        if self.cont_img < self.TEMPO_ANIMAÇAO:
            self.img = self.IMGS[0]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 2:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 3:
            self.img = self.IMGS[2]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4 + 1:
            self.img = self.IMGS[0]
            self.cont_img = 0

        # Não bate assas caso o Passaro esteja caindo
        if self.angulo <= -80:
            self.img = self.IMGS[1]
            self.cont_img = self.TEMPO_ANIMAÇAO * 2

        ## Desenha a imagem
        # Roda a imagem
        img_rot = pygame.transform.rotate(self.img, self.angulo)
        # Define o centro
        centro = self.img.get_rect(topleft = (self.x, self.y)).center
        # Cria um retangulo em volta
        retangulo = img_rot.get_rect(center = centro)
        # Desenha na tela
        tela.blit(img_rot, retangulo.topleft)

    # Cria a mascara de pixels para futuramente definir se há colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Cano:
    # Defina a distância entre os canos
    DISTANCIA = 200
    # Define a velocidade dos canos
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        self.passou = False
        self.def_altura()

    # Define a altura dos novos canos aleatoriamente
    def def_altura(self):
        self.altura = random.randrange(50, 500)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    # Move os Canos
    def mover(self):
        self.x -= self.VELOCIDADE
    
    # Desenha os Canos
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    # Define se algum Passaro colide com o Cano
    def colidir(self, passaro):
        # Retira as mascaras do tamanho em pixes de cada objeto
        pass_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # Define a distancia do Passaro dos Canos
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # Verifica se tem pixes sobrepostos dos objetos (colisão)
        topo_ponto = pass_mask.overlap(topo_mask, distancia_topo)
        base_ponto = pass_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    # Define a velocidade do Chão
    VELOCIDADE = 5
    # Define a largura da imagem do Chão para saber onde começará o próximo
    LARGURA = IMG_CHAO.get_width()
    # Define a imagem deste objeto
    IMAGEM = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    #move as duas imagens do Chão juntas
    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE
        # Quando alguma imagem sai da tela ela volta ao início
        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    # Desenha os Chãos
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))

# Desenha a tela com todos os objetos a cada frame
def desenha_tela(tela, passaros, canos, chao, pontos):
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