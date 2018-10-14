"""Scraper do Banco do Brasil """
from datetime import datetime
from decimal import Decimal
from random import randint

import requests
from requests.adapters import HTTPAdapter

from bbscraper.urls import API_ENDPOINT, HASH_URL, LOGIN_URL, SALDO_URL, TRANSACOES_URL


class MobileSession(requests.Session):
    def __init__(self):
        super().__init__()

        self.mount(API_ENDPOINT, HTTPAdapter(max_retries=32, pool_connections=50, pool_maxsize=50))
        self.headers.update({
            'User-Agent' :  'Apple; iPad2,1; iPhone OS; 9.3.5; 13G36; mov-iphone-app; 3.42.0.1; pt_BR; 00; 00; WIFI; isSmartphone=false;',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        })


class BancodoBrasilScraper:
    """Scraper do Banco do Brasil"""

    def __init__(self, agencia, conta, senha):
        self.agencia = agencia
        self.conta = conta
        self.senha = senha

        self.id_dispositivo = '000000000000000'
        self.ida = '00000000000000000000000000000000'
        self.nick = f'NICKRANDOM.{randint(1000, 99999)}'
        
        self.idh = ''
        self.mci = ''
        self.segmento = '' # PESSOA FISICA
        
        self.session = MobileSession()
    
    def login(self):
        hash_data = {
            'hash': '',
            'idh': '',
            'id': self.ida,
            'idDispositivo': self.id_dispositivo,
            'apelido': self.nick
        }

        response = self.session.post(HASH_URL, data=hash_data)
        self.idh = response.content

        login_data = {
            'idh': self.idh,
            'senhaConta': self.senha,
            'apelido': self.nick,
            'dependenciaOrigem': self.agencia,
            'numeroContratoOrigem': self.conta,
            'idRegistroNotificacao': '',
            'idDispositivo': self.id_dispositivo,
            'titularidade': 1
        }

        response = self.session.post(LOGIN_URL, data=login_data)
        if bytes('CODIGO NAO CONFERE', 'utf-8') in response.content or bytes('G176-845', 'utf-8') in response.content:
            print('[!] Login failed, invalid credentials')
        elif bytes('SENHA BLOQUEADA', 'utf-8') in response.content:
            print('[!] Login failed, account locked')
        
        try:  
            json_response = response.json()['login']
        except json.decoder.JsonDecodeError as e:
            print("Expecting Value")
        #else:
            #print(f'json response: {json_response}')
            #print(f"(<DONO:{json_response['nomeCliente']}>, <MCI: {json_response['mci']}>, <Segmento: {json_response['segmento']}>)")
        
        return json_response
    
    def saldo(self):
        saldo_data = {
            'servico/ServicoSaldo/saldo': '',
            'idh': self.idh,
            'idDispositivo': self.id_dispositivo,
            'apelido': self.nick
        }

        response = self.session.post(SALDO_URL, data=saldo_data)
        json_response = response.json()['servicoSaldo']
        json_saldo = json_response['saldo']
        saldo = Decimal(json_saldo.split()[0].replace('.', '').replace(',', '.')) * -1 if json_saldo.split()[-1] == 'D' else float(json_saldo.split()[0].replace('.', '').replace(',', '.'))
        
        return saldo

    def extrato(self):
        payload = {
            'abrangencia': 8,
            'idh': self.idh,
            'idDispositivo': self.id_dispositivo,
            'apelido': self.nick
        }

        response = self.session.post(TRANSACOES_URL, data=payload)

        json_response = response.json()

        sessoes = json_response['conteiner']['telas'][0]['sessoes']

        transacoes = []
        for s in sessoes:
            if s['TIPO'] == 'sessao' and s.get('cabecalho'):
                if s['cabecalho'].startswith('M') and 'ncia:' in s['cabecalho']:
                    month = s['cabecalho'].split()[-3:]

                    for tt in s['celulas']:
                        if tt['TIPO'] == 'celula':
                            if len(tt['componentes']) == 3 and tt['componentes'][0]['componentes'][0]['texto'] != 'Dia':
                                description = tt['componentes'][1]['componentes'][0]['texto']
                                date = self.parse_date(tt['componentes'][0]['componentes'][0]['texto'], month[0], month[2]).date()
                                value = Decimal(tt['componentes'][2]['componentes'][0]['texto'].split()[0].replace('.', '').replace(',', '.'))
                                sign = '-' if tt['componentes'][2]['componentes'][0]['texto'].split()[-1] == 'D' else '+'
                                raw = tt['componentes']
                                transacoes.append({'description': description, 'date': date, 'value': value}) # , 'sign': sign, 'raw': raw
                            else:
                                continue
                elif s['cabecalho'].startswith('Informa') and s['cabecalho'].endswith('es adicionais'):
                    for tt in s['celulas']:
                        if tt['TIPO'] == 'celula':
                            if tt['componentes'][0]['componentes'][0]['texto'] == 'Juros':
                                val = Decimal(tt['componentes'][1]['componentes'][0]['texto'].split()[-1].replace('.', '').replace(',', '.'))

        return transacoes

    def parse_date(self, day, month, year):

        m2n = {
            'Janeiro': 1,
            'Fevereiro': 2,
            'Marco': 3,
            'Março': 3,
            'Abril': 4,
            'Maio': 5,
            'Junho': 6,
            'Julho': 7,
            'Agosto': 8,
            'Setembro': 9,
            'Outubro': 10,
            'Novembro': 11,
            'Dezembro': 12
        }

        return datetime.strptime('{}/{}/{}'.format(day, m2n[month], year), '%d/%m/%Y')
    
    def __str__(self):
        return f"<Agencia: {self.agencia}, Conta: {self.conta}>"
