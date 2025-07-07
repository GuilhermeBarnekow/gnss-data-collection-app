# Documentação do Projeto Python GNSS

Este projeto é uma aplicação Python para trabalhar com dados GNSS (Global Navigation Satellite System). A seguir, uma descrição dos principais componentes e funcionalidades do projeto para que outra IA possa entender o que foi feito.

## Arquivos Principais

- **db_module.py**  
  Módulo responsável pela manipulação do banco de dados. Contém funções para armazenar, recuperar e gerenciar os dados coletados do GNSS.

- **gps_module.py**  
  Módulo que gerencia a comunicação com o dispositivo GNSS. Inclui funções para inicializar o dispositivo, ler dados de satélite, processar sinais e interpretar as informações recebidas.

- **main.py**  
  Arquivo principal que orquestra a execução do programa. Inicializa os módulos, configura o ambiente e controla o fluxo geral da aplicação.

- **ui.kv**  
  Arquivo de interface gráfica (usando Kivy) que define a aparência e os elementos visuais da aplicação.

- **requirements.txt**  
  Lista de dependências Python necessárias para executar o projeto.

## Funcionalidades

- Inicialização e configuração do dispositivo GNSS.
- Leitura contínua dos dados de satélite.
- Processamento e armazenamento dos dados em banco.
- Interface gráfica para visualização e controle da aplicação.

## Considerações Técnicas

- O projeto é desenvolvido em Python e utiliza a biblioteca Kivy para a interface gráfica.
- A comunicação com o dispositivo GNSS é feita via porta serial, com configuração de parâmetros como baud rate.
- O banco de dados pode ser local, utilizando SQLite ou outro sistema suportado.

---

Esta documentação serve para que outras inteligências artificiais possam compreender a estrutura e o funcionamento do projeto, facilitando manutenção, extensão e integração futura.
