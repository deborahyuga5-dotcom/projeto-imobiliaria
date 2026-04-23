import csv


class Imovel:
    def __init__(self, tipo, valor_base):
        self.tipo = tipo
        self.valor_base = valor_base

    def calcular_aluguel(self):
        return self.valor_base


class Apartamento(Imovel):
    def __init__(self, quartos, garagem, sem_criancas):
        super().__init__("Apartamento", 700.0)
        self.quartos = quartos
        self.garagem = garagem
        self.sem_criancas = sem_criancas

    def calcular_aluguel(self):
        valor = self.valor_base

        if self.quartos == 2:
            valor += 200.0

        if self.garagem:
            valor += 300.0

        if self.sem_criancas:
            valor *= 0.95

        return valor


class Casa(Imovel):
    def __init__(self, quartos, garagem):
        super().__init__("Casa", 900.0)
        self.quartos = quartos
        self.garagem = garagem

    def calcular_aluguel(self):
        valor = self.valor_base

        if self.quartos == 2:
            valor += 250.0

        if self.garagem:
            valor += 300.0

        return valor


class Estudio(Imovel):
    def __init__(self, vagas):
        super().__init__("Estúdio", 1200.0)
        self.vagas = vagas

    def calcular_aluguel(self):
        valor = self.valor_base

        if self.vagas >= 2:
            valor += 250.0
            if self.vagas > 2:
                valor += (self.vagas - 2) * 60.0

        return valor


class Orcamento:
    VALOR_CONTRATO = 2000.0

    def __init__(self, imovel, parcelas_contrato):
        self.imovel = imovel
        self.parcelas_contrato = parcelas_contrato

    def calcular_parcela_contrato(self):
        return self.VALOR_CONTRATO / self.parcelas_contrato

    def exibir_resumo(self):
        aluguel = self.imovel.calcular_aluguel()
        parcela_contrato = self.calcular_parcela_contrato()

        print("\n===== ORÇAMENTO DE LOCAÇÃO =====")
        print(f"Tipo de imóvel: {self.imovel.tipo}")
        print(f"Valor do aluguel mensal: R$ {aluguel:.2f}")
        print(f"Valor total do contrato: R$ {self.VALOR_CONTRATO:.2f}")
        print(
            f"Contrato parcelado em {self.parcelas_contrato}x de R$ {parcela_contrato:.2f}"
        )

    def gerar_csv(self, nome_arquivo="orcamento.csv"):
        aluguel = self.imovel.calcular_aluguel()
        parcela_contrato = self.calcular_parcela_contrato()

        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(
                ["Mês", "Aluguel Mensal", "Parcela do Contrato", "Total do Mês"]
            )

            for mes in range(1, 13):
                if mes <= self.parcelas_contrato:
                    contrato_mes = parcela_contrato
                else:
                    contrato_mes = 0.0

                total_mes = aluguel + contrato_mes

                escritor.writerow(
                    [
                        mes,
                        f"{aluguel:.2f}",
                        f"{contrato_mes:.2f}",
                        f"{total_mes:.2f}",
                    ]
                )

        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")


def ler_sim_ou_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ["s", "n"]:
            return resposta == "s"
        print("Digite apenas 's' para sim ou 'n' para não.")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")


def main():
    print("===== SISTEMA DE ORÇAMENTO IMOBILIÁRIO =====")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")

    opcao = input("Escolha o tipo de imóvel: ").strip()

    imovel = None

    if opcao == "1":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_ou_nao("Possui garagem? (s/n): ")
        sem_criancas = ler_sim_ou_nao("A pessoa NÃO possui crianças? (s/n): ")
        imovel = Apartamento(quartos, garagem, sem_criancas)

    elif opcao == "2":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_ou_nao("Possui garagem? (s/n): ")
        imovel = Casa(quartos, garagem)

    elif opcao == "3":
        vagas = ler_inteiro("Quantidade de vagas de estacionamento: ", 0)
        imovel = Estudio(vagas)

    else:
        print("Opção inválida.")
        return

    parcelas_contrato = ler_inteiro(
        "Parcelar o contrato em quantas vezes? (1 a 5): ", 1, 5
    )

    orcamento = Orcamento(imovel, parcelas_contrato)
    orcamento.exibir_resumo()

    exportar = ler_sim_ou_nao("Deseja gerar arquivo CSV? (s/n): ")
    if exportar:
        orcamento.gerar_csv()


if __name__ == "__main__":
    main()