import itertools
from math import min


class Carta:
    naipe: str
    valor: int

    def __init__(self, naipe: str, valor: str):
        self.naipe = naipe
        self.valor = valor

    # C = copas, E = espadas, O = ouros, P = paus
    # 3C = 3 de copas, KQ = rei de ouros...
    def __init__(self, nome: str):
        valor = nome[0]
        naipe = nome[1]
        self.naipe = naipe
        self.valor = valor

    def __init__(self):
        pass


def faz_permutacao_cartas() -> list[Carta]:
    cartas = []
    for i in ['C', 'E', 'O', 'P']:
        for j in range(2, 14):
            if j < 10:
                j = str(j)
            elif j == 10:
                j = 'J'
            elif j == 11:
                j = 'Q'
            elif j == 12:
                j = 'K'
            elif j == 13:
                j = 'A'
            cartas.append(Carta(i, j))
    return itertools.permutations(cartas)


class EstadoDoJogoParaJogador:
    # info jogo
    mesa: list[Carta]
    mao: list[Carta]

    # info jogadores
    aposta_jogadores: list[int]
    banca_jogadores: list[int]
    aposta_total_jogadores: list[int]

    # numeros importantes
    aposta_minima: int
    precisa_aumentar: bool
    preco_de_ficar_no_jogo: int
    pote: int
    soma_bancas: int

    def __init__(self,
                 mesa: list[Carta],
                 mao: list[Carta],
                 aposta_jogadores: list[int],
                 aposta_total_jogadores: list[int],
                 banca_jogadores: list[int]):
        self.mesa = mesa
        self.mao = mao
        self.aposta_jogadores = aposta_jogadores
        self.banca_jogadores = banca_jogadores
        self.aposta_total_jogadores = aposta_total_jogadores

        self.aposta_minima = 0
        self.precisa_aumentar = False
        for aposta in aposta_jogadores:
            if aposta > self.aposta_minima:
                self.aposta_minima = aposta
                self.precisa_aumentar = True

        self.preco_de_ficar_no_jogo = aposta + max(self.aposta_total_jogadores)
        self.pote = sum(self.aposta_total_jogadores)
        self.soma_bancas = sum(self.banca_jogadores)


class CalculadoraDeVitoria:
    ordem_cartas: list[str]
    ordem_jogadas: list[function]

    def __init__(self):
        ordem_cartas = ['A', 'K', 'Q', 'J', '9',
                        '8', '7', '6', '5', '4', '3', '2']
        ordem_jogadas = [
            {
                'verifica': self.royal_straight_flush,
                'nome': "royal_straight_flush",
            },
            {
                'verifica': self.royal_flush,
                'nome': "royal_flush",
            },
            {
                'verifica': self.royal_straight,
                'nome': "royal_straight",
            },
            {
                'verifica': self.straight_flush,
                'nome': "straight_flush",
            },
            {
                'verifica': self.four_of_a_kind,
                'nome': "four_of_a_kind",
            },
            {
                'verifica': self.full_house,
                'nome': "full_house",
            },
            {
                'verifica': self.flush,
                'nome': "flush",
            },
            {
                'verifica': self.straight,
                'nome': "straight",
            },
            {
                'verifica': self.three_of_a_kind,
                'nome': "three_of_a_kind",
            },
            {
                'verifica': self.two_pairs,
                'nome': "two_pairs",
            },
            {
                'verifica': self.pair,
                'nome': "pair",
            },
            {
                'verifica': self.high_card,
                'nome': "high_card",
            },
        ]

    def is_mao_A_maior(self, maoA: list[Carta], maoB: list[Carta]):
        sumA = sum(maoA)
        sumB = sum(maoB)
        return sumA > sumB

    def get_maos_vencedoras(self, maos: list[list[Carta]], maos_do_jogador: list[list[Carta]]):
        for mao in maos:
            mao = sorted(
                mao, key=lambda carta: self.ordem_cartas.index(carta.valor))

        buckets = [[] for _ in range(len(self.ordem_jogadas))]
        for mao in maos:
            for is_jogada in self.ordem_jogadas:
                if is_jogada(mao):
                    buckets.append(maos.index(mao))

    def royal_straight_flush(self, mao) -> tuple[bool, list[Carta]]:
        pass

    def royal_flush(self, mao) -> tuple[bool, list[Carta]]:
        pass

    def royal_straight(self, mao) -> tuple[bool, list[Carta]]:
        pass

    def straight_flush(self, mao) -> tuple[bool, list[Carta]]:
        is_straight, cartas_straight = self.straight(mao)
        is_flush, cartas_flush = self.flush(mao)
        if is_straight and is_flush:
            return True, list(set(cartas_straight + cartas_flush))
        return False, None

    def four_of_a_kind(self, mao) -> tuple[bool, list[Carta]]:
        pass

    def full_house(self, mao) -> tuple[bool, list[Carta]]:
        pass

    def flush(self, mao) -> tuple[bool, list[Carta]]:
        last_valor = -1
        naipes = {'C': [], 'E': [], 'O': [], 'P': []}
        for carta in mao:
            if last_valor == -1:
                last_valor = carta.valor
                continue
            elif carta.valor == last_valor - 1:
                sequence_groups[-1:].append(carta)
            elif carta.valor < last_valor-1:
                last_valor = carta.valor
                sequence_groups.append([carta])
        seqs = sorted(sequence_groups, key=lambda seq: len(seq)).reverse()
        if len(seqs) > 0 and len(seqs[0]) >= 5:
            return True, seqs[0]
        return False, None

    def straight(self, mao) -> tuple[bool, list[Carta]]:
        last_valor = -1
        sequence_groups = []
        for carta in mao:
            if last_valor == -1:
                last_valor = carta.valor
                continue
            elif carta.valor == last_valor - 1:
                sequence_groups[-1:].append(carta)
            elif carta.valor < last_valor-1:
                last_valor = carta.valor
                sequence_groups.append([carta])
        seqs = sorted(sequence_groups, key=lambda seq: len(seq)).reverse()
        if len(seqs) > 0 and len(seqs[0]) >= 5:
            return True, seqs[0]
        return False, None

    def three_of_a_kind(self, mao) -> tuple[bool, list[Carta]]:
        grupos = self.__count_groups(mao)
        if len(grupos) > 1 and len(grupos[0]) > 2:
            return True, grupos[0]
        return False, None

    def two_pairs(self, mao) -> tuple[bool, list[Carta]]:
        grupos = self.__count_groups(mao)
        if len(grupos) > 1 and len(grupos[0]) > 1 and len(grupos[1]) > 1:
            return True, grupos[0]+grupos[1]
        return False, None

    def pair(self, mao) -> tuple[bool, list[Carta]]:
        grupos = self.__count_groups(mao)
        if len(grupos) > 0 and len(grupos[0]) > 1:
            return True, grupos[0]
        return False, None

    def high_card(self, mao) -> tuple[bool, list[Carta]]:
        return True, mao[0]

    # retorna grupos de cartas, sendo cada grupo uma lista de cartas
    # de igual valor. a resposta será ordenada do maior grupo para o menor
    def __count_groups(self, mao) -> list[list[Carta]]:
        valor_last = -1
        grp_index = -1
        grupos = []
        for carta in mao:
            if carta.valor == valor_last:
                grupos[grp_index].append(carta)
            else:
                valor_last = carta.valor
                grp_index += 1
                grupos.append([carta])
        return sorted(grupos, key=lambda grupo: len(grupo[0])).reverse()
