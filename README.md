Banco do Brasil Scraper
============

Scraper para baixar seus extratos do Banco do Brasil com um comando.

Como instalar
-------------

```console
$ pip install bbscraper
```

Motivação
---------

A ideia de fazer um scraper para o banco do brasil surgiu em um post do Henrique Bastos 
sobre como bancos ainda não oferecem uma forma fácil para seus clientes extraírem seus próprios dados.
Algo tão simples quanto obter o seu extrato bancário é um sofrimento para sistematizar, 
como ele mesmo comenta no post.

Então ele resolveu fazer um scraper para o banco Itaú, o [itauscraper](https://github.com/henriquebastos/itauscraper), onde você encontrará as motivações do Henrique e a descrição do projeto do scraper do Itáu.

As minhas motivações foram colocar em prática o que eu estou aprendendo em python, contribuir com
a comunidade e também por concordar com o Henrique nos pontos levantados.

Como funciona
-------------

O código usa [Python 3.6](https://www.python.org/) com a biblioteca [request](http://docs.python-requests.org/en/master/) e o [tabulate](https://pypi.python.org/pypi/tabulate) 
para formatar melhor a saída do extrato. 

O Henrique comenta em seu post que durante sua pesquisa sobre a existia de algo pronto para o Itaú ele 
encontrou o [bankscraper](https://github.com/kamushadenes/bankscraper) do
[Kamus](http://endurance.hyadesinc.com/) que disponibiliza vários scripts
interessantes. Então eu fui verificar e testar se o script do Banco do Brasil estava funcionado e não estava, mas era um problema simples na verificação do tamanho da conta e da agência.
Eu criei esse projeto para organizar melhor o código do kamus baseado no itauscraper e tentar deixá-lo
mais simples, não sei se consegui, mas fique a vontade para contribuir. 

Para acessar os dados é usado a API mobile, então usando o requests.Session conseguimos simular que
a requisição está sendo por uma aplicação mobile.

A classe BancodoBrasilScraper usa a session para realizar o login e consultar o extrato. 

Como Usar
-------------

```console
$ bbscraper --extrato --saldo  --agencia 12345 --conta 123456 
Digite sua senha do Banco do Brasil:
```

Ou:

```console
$ bbscraper --extrato --saldo  --agencia 12345 --conta 123456 --senha SECRET
```

Para conhecer todas as opções:

```console
$ bbscraper -h
```

Com Docker
----------

```console
$ docker build -t anderson89marques/bbscraper --no-cache .
```

```console
$ docker container run -it anderson89marques/bbscraper:latest  bbscraper --extrato --saldo --agencia 12345 --conta 123456
```


Development
-----------

```console
 git clone https://github.com/anderson89marques/bbscraper
 cd bbscraper

Sem docker
----------
```
 python -m venv -p python3.6 .venv
 source .venv/bin/activate
 pip install -r requirements.txt
```

Com docker
-------
```console
$ docker build -t anderson89marques/bbscraper --no-cache .
$ docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp anderson89marques/bbscraper python -m bbscraper --extrato --agencia 12345 --conta 123456


Licença
-------

Copyright (C) 2018 Anderson Marques.

Este código é distribuído nos termos da "GNU LGPLv3". Veja o arquivo LICENSE para detalhes.
