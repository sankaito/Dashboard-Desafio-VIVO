from math import sqrt


def bhaskara(a, b, c):
    if a == 0:
        return "Isso não é uma equação do 2º grau (a não pode ser 0)."

    delta = b ** 2 - 4 * a * c

    if delta < 0:
        return f"Delta = {delta}\nNão existem raízes reais (delta negativo)."

    x1 = (-b + sqrt(delta)) / (2 * a)

    if delta == 0:
        return f"Delta = {delta}\nRaiz real dupla:\nx = {x1}"

    x2 = (-b - sqrt(delta)) / (2 * a)
    return f"Delta = {delta}\nDuas raízes reais distintas:\nx1 = {x1}\nx2 = {x2}"


def main():
    try:
        a = float(input("Digite o valor de a: "))
        b = float(input("Digite o valor de b: "))
        c = float(input("Digite o valor de c: "))

        resultado = bhaskara(a, b, c)
        print("\nResultado:")
        print(resultado)
    except ValueError:
        print("Por favor, digite apenas números válidos.")


if __name__ == "__main__":
    main()
