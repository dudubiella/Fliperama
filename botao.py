class Button():
    def __init__(self, imagem, pos, texto, fonte, cor, cor_selecionada, opcao):
        self.imagem = imagem
        self.x = pos[0]
        self.y = pos[1]
        self.fonte = fonte
        self.cor_base = cor
        self.cor_select = cor_selecionada
        self.texto_de_entrada = texto
        self.texto = self.fonte.render(self.texto_de_entrada, True, self.cor_base)
        if self.imagem is None:
            self.imagem = self.texto
        self.imagem_certa = self.imagem.get_rect(center = (self.x, self.y))
        self.texto_certo = self.texto.get_rect(center = (self.x, self.y))
        self.opcao = opcao

    def atualiza(self, tela):
        if self.imagem is not None:
            tela.blit(self.imagem, self.imagem_certa)
        tela.blit(self.texto, self.texto_certo)
        pass

    def verifica_entrada(self, opcao):
        if opcao == self.opcao:
            return True
        return False
    
    def muda_cor(self, opcao):
        if opcao == self.opcao:
            self.texto = self.fonte.render(self.texto_de_entrada, True, self.cor_select)
            return True
        else:
            self.texto = self.fonte.render(self.texto_de_entrada, True, self.cor_base)
            return False
    