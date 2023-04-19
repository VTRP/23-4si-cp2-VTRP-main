import cv2

# Declarando as imagens
pedra1 = cv2.imread('Pedra1.jpg')
papel1 = cv2.imread('Papel1.jpg')
tesoura1 = cv2.imread('Tesoura1.jpg')
pedra2 = cv2.imread('Pedra2.jpg')
papel2 = cv2.imread('Papel2.jpg')
tesoura2 = cv2.imread('Tesoura2.jpg')

# vídeo do jogo
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

# tentando acelerar a leitura do frame
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
cap.set(cv2.CAP_PROP_FPS, 60)

# Dimensões do vídeo
width = 1920
height = 1080

# Coordenadas dos crops
#(x,y)- A partir do ponto superior esquerdo (w) - largura e (h) - altura
crop1_x, crop1_y, crop1_w, crop1_h = 0, 0, int(width/2), height
crop2_x, crop2_y, crop2_w, crop2_h = int(width/2), 0, int(width/2), height

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    # Crops por região
    crop1 = frame[crop1_y:crop1_y+crop1_h, crop1_x:crop1_x+crop1_w]
    crop2 = frame[crop2_y:crop2_y+crop2_h, crop2_x:crop2_x+crop2_w]

    # jogada jogador 1 
    #https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html -> TM_SQDIFF_NORMED 
    #comparação de soma entre a imagem de referência e a img de entrada, resultando na correspondencia do valor
    result_pedra1 = cv2.matchTemplate(crop1, pedra1, cv2.TM_SQDIFF_NORMED)
    result_papel1 = cv2.matchTemplate(crop1, papel1, cv2.TM_SQDIFF_NORMED)
    result_tesoura1 = cv2.matchTemplate(crop1, tesoura1, cv2.TM_SQDIFF_NORMED)
    _, max_val_pedra1, _, max_loc_pedra1 = cv2.minMaxLoc(result_pedra1)
    _, max_val_papel1, _, max_loc_papel1 = cv2.minMaxLoc(result_papel1)
    _, max_val_tesoura1, _, max_loc_tesoura1 = cv2.minMaxLoc(result_tesoura1)

    # Identificação do jogador 1
    p1_mao = (max_loc_pedra1[0], max_loc_pedra1[1], pedra1.shape[1], pedra1.shape[0])
    if p1_mao is not None:
        x1, y1, w1, h1 = p1_mao
        cv2.rectangle(crop1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    # jogada jogador 2 
    result_pedra2 = cv2.matchTemplate(crop2, pedra2, cv2.TM_SQDIFF_NORMED)
    result_papel2 = cv2.matchTemplate(crop2, papel2, cv2.TM_SQDIFF_NORMED)
    result_tesoura2 = cv2.matchTemplate(crop2, tesoura2, cv2.TM_SQDIFF_NORMED)
    _, max_val_pedra2, _, max_loc_pedra2 = cv2.minMaxLoc(result_pedra2)
    _, max_val_papel2, _, max_loc_papel2 = cv2.minMaxLoc(result_papel2)
    _, max_val_tesoura2, _, max_loc_tesoura2 = cv2.minMaxLoc(result_tesoura2)

   # Identificação do jogador 2
    p2_mao = (max_loc_pedra2[0], max_loc_pedra2[1], pedra2.shape[1], pedra2.shape[0])
    if p2_mao is not None:
            x2, y2, w2, h2 = p2_mao
            cv2.rectangle(crop2, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)

    # verifica qual jogada foi escolhida pelo jogador 1
    if max_val_pedra1 > max_val_papel1 and max_val_pedra1 > max_val_tesoura1:
        jogada1 = 'pedra'
    elif max_val_papel1 > max_val_pedra1 and max_val_papel1 > max_val_tesoura1:
        jogada1 = 'papel'
    elif max_val_tesoura1 > max_val_pedra1 and max_val_tesoura1 > max_val_papel1:
        jogada1 = 'tesoura'
    else:
        jogada1 = None

 # verifica qual jogada foi escolhida pelo jogador 2
    if max_val_pedra2 > max_val_papel2 and max_val_pedra2 > max_val_tesoura2:
        jogada2 = 'pedra'
    elif max_val_papel2 > max_val_pedra2 and max_val_papel2 > max_val_tesoura2:
        jogada2 = 'papel'
    elif max_val_tesoura2 > max_val_pedra2 and max_val_tesoura2 > max_val_papel2:
        jogada2 = 'tesoura'
    else:
        jogada2 = None

    # compara as jogadas dos jogadores
    if jogada1 == jogada2:
        resultado = 'Empate!'
    elif jogada1 == 'pedra' and jogada2 == 'tesoura' or \
        jogada1 == 'papel' and jogada2 == 'pedra' or \
        jogada1 == 'tesoura' and jogada2 == 'papel':
        resultado = 'Jogador 1 venceu!'
    else:
        resultado = 'Jogador 2 venceu!'

    # exibe o resultado na tela
    cv2.putText(crop1, resultado, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(crop2, resultado, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(crop1, f'Jogada do Jogador 1: {jogada1}', (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(crop2, f'Jogada do Jogador 2: {jogada2}', (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('jogador 1', crop1)
    cv2.imshow('jogador 2', crop2)


  # Verifica se o usuário apertou a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
     break

# Libera os objetos de captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()
