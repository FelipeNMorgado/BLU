# BLU - Best Location for Urban Parking

<p align="center">
  <img src="docs/logo.png" alt="BLU Logo" width="250"/>
</p>

## Sobre o Projeto

O **BLU (Best Location for Urban Parking)** é uma solução inteligente para monitoramento de vagas de estacionamento urbano, desenvolvida com o objetivo de modernizar o sistema de Zona Azul por meio de tecnologias de **IoT**, **Visão Computacional**, **Machine Learning** e **Monitoramento em Tempo Real**.

O projeto surgiu da necessidade de reduzir o tempo gasto pelos motoristas na busca por vagas disponíveis, contribuindo para a diminuição dos congestionamentos e para uma melhor organização dos espaços urbanos.

Atualmente, muitos sistemas de estacionamento não fornecem informações em tempo real sobre a ocupação das vagas, obrigando os condutores a procurarem manualmente por locais livres. O BLU propõe uma solução automatizada capaz de identificar e disponibilizar essas informações de forma rápida e eficiente.

---

## Objetivos

- Monitorar automaticamente a ocupação das vagas de estacionamento.
- Informar aos usuários quais vagas estão disponíveis em tempo real.
- Reduzir congestionamentos causados pela procura de estacionamento.
- Aumentar a rotatividade das vagas da Zona Azul.
- Contribuir para uma mobilidade urbana mais eficiente.
- Permitir futuras análises preditivas utilizando Machine Learning.

---

## Arquitetura do Sistema

O sistema é composto por três módulos principais:

### Coleta de Dados
Responsável por identificar a ocupação das vagas através de sensores e/ou visão computacional.

### Comunicação
Envio dos dados coletados para a infraestrutura de processamento.

### Plataforma de Monitoramento
Recebe, processa e disponibiliza as informações para os usuários através de uma interface digital.

```text
┌───────────────┐
│ Sensores/Câmeras │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Processamento │
│ Machine Learning │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Plataforma Web │
│ Monitoramento  │
└───────────────┘
```

---

## Tecnologias Utilizadas

- Python
- Machine Learning
- Visão Computacional
- Internet das Coisas (IoT)
- Sensores Inteligentes
- Sistemas de Monitoramento em Tempo Real
- Banco de Dados
- Computação em Nuvem

---

## Dimensões das Vagas Monitoradas

| Tipo | Dimensões |
|--------|------------|
| Carro | 5,5m x 2,3m |
| Moto | 1,0m x 2,2m |

---

## Funcionalidades

- Detecção automática de ocupação das vagas.
- Atualização periódica das informações.
- Monitoramento em tempo real.
- Plataforma de visualização das vagas.
- Registro de dados para análises futuras.
- Previsão de demanda utilizando Machine Learning.
- Identificação de padrões de ocupação.
- Expansão para outras regiões urbanas.

---

## Metodologia

O desenvolvimento foi dividido nas seguintes etapas:

1. Pesquisa sobre estacionamentos inteligentes.
2. Levantamento de requisitos.
3. Modelagem da solução.
4. Desenvolvimento dos protótipos.
5. Implementação dos sistemas de monitoramento.
6. Testes de comunicação e detecção.
7. Validação dos resultados.

---

## Resultados Esperados

- Redução do tempo de busca por estacionamento.
- Maior rotatividade das vagas.
- Melhor organização urbana.
- Redução do tráfego desnecessário.
- Base de dados para análises inteligentes futuras.

---

## Equipe

Projeto desenvolvido por:

- Anderson Gomes Romão de Miranda Valença
- Arthur Vinícius Vieira Ventura
- Breno Monteiro Rodrigues Lira
- Felipe Nunes Morgado
- Lucas Ramon
- Lucas de Holanda Barros Soares
- Thiago Manguinho Rodrigues de Sousa
- Jimmy Paul Souza Barreto
- Izabella Nunes de Vasconcelos

---

## Publicação

Este projeto foi apresentado na **Mostra Nacional de Robótica (MNR 2025)**.

**Artigo:** *BLU - Best Location for Urban Parking*

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

## Visão de Futuro

O BLU busca evoluir para uma plataforma completa de gestão de estacionamento urbano, incorporando:

- Predição de disponibilidade de vagas.
- Integração com aplicativos de navegação.
- Dashboards para gestores públicos.
- Expansão para cidades inteligentes (*Smart Cities*).

