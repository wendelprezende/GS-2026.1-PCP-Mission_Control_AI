MISSION CONTROL AI - GS 2026.1

1. DESCRIÇÃO DO PROJETO
-----------------------
   O Controle Inteligente de Missão é um sistema desenvolvido em Python que simula o monitoramento inteligente de uma missão espacial experimental. O sistema organiza dados simulados de sensores em ciclos de monitoramento, analisa automaticamente as condições de cada ciclo, gera alertas e recomendações, e apresenta um relatório final da missão no terminal.

   A inteligência do sistema é baseada em regras lógicas: cada sensor recebe uma classificação (NORMAL, ATENÇÃO ou CRÍTICO) com base em limites predefinidos. Essa classificação gera uma pontuação de risco que, acumulada ao longo dos ciclos, permite identificar tendências e a área mais afetada da missão.

2. PRÉ-REQUISITO E COMO EXECUTAR
--------------------------------

  Pré-requisito: Python 3 instalado.

  No terminal, dentro da pasta do projeto, execute:

    python mission_control_ai.py

  Não é necessário instalar nenhuma biblioteca externa.
  O programa não possui interface gráfica nem entrada de dados pelo usuário. Todos os dados já estão fixos no código e a execução é automática do início ao fim.

3. ESTRUTURA PRINCIPAL DOS DADOS
--------------------------------

  3.1 CONSTANTE DE NOME

    NOME_MISSAO = "Controle Inteligente de Missão"

    Constante que armazena o nome da missão.

  ----

  3.2 LISTA DE ÁREAS MONITORADAS

    areas_monitoradas = [
        "Temperatura interna",
        "Comunicação com a base",
        "Sistema de energia",
        "Suporte de oxigênio",
        "Estabilidade operacional"
    ]

    Lista com os nomes das cinco áreas monitoradas. Cada posição desta lista corresponde a uma coluna da matriz dados_missao.
    É usada no relatório final para nomear as áreas ao exibir a pontuação acumulada e identificar a área mais afetada.

  ----

  3.3 MATRIZ PRINCIPAL — dados_missao

    dados_missao = [
        [22, 85, 80, 95, 88],   # Ciclo 1
        [32, 68, 65, 92, 72],   # Ciclo 2
        [34, 45, 42, 88, 58],   # Ciclo 3
        [38, 25, 18, 77, 32],   # Ciclo 4
        [33, 35, 22, 83, 45],   # Ciclo 5
        [21, 70, 55, 91, 75]    # Ciclo 6
    ]

    A estrutura central do programa. É uma lista de listas (matriz), onde cada linha representa um ciclo de monitoramento e cada coluna representa um sensor, na seguinte ordem obrigatória:

    Posição │ Sensor        │ Unidade
    ────────┼───────────────┼─────────
       0    │ Temperatura   │ °C
       1    │ Comunicação   │ %
       2    │ Bateria       │ %
       3    │ Oxigênio      │ %
       4    │ Estabilidade  │ %

    Narrativa dos ciclos:
      Ciclo 1 → Início estável: todos os parâmetros nominais
      Ciclo 2 → Anomalia térmica isolada
      Ciclo 3 → Degradação moderada em múltiplos sistemas
      Ciclo 4 → Crise generalizada
      Ciclo 5 → Recuperação parcial após intervenção
      Ciclo 6 → Estabilização e retorno ao estado operacional

