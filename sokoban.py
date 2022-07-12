"""
  Autor: vichShir
  Versão: 1.5
"""


class Sokoban():

  def __init__(self, nome_arquivo):
    self.fase = self.CarregarFase(nome_arquivo)
  

  # Funcao que recebe a matriz M de cenario e executa o jogo. Deve imprimir uma
  # unica vez a mensagem "Jogar: (c)ima / (b)aixo / (e)squerda / (d)ireita / 
  # (v)oltar / (s)air", depois a matriz com o cenario inicial, entao imprimir a 
  # mensagem "Sequencia de movimentos: " solicitando uma cadeia de caracteres com
  # varios movimentos (quantidade arbitraria). Se o jogo finalizar com sucesso 
  # depois dos movimentos serem executados, deve imprimir a mensagem adequada. 
  # Senao, deve solicitar nova cadeia de caracteres com nova sequencia de 
  # movimentos. Repetir ate finalizar jogo ou sair. 
  # Nada devolve.
  def play(self):
    M = self.fase
    if not self.CenarioValido(M):
      print('Cenario invalido')
      return
    print('Jogar: (c)ima / (b)aixo / (e)squerda / (d)ireita / (v)oltar / (s)air')
    self.ImprimirCenario(M)
    Hmov = []
    leave = False
    while not self.FaseCompletada(M) and not leave:
      movs = input('Sequencia de movimentos: \n')
      for mov in movs:
        if mov == 's':
          leave = True
          print('Fim do jogo')
          break
        elif mov == 'v':
          self.VoltarJogador(M, Hmov[-1])
          del Hmov[-1]
        else:
          temp_mov = self.MoverJogador(M, mov)
          if temp_mov != '':
            Hmov.append(temp_mov)
      if not leave:
        self.ImprimirCenario(M)
        if self.FaseCompletada(M):
          print('Parabens, fase completada!')
          self.ImprimeMovimentos(''.join(Hmov))


  # Funcao que le um cenario do arquivo texto de nome nome_arquivo e o armazena
  # numa matriz de caracteres.
  # Todas as linhas da matriz devem ter o mesmo numero de elementos.
  # No caso de arquivos texto com diferentes quantidades de caracteres por linha,
  # as linhas da matriz com menos elementos devem ser completadas com espacos em
  # branco a direita. 
  # Devolve a matriz do cenário.
  def CarregarFase(self, nome_arquivo): # todos os modos
    # completar
    fase = []
    fase2 = []
    max_elements = 0
    with open(nome_arquivo, 'r') as f:
      for line in f.readlines():
        line = line.replace('\n', '')
        fase.append(line)
        if len(line) > max_elements:
          max_elements = len(line)
    for element in fase:
      fase2.append(list(self.FillString(element, max_elements)))
    return fase2  # alterar valor devolvido


  def FillString(self, text, len_goal):
    n_fill = len_goal - len(text)
    return text + (' ' * n_fill)


  # Funcao que recebe uma matriz de cenario M e a imprime tal como ela aparece
  # no arquivo texto de onde foi carregada.
  # Nada devolve.
  def ImprimirCenario(self, M): # modo 1
    # completar
    for row in M:
      print(''.join(row))
    return

    
  # Funcao  que testa se o cenario na matriz M e' um cenario valido. Todo 
  # cenario deve: ter um unico jogador; quantidade igual de caixas e locais de 
  # armazenamento; e pelo menos um lugar de armazenamento.
  # A funcao deve devolver True (se cenario valido) ou False (se cenario  
  # invalido).
  # Devolve True ou False.
  def CenarioValido(self, M): # modo 2
    # Completar
    n_players = 0
    n_caixas = 0
    n_locais = 0
    for i in range(len(M)):
      for j in range(len(M[0])):
        if M[i][j] == '@' or M[i][j] == '+':
          n_players += 1
        if M[i][j] == '$':
          n_caixas += 1
        elif M[i][j] == '.' or M[i][j] == '+':
          n_locais += 1
    return (n_players == 1) and (n_caixas == n_locais) and (n_locais > 0)   # alterar valor devolvido


  # Funcao que recebe a matriz de caracteres M (cenario) e devolve a posicao 
  # do jogador no cenario (ou seja, a linha i e coluna j para a qual M[i][j]=='@'
  # ou M[i][j]=='+').
  # Se nao existe um jogador dentro do cenario, entao a funcao deve devolver
  # os valores -1,-1. 
  # Devolve a posicao i,j do jogador.
  def ObterPosicaoJogador(self, M): # modo 3
    # Completar
    for i in range(len(M)):
      for j in range(len(M[0])):
        if M[i][j] == '@' or M[i][j] == '+':
          p_pos = (i, j)
    if p_pos is None:
      p_pos = -1, -1
    return p_pos  # alterar valor devolvido


  # Funcao que realiza o movimento dado pelo caracter em mov, atualizando 
  # adequadamente a matriz M de estado do jogo. Assim, mov pode conter qualquer
  # um dos caracteres de movimentos validos ('c', 'b', 'e', 'd').
  # A funcao deve devolver um caractere correspondente ao valor do movimento,
  # para ser armazenado no historico de movimentos. Portanto, a funcao deve 
  # devolver o caracter vazio ('') caso nao seja possivel realizar o movimento
  # (como quando tenta-se  empurrar duas ou mais caixas juntas de uma so vez
  # ou mover sobre um muro). Quando o movimento e valido e nao empurra caixas,
  # o proprio valor de mov deve ser devolvido. Porem, se uma caixa e' empurrada
  # pelo movimento, entao a funcao deve devolver a letra armazenada em mov 
  # convertida para letra maiuscula. 
  # Devolve caractere do movimento efetivado (eventualmente vazio '').
  def MoverJogador(self, M, mov): # modo 4
    # Completar
    temp_mov = mov
    y, x = self.ObterPosicaoJogador(M)
    curr_pos, next_pos, third_pos = self.GetPositions(M, x, y, temp_mov)
    # Movimento parado
    if third_pos == '-1':
      return ''
    # Realizar movimento
    if next_pos != '#':
      if (next_pos == '$' and third_pos == '$') or (next_pos == '$' and third_pos == '#') or (next_pos == '*' and third_pos == '#'):  # Empurar duas ou mais caixas ou empurrar caixa para parede
        mov = ''
      elif curr_pos == '+' and next_pos == '$': # Sair do local de armazenamento
        mov = mov.upper()
        curr_pos = '.'
        next_pos = '@'
        third_pos = '$'
      elif curr_pos == '+' and next_pos == '*' and third_pos == '.': # Sair do local de armazenamento
        mov = mov.upper()
        curr_pos = '.'
        next_pos = '+'
        third_pos = '*'
      elif next_pos == '$' and third_pos == ' ': # Empurrar caixa
        mov = mov.upper()
        curr_pos = ' '
        next_pos = '@'
        third_pos = '$'
      elif next_pos == '$' and third_pos == '.': # Empurrar caixa no local de armazenamento
        mov = mov.upper()
        curr_pos = ' '
        next_pos = '@'
        third_pos = '*'
      elif next_pos == '*' and third_pos == '.': # Empurrar caixa que está no local de armazenamento
        mov = mov.upper()
        curr_pos = ' '
        next_pos = '+'
        third_pos = '*'
      elif next_pos == '*' and third_pos == ' ': # Empurrar caixa que está no local de armazenamento
        mov = mov.upper()
        curr_pos = ' '
        next_pos = '+'
        third_pos = '$'
      elif curr_pos == '+' and next_pos == ' ': # Sair do local de armazenamento
        curr_pos = '.'
        next_pos = '@'
      elif curr_pos == '+' and next_pos == '.': # Sair do local de armazenamento
        curr_pos = '.'
        next_pos = '+'
      elif next_pos == '.': # Entrar no local de armazenamento
        curr_pos = ' '
        next_pos = '+'
      else: # Andar
        curr_pos = ' '
        next_pos = '@'
    elif (next_pos == '#' and third_pos == '#'):
      third_pos = '#'
    else:
      mov = ''
    # Atualizar matriz
    if temp_mov == 'd':
      M[y][x] = curr_pos
      M[y][x+1] = next_pos
      M[y][x+2] = third_pos
    elif temp_mov == 'e':
      M[y][x] = curr_pos
      M[y][x-1] = next_pos
      M[y][x-2] = third_pos
    elif temp_mov == 'b':
      M[y][x] = curr_pos
      M[y+1][x] = next_pos
      M[y+2][x] = third_pos
    elif temp_mov == 'c':
      M[y][x] = curr_pos
      M[y-1][x] = next_pos
      M[y-2][x] = third_pos
    return mov   # alterar valor devolvido


  def GetPositions(self, M, x, y, mov):
    if mov == 'd':
      first_pos = M[y][x]
      second_pos = M[y][x+1]
      third_pos = M[y][x+2] if second_pos != '#' else '-1'
    elif mov == 'e':
      first_pos = M[y][x]
      second_pos = M[y][x-1]
      third_pos = M[y][x-2] if second_pos != '#' else '-1'
    elif mov == 'b':
      first_pos = M[y][x]
      second_pos = M[y+1][x]
      third_pos = M[y+2][x] if second_pos != '#' else '-1'
    elif mov == 'c':
      first_pos = M[y][x]
      second_pos = M[y-1][x]
      third_pos = M[y-2][x] if second_pos != '#' else '-1'
    return first_pos, second_pos, third_pos


  # Funcao que desfaz o ultimo movimento realizado (que deve estar em mov), 
  # atualizando adequadamente a matriz M de estado do jogo. O parametro mov 
  # pode ter qualquer dos seguintes valores: 'c', 'C', 'b', 'B', 'e', 'E', 
  # 'd', 'D'.
  # Nada devolve (mas altera M).
  def VoltarJogador(self, M, mov): # modo 5
    # Completar
    y, x = self.ObterPosicaoJogador(M)
    goal_pos, curr_pos, neighbor_pos = self.GetBackPositions(M, x, y, mov)
    if mov == 'd' or mov == 'e' or mov == 'b' or mov == 'c': # Mover jogador
      if goal_pos == '.':
        goal_pos = '+'
        curr_pos = ' '
      else:
        goal_pos = '@'
        curr_pos = ' '
    elif mov == 'D' or mov == 'E' or mov == 'B' or mov == 'C': # Mover jogador e caixa
      if goal_pos == '.' and curr_pos == '+' and neighbor_pos == '*':
        goal_pos = '+'
        curr_pos = '*'
        neighbor_pos = '.'
      elif curr_pos == '+' and neighbor_pos == '*':
        goal_pos = '@'
        curr_pos = '*'
        neighbor_pos = '.'
      elif goal_pos == '.':
        goal_pos = '+'
        curr_pos = '$'
        neighbor_pos = ' '
      elif neighbor_pos == '*':
        goal_pos = '@'
        curr_pos = '$'
        neighbor_pos = '.'
      else:
        goal_pos = '@'
        curr_pos = '$'
        neighbor_pos = ' '
    
    # Atualizar matriz
    if mov == 'd' or mov == 'D':
      M[y][x-1] = goal_pos
      M[y][x] = curr_pos
      M[y][x+1] = neighbor_pos
    elif mov == 'e' or mov == 'E':
      M[y][x+1] = goal_pos
      M[y][x] = curr_pos
      M[y][x-1] = neighbor_pos
    elif mov == 'b' or mov == 'B':
      M[y-1][x] = goal_pos
      M[y][x] = curr_pos
      M[y+1][x] = neighbor_pos
    elif mov == 'c' or mov == 'C':
      M[y+1][x] = goal_pos
      M[y][x] = curr_pos
      M[y-1][x] = neighbor_pos
    return


  def GetBackPositions(M, x, y, mov):
    if mov == 'd' or mov == 'D':
      goal_pos = M[y][x-1]
      curr_pos = M[y][x]
      neighbor_pos = M[y][x+1]
    elif mov == 'e' or mov == 'E':
      goal_pos = M[y][x+1]
      curr_pos = M[y][x]
      neighbor_pos = M[y][x-1]
    elif mov == 'b' or mov == 'B':
      goal_pos = M[y-1][x]
      curr_pos = M[y][x]
      neighbor_pos = M[y+1][x]
    elif mov == 'c' or mov == 'C':
      goal_pos = M[y+1][x]
      curr_pos = M[y][x]
      neighbor_pos = M[y-1][x]
    return goal_pos, curr_pos, neighbor_pos


  # Funcao que verifica se todas caixas na matriz M estao colocadas nas posicoes
  # predeterminadas (alvo), o que indicara o fim do jogo com sucesso. A funcao 
  # deve devolver verdadeiro (no caso da vitoria do jogador) ou falso (no caso 
  # de jogo nao encerrado).
  # Devolve True ou False.
  def FaseCompletada(self, M): # modo 6
    # Completar
    n_caixas = 0
    n_locais = 0
    for i in range(len(M)):
      for j in range(len(M[0])):
        if M[i][j] == '$':
          n_caixas += 1
        elif M[i][j] == '.':
          n_locais += 1
    return (n_caixas == 0) and (n_locais == 0)    # alterar valor devolvido


  # Funcao que recebe uma cadeia de caracteres Hmov com uma sequência de 
  # movimentos e imprime o numero de movimentos e os movimentos propriamente
  # ditos, devendo ser usada pela funcao Jogo (no modo 7).
  # Nada devolve.
  def ImprimeMovimentos(self, Hmov): # usada na funcao Jogo (abaixo)
    # Completar
    print(f'Total movimentos: {len(Hmov)}')
    print(f'Movimentos: {Hmov}')
    return 


# Funcao principal
# A funcao devera primeiro solicitar do usuario que digite o nome do arquivo
# com o cenario, depois solicitar o modo (1 ate 7), entao invocar a funcao 
# adequada.
# Nada devolve.
def main():
  # Completar
  nome_arquivo = input('Nome arquivo: ')
  game = Sokoban(nome_arquivo)
  game.play()


main()