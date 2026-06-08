# CONTROLE INTELIGENTE DE MISSÃO - GS 2026.1

# DADOS DA MISSÃO

NOME_MISSAO = "Controle Inteligente de Missão"

# Lista de áreas monitoradas
areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]

# Matriz principal, cada linha é um ciclo
dados_missao = [
    [22, 85, 80, 95, 88],   # Ciclo 1 - Início dentro dos parâmetros nominais
    [32, 68, 65, 92, 72],   # Ciclo 2 - Anomalia térmica isolada
    [34, 45, 42, 88, 58],   # Ciclo 3 - Degradação moderada em múltiplos sistemas
    [38, 25, 18, 77, 32],   # Ciclo 4 - Crise generalizada
    [33, 35, 22, 83, 45],   # Ciclo 5 - Recuperação parcial após intervenção
    [21, 70, 55, 91, 75]    # Ciclo 6 - Estabilização e retorno ao estado operacional
]

# FUNÇÕES

# Recebe o valor numérico de um sensor e seu tipo, e retorna com três elementos: a classificação (NORMAL / ATENÇÃO / CRÍTICO), a descrição do estado e a pontuação de risco correspondente (0, 1 ou 2)
def analisar_sensor(valor, tipo):
    if tipo == "temperatura":
        if valor < 18:
            return "ATENÇÃO", "Temperatura abaixo do ideal", 1
        elif valor <= 30:
            return "NORMAL", "Temperatura estável", 0
        elif valor <= 35:
            return "ATENÇÃO", "Temperatura elevada", 1
        else:
            return "CRÍTICO", "Risco de superaquecimento", 2

    elif tipo == "comunicacao":
        if valor < 30:
            return "CRÍTICO", "Comunicação com a base em nível crítico", 2
        elif valor < 60:
            return "ATENÇÃO", "Comunicação instável", 1
        else:
            return "NORMAL", "Comunicação estável", 0

    elif tipo == "bateria":
        if valor < 20:
            return "CRÍTICO", "Bateria em nível crítico", 2
        elif valor < 50:
            return "ATENÇÃO", "Bateria abaixo do recomendado", 1
        else:
            return "NORMAL", "Energia estável", 0

    elif tipo == "oxigenio":
        if valor < 80:
            return "CRÍTICO", "Oxigênio em nível crítico", 2
        elif valor < 90:
            return "ATENÇÃO", "Oxigênio abaixo do ideal", 1
        else:
            return "NORMAL", "Oxigênio adequado", 0

    elif tipo == "estabilidade":
        if valor < 40:
            return "CRÍTICO", "Estabilidade operacional crítica", 2
        elif valor < 70:
            return "ATENÇÃO", "Estabilidade operacional reduzida", 1
        else:
            return "NORMAL", "Estabilidade operacional adequada", 0


# Recebe a pontuação total do ciclo (0 a 10) e retorna a string de classificação
def classificar_ciclo(pontuacao):
    if pontuacao <= 2:
        return "MISSÃO ESTÁVEL"
    elif pontuacao <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


# Recebe a lista de classificações do ciclo e a pontuação total, e retorna a recomendação automática como string
# Se houver múltiplas áreas críticas, todas são listadas na recomendação
def gerar_recomendacao(classificacoes, pontuacao):

    # Pontuação muito alta: recomendação de emergência geral
    if pontuacao >= 8:
        return "Ativar modo de segurança e priorizar suporte à vida, energia e comunicação."

    # Identifica as entradas classificadas como CRÍTICO
    criticos = [c for c in classificacoes if c[1] == "CRÍTICO"]

    if criticos:
        acoes = []
        for entrada in criticos:
            tipo = entrada[0]
            if tipo == "temperatura":
                acoes.append("verificar controle térmico da missão")
            elif tipo == "comunicacao":
                acoes.append("tentar restabelecer contato com a base")
            elif tipo == "bateria":
                acoes.append("ativar modo de economia de energia")
            elif tipo == "oxigenio":
                acoes.append("acionar protocolo de suporte à vida")
            elif tipo == "estabilidade":
                acoes.append("reduzir operações não essenciais")
        texto = "; ".join(acoes)
        return texto[0].upper() + texto[1:] + "."

    # Verifica se há pelo menos uma área em atenção
    atencoes = [c for c in classificacoes if c[1] == "ATENÇÃO"]
    if atencoes:
        return "Monitorar sistemas em atenção e preparar plano de contingência."

    return "Manter operação normal e continuar monitoramento."


# Compara o risco do primeiro ciclo com o do último e retorna uma string descrevendo a tendência geral da missão (piora, melhora ou estabilidade)
def analisar_tendencia(risco_inicial, risco_final):
    if risco_final > risco_inicial:
        return "A missão apresentou tendência de piora."
    elif risco_final < risco_inicial:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão permaneceu estável em relação ao início."