4. FUNÇÕES DO SISTEMA
---------------------

  O sistema possui exatamente 5 funções, cada uma com uma
  responsabilidade bem definida.

  ----

  FUNÇÃO 1 — analisar_sensor(valor, tipo)

    Recebe o valor numérico lido de um sensor e o nome do seu tipo ("temperatura", "comunicacao", "bateria", "oxigenio" ou "estabilidade"). Aplica os limites de classificação correspondentes ao tipo recebido usando estruturas if/elif encadeadas. Retorna com com três elementos: a classificação em texto (NORMAL, ATENÇÃO ou CRÍTICO), a descrição textual do estado do sensor e a pontuação de risco (0, 1 ou 2).

    Esta função é a base de toda a análise do sistema. É chamada dentro do loop principal para cada um dos cinco sensores de cada ciclo.

  ----

  FUNÇÃO 2 — classificar_ciclo(pontuacao)

    Recebe a pontuação total do ciclo (soma dos pontos de risco dos cinco sensores, valor entre 0 e 10) e retorna uma string com a classificação correspondente:

      0 a 2 pontos  →  MISSÃO ESTÁVEL
      3 a 5 pontos  →  MISSÃO EM ATENÇÃO
      6 a 10 pontos →  MISSÃO CRÍTICA

    É chamada ao final de cada ciclo, após o loop interno somar todas as pontuações dos sensores.

  ----

  FUNÇÃO 3 — gerar_recomendacao(classificacoes, pontuacao)

    Recebe a lista geradas no ciclo (contendo tipo, classificação, descrição e pontos de cada sensor) e a pontuação total do ciclo. Gera a recomendação automática seguindo uma ordem de prioridade:

      1. Pontuação >= 8: emergência geral — ativa modo
         de segurança independente das áreas afetadas.
      2. Há áreas CRÍTICO: lista as ações específicas para
         cada área crítica encontrada no ciclo.
      3. Há áreas ATENÇÃO: recomenda monitoramento e plano
         de contingência.
      4. Sem alertas: recomenda manter operação normal.

    Retorna a recomendação como uma string. É chamada ao final de cada ciclo, logo após classificar_ciclo().

  ----

  FUNÇÃO 4 — analisar_tendencia(risco_inicial, risco_final)

    Recebe a pontuação do primeiro ciclo e a pontuação do último ciclo. Compara os dois valores e retorna uma string descrevendo a tendência geral da missão:

      risco_final > risco_inicial → "tendência de piora"
      risco_final < risco_inicial → "tendência de melhora"
      risco_final = risco_inicial → "permaneceu estável"

    É chamada dentro de gerar_relatorio_final(), passando o primeiro e o último elemento da lista de riscos.

  ----

  FUNÇÃO 5 — gerar_relatorio_final(nome_missao, resultados,
                                   pontuacoes_areas)

    Recebe o nome da missão, a lista de dicionários com os resultados de cada ciclo e a lista de pontuações acumuladas por área. Calcula e exibe o relatório consolidado completo da missão, incluindo:

      - Médias por sensor (temperatura, comunicação,
        bateria, oxigênio, estabilidade)
      - Ciclo mais crítico (maior pontuação individual)
      - Risco médio da missão
      - Quantidade de ciclos críticos
      - Tendência da missão (chamando analisar_tendencia)
      - Pontuação acumulada por área
      - Área mais afetada (maior pontuação acumulada)
      - Classificação final (baseada no risco médio)
      - Conclusão textual correspondente à classificação

    É a última chamada da execução principal.

5. REGRAS DE CLASSIFICAÇÃO DOS SENSORES
---------------------------------------

  Cada sensor é classificado com base em faixas de valores.
  A pontuação resultante é: NORMAL = 0 | ATENÇÃO = 1 | CRÍTICO = 2.

  5.1 TEMPERATURA (°C)

    Condição              │ Classificação
    ──────────────────────┼───────────────
    Menor que 18 °C       │ ATENÇÃO
    De 18 °C até 30 °C    │ NORMAL
    De 31 °C até 35 °C    │ ATENÇÃO
    Maior que 35 °C       │ CRÍTICO

  5.2 COMUNICAÇÃO (%)

    Condição              │ Classificação
    ──────────────────────┼───────────────
    Menor que 30%         │ CRÍTICO
    De 30% até 59%        │ ATENÇÃO
    60% ou mais           │ NORMAL

  5.3 BATERIA (%)

    Condição              │ Classificação
    ──────────────────────┼───────────────
    Menor que 20%         │ CRÍTICO
    De 20% até 49%        │ ATENÇÃO
    50% ou mais           │ NORMAL

  5.4 OXIGÊNIO (%)

    Condição              │ Classificação
    ──────────────────────┼───────────────
    Menor que 80%         │ CRÍTICO
    De 80% até 89%        │ ATENÇÃO
    90% ou mais           │ NORMAL

  5.5 ESTABILIDADE (%)

    Condição              │ Classificação
    ──────────────────────┼───────────────
    Menor que 40%         │ CRÍTICO
    De 40% até 69%        │ ATENÇÃO
    70% ou mais           │ NORMAL

6. LÓGICA DE PONTUAÇÃO E CLASSIFICAÇÃO DE CICLOS
------------------------------------------------

  Cada ciclo tem 5 sensores, cada um gerando 0, 1 ou 2 pontos. A pontuação máxima por ciclo é 10 pontos.

  Após somar os pontos dos cinco sensores, o ciclo é classificado por classificar_ciclo():

    0 a 2 pontos  → MISSÃO ESTÁVEL
    3 a 5 pontos  → MISSÃO EM ATENÇÃO
    6 a 10 pontos → MISSÃO CRÍTICA

  Exemplo de cálculo (Ciclo 4 da missão):

    Temperatura  38 °C → CRÍTICO   = 2 pontos
    Comunicação  25%   → CRÍTICO   = 2 pontos
    Bateria      18%   → CRÍTICO   = 2 pontos
    Oxigênio     77%   → CRÍTICO   = 2 pontos
    Estabilidade 32%   → CRÍTICO   = 2 pontos
                                   ─────────
    Total do ciclo                 = 10 pontos → MISSÃO CRÍTICA

