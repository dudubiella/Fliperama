import pygame
import os

class Chao:
    # Define a imagem deste objeto
    IMAGEM = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','base.png')))
    # Define a velocidade do Chão
    VELOCIDADE = 5
    # Define a largura da imagem do Chão para saber onde começará o próximo
    LARGURA = IMAGEM.get_width()
    # Define a imagem deste objeto

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