# Gera e exibe o relatório final da missão, incluindo médias, ciclos críticos, tendência e área mais afetada
def gerar_relatorio_final(nome_missao, resultados, pontuacoes_areas):
    total_ciclos = len(resultados)
    riscos = [r["pontuacao"] for r in resultados]

    media_temp = round(sum(r["temperatura"] for r in resultados) / total_ciclos, 2)
    media_com  = round(sum(r["comunicacao"] for r in resultados) / total_ciclos, 2)
    media_bat  = round(sum(r["bateria"] for r in resultados) / total_ciclos, 2)
    media_ox   = round(sum(r["oxigenio"] for r in resultados) / total_ciclos, 2)
    media_est  = round(sum(r["estabilidade"] for r in resultados) / total_ciclos, 2)

    risco_medio = round(sum(riscos) / total_ciclos, 2)

    ciclo_mais_critico = max(resultados, key=lambda r: r["pontuacao"])
    ciclos_criticos    = sum(1 for r in resultados if r["classificacao"] == "MISSÃO CRÍTICA")

    tendencia          = analisar_tendencia(riscos[0], riscos[-1])

    # Identifica a área com maior acúmulo de risco ao longo de todos os ciclos
    max_pontos        = max(pontuacoes_areas)
    area_mais_afetada = areas_monitoradas[pontuacoes_areas.index(max_pontos)]

    # Classificação final baseada no risco médio arredondado
    classificacao_final = classificar_ciclo(round(risco_medio))

    print()
    print("RELATÓRIO FINAL DA MISSÃO")
    print()
    print("Missão: " + nome_missao)
    print("Quantidade de ciclos analisados: " + str(total_ciclos))
    print("Média de temperatura: " + str(media_temp) + " °C")
    print("Média de comunicação: " + str(media_com) + "%")
    print("Média de bateria: " + str(media_bat) + "%")
    print("Média de oxigênio: " + str(media_ox) + "%")
    print("Média de estabilidade: " + str(media_est) + "%")
    print("Ciclo mais crítico: Ciclo " + str(ciclo_mais_critico["numero"]))
    print("Maior pontuação de risco: " + str(ciclo_mais_critico["pontuacao"]))
    print("Risco médio da missão: " + str(risco_medio))
    print("Ciclos críticos: " + str(ciclos_criticos))
    print()
    print("Tendência da missão:")
    print("  " + tendencia)
    print()
    print("Pontuação acumulada por área:")
    for i in range(len(areas_monitoradas)):
        print("  " + areas_monitoradas[i] + ": " + str(pontuacoes_areas[i]) + " pontos")
    print()
    print("Área mais afetada:")
    print("  " + area_mais_afetada)
    print()
    print("Classificação final da missão:")
    print("  " + classificacao_final)
    print()
    print("Conclusão:")
    if classificacao_final == "MISSÃO CRÍTICA":
        print("  A missão enfrentou situações de risco severo. Intervenção")
        print("  imediata é necessária para garantir a segurança operacional.")
    elif classificacao_final == "MISSÃO EM ATENÇÃO":
        print("  A missão apresentou instabilidade relevante durante a operação.")
        print("  A equipe deve manter o plano de contingência ativo.")
    else:
        print("  A missão foi concluída dentro dos parâmetros operacionais.")
        print("  Todos os sistemas se mantiveram dentro do esperado.")
    print("=" * 60)

# EXECUÇÃO PRINCIPAL

if __name__ == "__main__":

    tipos = ["temperatura", "comunicacao", "bateria", "oxigenio", "estabilidade"]

    # Listas de acúmulo entre ciclos
    resultados        = []
    pontuacoes_areas  = [0, 0, 0, 0, 0]  # Para acumular pontos por área ao longo de todos os ciclos

    print("=" * 60)
    print("Controle Inteligente de Missão")
    print("=" * 60)
    print("Missão: " + NOME_MISSAO)
    print("Quantidade de ciclos analisados: " + str(len(dados_missao)))
    print("=" * 60)

    # Percorre cada ciclo da matriz dados_missao
    for i in range(len(dados_missao)):
        ciclo        = dados_missao[i]
        numero_ciclo = i + 1

        print("\nCICLO " + str(numero_ciclo))
        print("-" * 60)

        pontuacao_ciclo = 0
        classificacoes  = []   # lista (tipo, classificação, descrição, pontos)

        # Analisa cada um dos cinco sensores do ciclo atual
        for j in range(len(ciclo)):
            valor = ciclo[j]
            tipo  = tipos[j]

            classificacao, descricao, pontos = analisar_sensor(valor, tipo)

            pontuacao_ciclo      += pontos
            pontuacoes_areas[j]  += pontos
            classificacoes.append((tipo, classificacao, descricao, pontos))

            # Formata e exibe a linha do sensor com valor, classificação e descrição
            if tipo == "temperatura":
                linha = "Temperatura   : " + str(valor) + " °C"
            elif tipo == "comunicacao":
                linha = "Comunicação   : " + str(valor) + "%"
            elif tipo == "bateria":
                linha = "Bateria       : " + str(valor) + "%"
            elif tipo == "oxigenio":
                linha = "Oxigênio      : " + str(valor) + "%"
            else:
                linha = "Estabilidade  : " + str(valor) + "%"

            print(linha + " | " + classificacao + " | " + descricao)

        classificacao_ciclo = classificar_ciclo(pontuacao_ciclo)
        recomendacao        = gerar_recomendacao(classificacoes, pontuacao_ciclo)

        print("Pontuação de risco do ciclo: " + str(pontuacao_ciclo))
        print("Classificação do ciclo: " + classificacao_ciclo)
        print("Recomendação: " + recomendacao)

        # Armazena o resultado do ciclo para uso no relatório final
        resultados.append({
            "numero"      : numero_ciclo,
            "temperatura" : ciclo[0],
            "comunicacao" : ciclo[1],
            "bateria"     : ciclo[2],
            "oxigenio"    : ciclo[3],
            "estabilidade": ciclo[4],
            "pontuacao"   : pontuacao_ciclo,
            "classificacao": classificacao_ciclo
        })

    print()
    gerar_relatorio_final(NOME_MISSAO, resultados, pontuacoes_areas)