7. IDENTIFICAÇÃO DA ÁREA MAIS AFETADA
-------------------------------------

  A lista pontuacoes_areas = [0, 0, 0, 0, 0] é incrementada a cada ciclo. Cada posição acumula os pontos de risco da área correspondente ao longo de todos os ciclos.

  Ao final da execução, gerar_relatorio_final() usa max() para localizar o maior valor acumulado e areas_monitoradas.index() para recuperar o nome da área correspondente.

  Resultado desta missão:

    Temperatura interna    → 5 pontos  ← ÁREA MAIS AFETADA
    Comunicação com a base → 4 pontos
    Sistema de energia     → 4 pontos
    Suporte de oxigênio    → 4 pontos
    Estabilidade operac.   → 4 pontos

8. ANÁLISE DE TENDÊNCIA
-----------------------

  A tendência é calculada por analisar_tendencia() comparando a pontuação do Ciclo 1 com a do Ciclo 6.

  Nesta missão:
    Risco do Ciclo 1 = 0 (todos NORMAL)
    Risco do Ciclo 6 = 0 (todos NORMAL)
    Resultado → A missão permaneceu estável em relação ao início.

9. FLUXO DE EXECUÇÃO DO PROGRAMA
------------------------------------------------------------

  O bloco if __name__ == "__main__" controla toda a execução:

    1. Inicializa resultados = [] e pontuacoes_areas = [0,0,0,0,0]
    2. Exibe cabeçalho da missão no terminal
    3. Loop externo: percorre os 6 ciclos de dados_missao
       3.1 Loop interno: percorre os 5 sensores do ciclo
           - Chama analisar_sensor(valor, tipo)
           - Acumula pontuacao_ciclo e pontuacoes_areas
           - Exibe linha do sensor formatada
       3.2 Chama classificar_ciclo(pontuacao_ciclo)
       3.3 Chama gerar_recomendacao(classificacoes, pontuacao)
       3.4 Exibe pontuação, classificação e recomendação do ciclo
       3.5 Adiciona dicionário do ciclo à lista resultados
    4. Chama gerar_relatorio_final(NOME_MISSAO, resultados,
                                   pontuacoes_areas)

  O bloco if __name__ == "__main__" garante que o código só executa quando o arquivo é rodado diretamente, e não quando importado por outro módulo.

10. EXEMPLO DE SAÍDA NO TERMINAL
--------------------------------

  ============================================================
  MISSION CONTROL AI
  ============================================================
  Missão: Mission Control AI
  Quantidade de ciclos analisados: 6
  ============================================================

  CICLO 1
  ------------------------------------------------------------
  Temperatura   : 22 °C | NORMAL | Temperatura estável
  Comunicação   : 85%   | NORMAL | Comunicação estável
  Bateria       : 80%   | NORMAL | Energia estável
  Oxigênio      : 95%   | NORMAL | Oxigênio adequado
  Estabilidade  : 88%   | NORMAL | Estabilidade operacional adequada
  Pontuação de risco do ciclo: 0
  Classificação do ciclo     : MISSÃO ESTÁVEL
  Recomendação               : Manter operação normal e continuar monitoramento.

  [... ciclos 2 a 5 omitidos neste exemplo ...]

  CICLO 4
  ------------------------------------------------------------
  Temperatura   : 38 °C | CRÍTICO | Risco de superaquecimento
  Comunicação   : 25%   | CRÍTICO | Comunicação com a base em nível crítico
  Bateria       : 18%   | CRÍTICO | Bateria em nível crítico
  Oxigênio      : 77%   | CRÍTICO | Oxigênio em nível crítico
  Estabilidade  : 32%   | CRÍTICO | Estabilidade operacional crítica
  Pontuação de risco do ciclo: 10
  Classificação do ciclo     : MISSÃO CRÍTICA
  Recomendação               : Ativar modo de segurança e priorizar
                               suporte à vida, energia e comunicação.

  ============================================================
  RELATÓRIO FINAL DA MISSÃO
  ============================================================
  Missão: Mission Control AI
  Quantidade de ciclos analisados: 6
  Média de temperatura   : 30.0 °C
  Média de comunicação   : 54.67%
  Média de bateria       : 47.0%
  Média de oxigênio      : 87.67%
  Média de estabilidade  : 61.67%
  Ciclo mais crítico     : Ciclo 4
  Maior pontuação de risco: 10
  Risco médio da missão  : 3.5
  Ciclos críticos        : 1

  Tendência da missão:
    A missão permaneceu estável em relação ao início.

  Pontuação acumulada por área:
    Temperatura interna: 5 pontos
    Comunicação com a base: 4 pontos
    Sistema de energia: 4 pontos
    Suporte de oxigênio: 4 pontos
    Estabilidade operacional: 4 pontos

  Área mais afetada:
    Temperatura interna

  Classificação final da missão:
    MISSÃO EM ATENÇÃO

  Conclusão:
    A missão apresentou instabilidade relevante durante a operação.
    A equipe deve manter o plano de contingência ativo.
  ============================================================
