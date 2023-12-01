import pygame
import sys
import json
import random

# Inicialize o Pygame
pygame.init()
pygame.mixer.init()

#musica
pygame.mixer.music.load('data/b423b42.wav')
pygame.mixer.music.play(-1)

# Configurações da janela
largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Math Word")

# Cores
ciano = (0, 255, 255)
preto = (0, 0, 0)

# Usuário atualmente logado
usuario_logado = None

# Função para criar uma conta
def criar_conta():
    nome_usuario = input_caixa_texto("Digite o nome de usuário:")
    senha = input_caixa_texto("Digite a senha:")

    # Verifique se o arquivo de contas existe
    try:
        with open("contas.json", "r") as arquivo_contas:
            contas = json.load(arquivo_contas)
    except FileNotFoundError:
        contas = {}

    # Verifique se o nome de usuário já existe
    if nome_usuario in contas:
        exibir_mensagem("Nome de usuário já existe. Escolha outro.")
        return False

    # Adicione a nova conta
    contas[nome_usuario] = senha

    # Salve as contas no arquivo
    with open("contas.json", "w") as arquivo_contas:
        json.dump(contas, arquivo_contas)

    exibir_mensagem("Conta criada com sucesso.")
    return True

# Função para fazer login
def fazer_login():
    nome_usuario = input_caixa_texto("Digite o nome de usuário:")
    senha = input_caixa_texto("Digite a senha:")

    # Verifique se o arquivo de contas existe
    try:
        with open("contas.json", "r") as arquivo_contas:
            contas = json.load(arquivo_contas)
    except FileNotFoundError:
        exibir_mensagem("Nenhuma conta encontrada.")
        return None

    # Verifique se as credenciais são válidas
    if nome_usuario in contas and contas[nome_usuario] == senha:
        exibir_mensagem("Login bem-sucedido.")
        return nome_usuario
    else:
        exibir_mensagem("Credenciais inválidas.")
        return None

