"""Comand Line Interface"""
import argparse
from getpass import getpass

from tabulate import tabulate

from bbscraper.scraper import BancodoBrasilScraper


def csv(data):
    lines = (','.join((str(col) for _, col in row.items()) )  for row in data)
    return "\n".join(lines)

def table(data):
    return tabulate(data, headers="keys", floatfmt='.2f', tablefmt="fancy_grid")


def main():
    parser = argparse.ArgumentParser(
        description='Programa para parsear transações financeiras do Banco do Brasil')
    parser.add_argument(
        '--agencia', '-a', help='Número da agência do Banco do Brasil, no formato 00000', required=True)
    parser.add_argument(
        '--conta', '-c', help='Número da conta do Banco do Brasil, no formato 00000', required=True)
    parser.add_argument('--senha', '-s', help='Senha da Conta do Banco do Brasil')
    parser.add_argument(
        '--dias', help='Log de Transações dos últimos dias. default é 15 dias.', default=15, type=int)
    parser.add_argument(
        '--saldo', dest='saldo', action='store_true', help='Busca somente o saldo da conta.')
    parser.add_argument(
        '--extrato', dest='extrato', action='store_true', help='Busca o extrato da conta.')
    parser.add_argument(
        '--csv', help='Imprime os dados em CSV.', dest='output', action='store_const', const=csv, 
        default=table)

    args = parser.parse_args()

    if not (args.saldo or args.extrato):
        parser.exit(0, "Indique a operação: --saldo ou --extrato\n")
    
    senha = args.senha or getpass("Digite sua senha do Banco do Brasil: ")
    if not senha:
        parser.exit(0, "Você não digitou a senha!\n")
    
    if len(senha) < 8:
        parser.exit(0, "Digite a senha de 8 dígitos!\n")
    output = args.output # csv or table (default)
    bb = BancodoBrasilScraper(args.agencia, args.conta, senha)
    print(bb)
    assert bb.login()
    print()

    if args.saldo:
        print(f'Saldo: R${bb.saldo()}')
    if args.extrato:
        print(output(bb.extrato()))
