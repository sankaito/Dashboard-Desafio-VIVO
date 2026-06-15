B = input("Caso queira calcular uma raiz quadrada digite um número, se deseja calcular raiz cúbica deixe em branco: ")

if B == "":
    C = float(input("Digite um número para calcular a raiz cúbica: "))
    T2 = C**(1/3)
    print("O valor da raiz cúbica é {:.2f}".format(T2))
else:
    B = float(B)
    T = B**(1/2)
    print("O valor da raiz quadrada é {:.2f}".format(T))