# Função para exibir uma mensagem na tela
def exibir_mensagem(mensagem, cor=preto):
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(mensagem, True, cor)
    retangulo_texto = texto.get_rect(center=(largura // 2, altura // 2))
    janela.fill(ciano)
    janela.blit(texto, retangulo_texto)
    pygame.display.flip()
    pygame.time.delay(2000)  # Exibe a mensagem por 2 segundos

# Função para exibir uma caixa de texto e obter a entrada do usuário
def input_caixa_texto(mensagem):
    fonte = pygame.font.Font(None, 36)
    entrada = ""
    ativo = True

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                else:
                    entrada += evento.unicode

        janela.fill(ciano)
        texto = fonte.render(mensagem + " " + entrada, True, preto)
        retangulo_texto = texto.get_rect(center=(largura // 2, altura // 2))
        janela.blit(texto, retangulo_texto)
        pygame.display.flip()

    return entrada

# Função para escolher a dificuldade
def escolher_dificuldade():
    exibir_mensagem("Escolha a dificuldade:")

    fonte = pygame.font.Font(None, 36)
    texto_facil = fonte.render("Pressione '1' para Fácil", True, preto)
    texto_medio = fonte.render("Pressione '2' para Médio", True, preto)
    texto_dificil = fonte.render("Pressione '3' para Difícil", True, preto)

    retangulo_facil = texto_facil.get_rect(center=(largura // 2, altura // 2))
    retangulo_medio = texto_medio.get_rect(center=(largura // 2, altura // 2 + 50))
    retangulo_dificil = texto_dificil.get_rect(center=(largura // 2, altura // 2 + 100))

    janela.fill(ciano)
    janela.blit(texto_facil, retangulo_facil)
    janela.blit(texto_medio, retangulo_medio)
    janela.blit(texto_dificil, retangulo_dificil)
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "Fácil"
                elif evento.key == pygame.K_2:
                    return "Médio"
                elif evento.key == pygame.K_3:
                    return "Difícil"

# Função para escolher as operações
def escolher_operacoes():
    exibir_mensagem("Escolha as operações:")

    operacoes = ["+", "-", "*", "/"]
    operacoes_escolhidas = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3]:
                    tecla = evento.key - pygame.K_KP0
                    if tecla == 10:  # A tecla 10 corresponde a 0 no teclado numérico
                        tecla = 0
                    operacao = operacoes[tecla]
                    if operacao not in operacoes_escolhidas:
                        operacoes_escolhidas.append(operacao)
                elif evento.unicode in operacoes and evento.unicode not in operacoes_escolhidas:
                    operacoes_escolhidas.append(evento.unicode)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    return operacoes_escolhidas

        janela.fill(ciano)
        fonte = pygame.font.Font(None, 36)
        texto_escolhidas = fonte.render("Operações escolhidas: " + ' '.join(operacoes_escolhidas), True, preto)
        retangulo_escolhidas = texto_escolhidas.get_rect(center=(largura // 2, altura // 2 - 100))
        janela.blit(texto_escolhidas, retangulo_escolhidas)

        for i, operacao in enumerate(operacoes):
            texto_operacao = fonte.render(f"Pressione '{operacao}' para {operacao}", True, preto)
            retangulo_operacao = texto_operacao.get_rect(center=(largura // 2, altura // 2 + i * 50))
            janela.blit(texto_operacao, retangulo_operacao)

        texto_confirmar = fonte.render("Pressione 'ENTER' para confirmar", True, preto)
        retangulo_confirmar = texto_confirmar.get_rect(center=(largura // 2, altura // 2 + len(operacoes) * 50))
        janela.blit(texto_confirmar, retangulo_confirmar)

        pygame.display.flip()

# Função para iniciar o jogo
def iniciar_jogo(dificuldade, operacoes):
    exibir_mensagem(f"Jogo iniciado com dificuldade {dificuldade} e operações {', '.join(operacoes)}")

    pontuacao_total = 0

    while True:
        pontuacao_partida = jogar_partida(dificuldade, operacoes)
        pontuacao_total += pontuacao_partida

        mensagem_final = f"Fim da partida! Pontuação da partida: {pontuacao_partida}, Pontuação total: {pontuacao_total}"
        exibir_mensagem(mensagem_final)

        # Perguntar se o jogador quer jogar novamente
        resposta = input_caixa_texto("Deseja jogar novamente? (S/N)").lower()
        if resposta != "s":
            exibir_mensagem("Obrigado por jogar! Até a próxima.")
            break

# Função para jogar uma partida
def jogar_partida(dificuldade, operacoes):
    pontuacao = 0
    num_calculos = 5

    for _ in range(num_calculos):
        resultado = gerar_calculo(operacoes)

        while True:
            resposta_usuario = input_caixa_texto(resultado["expressao"])

            try:
                resposta_usuario = float(resposta_usuario)
                if resposta_usuario == resultado["correto"]:
                    exibir_mensagem("Resposta correta!", cor=(0, 255, 0))  # Verde
                    pontuacao += 1
                    break
                else:
                    exibir_mensagem(f"Resposta incorreta. A resposta correta é {resultado['correto']}", cor=(255, 0, 0))  # Vermelho
                    break
            except ValueError:
                exibir_mensagem("Digite um número válido.", cor=(255, 0, 0))  # Vermelho

    return pontuacao

# Função para gerar um cálculo
def gerar_calculo(operacoes):
    global correto
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operacao = random.choice(operacoes)

    if operacao == "+":
        correto = num1 + num2
    elif operacao == "-":
        correto = num1 - num2
    elif operacao == "*":
        correto = num1 * num2
    elif operacao == "/":
        correto = num1 / num2

    expressao = f"{num1} {operacao} {num2} = "
    return {"expressao": expressao, "correto": correto}

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Exibir opções na tela
    janela.fill(ciano)
    fonte = pygame.font.Font(None, 36)

    opcao_criar_conta = fonte.render("Pressione 'C' para criar uma conta", True, preto)
    opcao_fazer_login = fonte.render("Pressione 'L' para fazer login", True, preto)
    opcao_fechar_jogo = fonte.render("Pressione 'ESC' para fechar o jogo", True, preto)

    retangulo_criar_conta = opcao_criar_conta.get_rect(center=(largura // 2, altura // 2 - 50))
    retangulo_fazer_login = opcao_fazer_login.get_rect(center=(largura // 2, altura // 2))
    retangulo_fechar_jogo = opcao_fechar_jogo.get_rect(center=(largura // 2, altura // 2 + 50))

    janela.blit(opcao_criar_conta, retangulo_criar_conta)
    janela.blit(opcao_fazer_login, retangulo_fazer_login)
    janela.blit(opcao_fechar_jogo, retangulo_fechar_jogo)

    pygame.display.flip()

    # Processar eventos de teclado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_c]:
        if criar_conta():
            usuario_logado = fazer_login()  # Após criar conta, faça login automaticamente
    elif teclas[pygame.K_l]:
        usuario_logado = fazer_login()
        if usuario_logado:
            dificuldade_escolhida = escolher_dificuldade()
            exibir_mensagem(f"Dificuldade escolhida: {dificuldade_escolhida}")

            operacoes_escolhidas = escolher_operacoes()
            exibir_mensagem(f"Operações escolhidas: {' '.join(operacoes_escolhidas)}")

            exibir_mensagem("Pressione 'ENTER' para iniciar o jogo.")
            iniciar_jogo(dificuldade_escolhida, operacoes_escolhidas)
    elif teclas[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Controla a taxa de quadros (FPS)
    pygame.time.Clock().tick(30)