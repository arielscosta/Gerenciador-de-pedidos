import csv  # Importa a biblioteca para manipular arquivos CSV
import os  # Importa a biblioteca para interagir com o sistema operacional (verificar arquivos)
from datetime import datetime, timedelta  # Importa classes para manipulação de datas e horas

# --- Configurações de Arquivos ---
ARQUIVO_CABECALHO = 'pedidos_cabecalho.csv'  # Define o nome do arquivo que guarda o resumo dos pedidos
ARQUIVO_ITENS = 'pedidos_itens.csv'  # Define o nome do arquivo que guarda os produtos de cada pedido
ARQUIVO_PRODUTOS = 'produtos.csv'  # Define o nome do arquivo que serve como banco de dados de produtos

# Cabeçalhos dos arquivos 
CAMPOS_CABECALHO = [  # Lista com os nomes das colunas para o arquivo de cabeçalho
    'ID do Pedido', 'Data do Pedido', 'Nome do Cliente', 
    'Valor Total (R$)', 'Valor Pago (R$)', 'Forma de Pagamento', 
    'Status do Pagamento', 'Data do Pagamento', 'Data Vencimento Prazo', 
    'Status do Pedido', 'Data/Hora Entrega'
]

CAMPOS_ITENS = [  # Lista com os nomes das colunas para o arquivo de itens detalhados
    'ID do Item', 'ID do Pedido', 'Produto', 
    'Quantidade', 'Valor Item (R$)'
]

# --- Constantes para os Menus ---
OPCOES_STATUS_PAGAMENTO = ['Pago', 'Pendente', 'Parcial']  # Opções fixas para o estado financeiro do pedido
OPCOES_STATUS_PEDIDO = ['Entregue', 'Pendente']  # Opções fixas para o estado de logística do pedido
OPCOES_FORMA_PAGAMENTO = ['Pix', 'Dinheiro', 'Prazo']  # Opções fixas de métodos de pagamento

# =================================================================
#               FUNÇÕES DE INICIALIZAÇÃO E UTILIDADE 
# =================================================================

def inicializar_csv():  # Define a função que prepara os arquivos do sistema
    """Cria ou verifica os arquivos CSV com cabeçalhos."""
    if not os.path.exists(ARQUIVO_CABECALHO):  # Verifica se o arquivo de cabeçalho já existe
        with open(ARQUIVO_CABECALHO, mode='w', newline='', encoding='utf-8') as f:  # Abre para escrita se não existir
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_CABECALHO)  # Configura o gravador CSV com as colunas definidas
            escritor.writeheader()  # Escreve a primeira linha (títulos das colunas)
    
    if not os.path.exists(ARQUIVO_ITENS):  # Verifica se o arquivo de itens já existe
        with open(ARQUIVO_ITENS, mode='w', newline='', encoding='utf-8') as f:  # Abre para escrita se não existir
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_ITENS)  # Configura o gravador CSV
            escritor.writeheader()  # Escreve os títulos das colunas
    
def carregar_cabecalhos():  # Define a função para ler os pedidos do disco
    """Carrega todos os cabeçalhos de pedidos."""
    if not os.path.exists(ARQUIVO_CABECALHO):  # Se o arquivo não existir
        return []  # Retorna uma lista vazia
    with open(ARQUIVO_CABECALHO, mode='r', newline='', encoding='utf-8', errors='ignore') as f:  # Abre para leitura ignorando erros de caracteres
        leitor = csv.DictReader(f)  # Cria um leitor que transforma linhas em dicionários
        return list(leitor)  # Converte o leitor em uma lista de dados e retorna

def carregar_itens():  # Define a função para ler os produtos vendidos do disco
    """Carrega todos os itens de pedidos."""
    if not os.path.exists(ARQUIVO_ITENS):  # Se o arquivo não existir
        return []  # Retorna lista vazia
    with open(ARQUIVO_ITENS, mode='r', newline='', encoding='utf-8', errors='ignore') as f:  # Abre para leitura
        leitor = csv.DictReader(f)  # Transforma linhas em dicionários
        return list(leitor)  # Retorna a lista de todos os itens

def salvar_cabecalhos(cabecalhos):  # Define a função para gravar pedidos no disco
    """Salva a lista atualizada de cabeçalhos de pedidos."""
    with open(ARQUIVO_CABECALHO, mode='w', newline='', encoding='utf-8') as f:  # Abre o arquivo em modo de sobreescrita
        escritor = csv.DictWriter(f, fieldnames=CAMPOS_CABECALHO)  # Prepara o gravador
        escritor.writeheader()  # Escreve o cabeçalho novamente
        escritor.writerows(cabecalhos)  # Grava todos os dados da lista no arquivo

def salvar_itens(itens):  # Define a função para gravar os itens no disco
    """Salva a lista atualizada de itens de pedidos."""
    with open(ARQUIVO_ITENS, mode='w', newline='', encoding='utf-8') as f:  # Abre em modo de sobreescrita
        escritor = csv.DictWriter(f, fieldnames=CAMPOS_ITENS)  # Prepara o gravador
        escritor.writeheader()  # Escreve o cabeçalho
        escritor.writerows(itens)  # Grava a lista de itens

def gerar_novo_id_pedido(cabecalhos):  # Define a função para auto-incremento de ID de pedido
    """Gera o próximo ID sequencial para pedidos."""
    if not cabecalhos:  # Se a lista estiver vazia
        return 1  # Retorna o primeiro ID como 1
    max_id = max(int(p['ID do Pedido']) for p in cabecalhos)  # Busca o maior ID numérico existente
    return max_id + 1  # Retorna o maior ID somado de 1

def gerar_novo_id_item(itens):  # Define a função para auto-incremento de ID de itens
    """Gera o próximo ID sequencial para itens."""
    if not itens:  # Se não houver itens
        return 1  # Retorna 1
    max_id = max(int(i['ID do Item']) for i in itens)  # Busca o maior ID de item existente
    return max_id + 1  # Retorna o próximo número

def carregar_produtos():  # Define a função para carregar o catálogo de produtos
    """Carrega todos os produtos do arquivo CSV de produtos (BD)."""
    if not os.path.exists(ARQUIVO_PRODUTOS):  # Se o arquivo de estoque não existir
        print(f"\n❌ Erro: Arquivo de produtos '{ARQUIVO_PRODUTOS}' não encontrado.")  # Exibe erro
        return {}  # Retorna dicionário vazio
    
    produtos = {}  # Inicializa dicionário de produtos
    with open(ARQUIVO_PRODUTOS, mode='r', newline='', encoding='utf-8', errors='ignore') as f:  # Abre o estoque
        leitor = csv.DictReader(f)  # Lê o CSV
        for linha in leitor:  # Percorre cada linha do estoque
            produtos[linha['Código']] = linha  # Armazena usando o 'Código' como chave do dicionário
    return produtos  # Retorna o catálogo carregado

def selecionar_opcao(titulo, opcoes):  # Função utilitária para menus numéricos
    """Exibe um menu de opções e força o usuário a escolher uma opção válida."""
    while True:  # Loop infinito até que uma entrada válida ocorra
        print(f"\n--- {titulo} ---")  # Exibe o título do menu
        for i, op in enumerate(opcoes):  # Percorre as opções disponíveis
            print(f"{i+1}. {op}")  # Imprime o número e o nome da opção
        
        escolha = input("Selecione o número da opção: ")  # Captura a entrada do usuário
        
        try:  # Bloco de tratamento de erro
            indice = int(escolha) - 1  # Tenta converter para inteiro e subtrair 1 para o índice da lista
            if 0 <= indice < len(opcoes):  # Verifica se o número está dentro do intervalo da lista
                return opcoes[indice]  # Retorna o texto da opção escolhida
            else:  # Se o número estiver fora do intervalo
                print("⚠️ Opção inválida. Tente novamente.")  # Avisa o usuário
        except ValueError:  # Se o usuário digitar letras em vez de números
            print("⚠️ Entrada inválida. Digite apenas o número correspondente.")  # Avisa o usuário

def solicitar_data_hora_entrega():  # Função para validar agendamento
    """Solicita a data e hora para agendamento de entrega, garantindo que seja futuro."""
    while True:  # Loop de validação
        data_str = input("Digite a Data de Entrega (DD-MM-AAAA): ")  # Pede a data
        hora_str = input("Digite a Hora de Entrega (HH:MM): ")  # Pede a hora
        
        try:  # Tenta processar as strings
            data_hora = datetime.strptime(f"{data_str} {hora_str}", "%d-%m-%Y %H:%M")  # Converte para objeto datetime
            if data_hora < datetime.now() - timedelta(minutes=1):   # Compara com o horário atual (com margem de 1min)
                print("⚠️ A data e hora de entrega não podem ser no passado.")  # Bloqueia datas passadas
                continue  # Reinicia o loop
            return data_hora.strftime("%d-%m-%Y %H:%M")  # Retorna a data formatada como string
        except ValueError:  # Se o formato estiver errado
            print("⚠️ Formato de data ou hora inválido. Use DD-MM-AAAA e HH:MM.")  # Avisa o formato correto

def solicitar_data_limite_pagamento(data_pedido_str, status_pagamento):  # Função para controlar prazos de pagamento
    """Solicita a data esperada para o pagamento, validando limite de 30 dias."""
    DATA_FORMATO_PARSING = "%d-%m-%Y"  # Formato para entrada do usuário
    DATA_FORMATO_DATETIME = "%d-%m-%Y %H:%M"  # Formato para ler do sistema
    
    try:  # Tenta extrair a data do pedido
        data_base_pedido = datetime.strptime(data_pedido_str, DATA_FORMATO_DATETIME).date()  # Converte string para objeto date
    except ValueError:  # Se falhar (formato antigo ou vazio)
        data_base_pedido = datetime.now().date()  # Usa a data de hoje como base
        
    data_limite = data_base_pedido + timedelta(days=30)  # Calcula 30 dias à frente do pedido
    
    while True:  # Loop de validação de prazo
        prompt_status = "restante" if status_pagamento == 'Parcial' else ""  # Ajusta o texto conforme o status
        data_str = input(  # Pede a data ao usuário
            f"Digite a Data Esperada para o Pagamento {prompt_status} (Máx: {data_limite.strftime(DATA_FORMATO_PARSING)}, DD-MM-AAAA): "
        )
        
        try:  # Valida a entrada
            data_esperada = datetime.strptime(data_str, DATA_FORMATO_PARSING).date()  # Converte entrada
            data_atual = datetime.now().date()  # Pega data atual
            
            if data_esperada < data_atual:  # Verifica se não é passado
                print("⚠️ A data esperada deve ser hoje ou no futuro.")  # Avisa o usuário
                continue  # Reinicia
            
            if data_esperada > data_limite:  # Verifica se respeita o limite de 30 dias
                print(f"⚠️ A data de pagamento não pode ultrapassar 30 dias após o pedido ({data_limite.strftime(DATA_FORMATO_PARSING)}).")  # Avisa limite
                continue  # Reinicia
            
            return data_str  # Retorna a data validada
        except ValueError:  # Se digitar errado
            print("⚠️ Formato de data inválido. Use DD-MM-AAAA.")  # Avisa formato

def registrar_pagamento_parcial(cabecalho_alvo):  # Função para abater valores de uma dívida
    """Permite registrar um novo pagamento para um pedido parcial."""
    while True:  # Loop para entrada de valor
        try:  # Início do cálculo financeiro
            valor_total = float(cabecalho_alvo['Valor Total (R$)'])  # Pega o custo total do pedido
            valor_pago_atual = float(cabecalho_alvo.get('Valor Pago (R$)', '0.00'))   # Pega o que já foi pago
            valor_restante = valor_total - valor_pago_atual  # Calcula a dívida atual

            print(f"\nTotal do Pedido: R$ {valor_total:.2f}")  # Mostra total
            print(f"Valor já Pago: R$ {valor_pago_atual:.2f}")  # Mostra pago
            print(f"Valor Restante: R$ {valor_restante:.2f}")  # Mostra o que falta

            if valor_restante <= 0:  # Se não houver dívida
                print("\n✅ O valor restante é R$ 0,00. O status já está como 'Pago'.")  # Informa sucesso
                return  # Sai da função

            novo_pagamento = float(input("Digite o valor do novo pagamento (R$): "))  # Pede novo valor

            if novo_pagamento <= 0:  # Bloqueia valores negativos ou zero
                print("⚠️ O valor do pagamento deve ser positivo.")  # Avisa o erro
                continue  # Reinicia

            novo_valor_pago = valor_pago_atual + novo_pagamento  # Soma o novo pagamento ao anterior

            if novo_valor_pago > valor_total + 0.01:   # Verifica se não está pagando a mais que o total (margem de erro de centavos)
                print(f"⚠️ O novo valor excede o total. O máximo permitido para completar é R$ {valor_restante:.2f}.")  # Avisa excesso
                continue  # Reinicia
            
            cabecalho_alvo['Valor Pago (R$)'] = f"{novo_valor_pago:.2f}"  # Atualiza o dicionário com o novo total pago
            
            if novo_valor_pago >= valor_total:  # Se quitou a dívida
                cabecalho_alvo['Status do Pagamento'] = 'Pago'  # Muda status para pago
                cabecalho_alvo['Data do Pagamento'] = datetime.now().strftime("%d-%m-%Y %H:%M")  # Registra data da quitação
                cabecalho_alvo['Data Vencimento Prazo'] = "" # Limpa o prazo pois já foi pago
                print("\n✅ Pagamento completado! Status alterado para 'Pago'.")  # Avisa conclusão
            else:  # Se ainda falta dinheiro
                cabecalho_alvo['Status do Pagamento'] = 'Parcial'  # Mantém/Define como parcial
                cabecalho_alvo['Data do Pagamento'] = datetime.now().strftime("%d-%m-%Y %H:%M")   # Atualiza data do último pagamento
                print(f"\n✅ R$ {novo_pagamento:.2f} registrado. Novo valor pago: R$ {novo_valor_pago:.2f}")  # Mostra progresso
            
            return  # Finaliza a função com sucesso
        
        except ValueError:  # Se digitar letras no valor
            print("⚠️ Entrada inválida. Digite um valor numérico.")  # Pede números

def calcular_valor_total_pedido(id_pedido_alvo, todos_itens):  # Função para somar os itens
    """Calcula a soma total de todos os itens de um pedido específico."""
    total = 0.0  # Inicializa soma
    for item in todos_itens:  # Percorre a lista global de itens
        if item['ID do Pedido'] == str(id_pedido_alvo):  # Se o item pertencer ao pedido em questão
            total += float(item['Valor Item (R$)'])  # Acumula o valor do item no total
    return total  # Retorna o valor final somado

def adicionar_item_a_pedido(id_pedido_alvo, todos_itens, produtos_disponiveis):  # Interface de gestão de itens
    """Permite listar, adicionar, remover e EDITAR quantidade e tipo (UN/CX)."""
    while True:  # Loop do menu interno de itens
        itens_atuais = [item for item in todos_itens if item['ID do Pedido'] == str(id_pedido_alvo)]  # Filtra itens desse pedido
        
        print("\n" + "─"*60)  # Linha decorativa
        print(f"📦 ITENS NO PEDIDO #{id_pedido_alvo}")  # Título
        print("─"*60)  # Linha decorativa
        
        if not itens_atuais:  # Se a lista filtrada estiver vazia
            print("   (Pedido Vazio)")  # Avisa vacuidade
        else:  # Se houver itens
            for i, item in enumerate(itens_atuais, 1):  # Lista os itens numerados
                print(f"{i}. {item['Produto']:<30} | Qtd: {item['Quantidade']:<4} | Total: R$ {item['Valor Item (R$)']}")  # Formata linha
        
        print("-" * 60)  # Linha decorativa
        print("A. Adicionar Novo Produto")  # Opção A
        print("E. EDITAR Item (Alterar Qtd ou Tipo UN/CX)")  # Opção E
        print("R. Remover Item (Excluir)")  # Opção R
        print("F. Finalizar e Recalcular Total")  # Opção F
        print("-" * 60)  # Linha decorativa
        
        acao = input("Escolha uma ação: ").upper()  # Captura ação em maiúsculo

        if acao == 'F':  # Se escolher finalizar
            break  # Sai do loop de itens
        
        elif acao == 'E':  # Se escolher editar
            if not itens_atuais:  # Verifica se tem o que editar
                print("❌ Não há itens para editar.")  # Avisa erro
                continue  # Reinicia
            try:  # Tenta editar
                idx = int(input("Digite o número da linha para EDITAR: ")) - 1  # Pede o índice da lista
                if 0 <= idx < len(itens_atuais):  # Valida o índice
                    item_editando = itens_atuais[idx]  # Seleciona o item para edição
                    
                    nome_limpo = item_editando['Produto'].replace(" (UN)", "").replace(" (CX)", "").strip()  # Remove sufixos para achar o nome base
                    
                    prod_info = next((info for info in produtos_disponiveis.values() if info['Nome do Produto'] == nome_limpo), None)  # Busca dados originais no estoque
                    
                    if not prod_info:  # Se o produto sumiu do estoque
                        print("❌ Produto base não encontrado no estoque para recalcular.")  # Avisa erro
                        continue  # Reinicia

                    print(f"\nEditando: {nome_limpo}")  # Mostra o que está editando
                    print("1. Mudar para UNIDADE (R$ " + prod_info['Valor Unidade (R$)'] + ")")  # Opção UN
                    print("2. Mudar para CAIXA (R$ " + prod_info['Valor Caixa (R$)'] + ")")  # Opção CX
                    tipo_venda = input("Escolha o novo tipo: ")  # Pede o tipo
                    
                    nova_qtd = int(input(f"Nova quantidade: "))  # Pede nova quantidade
                    
                    if nova_qtd <= 0:  # Bloqueia zero ou negativos
                        print("❌ Quantidade inválida.")  # Avisa erro
                        continue  # Reinicia

                    if tipo_venda == '1':  # Se for unidade
                        preco = float(prod_info['Valor Unidade (R$)'])  # Pega preço unitário
                        novo_nome = f"{nome_limpo} (UN)"  # Define novo nome com sufixo
                    else:  # Se for caixa
                        preco = float(prod_info['Valor Caixa (R$)'])  # Pega preço da caixa
                        novo_nome = f"{nome_limpo} (CX)"  # Define novo nome com sufixo

                    item_editando['Produto'] = novo_nome  # Atualiza o nome do produto no item
                    item_editando['Quantidade'] = str(nova_qtd)  # Atualiza a quantidade
                    item_editando['Valor Item (R$)'] = f"{(nova_qtd * preco):.2f}"  # Recalcula o subtotal do item
                    
                    print(f"✅ Item atualizado: {novo_nome} x {nova_qtd}!")  # Confirma edição
                else:  # Se o número da linha for inválido
                    print("❌ Linha inválida.")  # Avisa erro
            except ValueError:  # Erro de digitação
                print("❌ Erro: Entrada inválida.")  # Avisa erro

        elif acao == 'A':  # Se escolher adicionar novo produto
            print("\nPRODUTOS DISPONÍVEIS:")  # Título do catálogo
            for cod, info in produtos_disponiveis.items():  # Percorre estoque
                print(f"{cod:<5} | {info['Nome do Produto']:<30} | UN: {info['Valor Unidade (R$)']:<8} | CX: {info['Valor Caixa (R$)']}")  # Lista catálogo
            
            codigo = input("\nCódigo: ").strip().zfill(2)  # Pede código (completa com zero se necessário)
            if codigo in produtos_disponiveis:  # Verifica se o código existe
                p = produtos_disponiveis[codigo]  # Pega dados do produto
                t = input("1. Unidade | 2. Caixa: ")  # Pede tipo
                q = int(input("Quantidade: "))  # Pede quantidade
                pr = float(p['Valor Unidade (R$)']) if t == '1' else float(p['Valor Caixa (R$)'])  # Define preço baseado no tipo
                nm = f"{p['Nome do Produto']} ({'UN' if t == '1' else 'CX'})"  # Define nome com sufixo
                todos_itens.append({  # Adiciona novo dicionário à lista global de itens
                    'ID do Pedido': str(id_pedido_alvo), 
                    'ID do Item': str(gerar_novo_id_item(todos_itens)), # Gera ID único para o item
                    'Produto': nm, 
                    'Quantidade': str(q), 
                    'Valor Item (R$)': f"{(q*pr):.2f}"
                })
            else:  # Código inexistente
                print("❌ Código inválido.")  # Avisa erro

        elif acao == 'R':  # Se escolher remover
            try:  # Tenta remover
                idx = int(input("Linha para remover: ")) - 1  # Pede linha
                todos_itens.remove(itens_atuais[idx])  # Remove o item da lista global
                print("🗑️ Item removido.")  # Confirma
            except:  # Qualquer erro na remoção
                print("❌ Erro ao remover.")  # Avisa falha

def visualizar_detalhes_cliente(pedidos_cliente, todos_itens):  # Função para ver o "espelho" do pedido
    """Permite escolher um pedido da lista do cliente para ver detalhes e itens."""
    id_escolhido = input("\nDigite o ID do pedido que deseja ver detalhes: ").strip()  # Pede o ID
    
    pedido = next((p for p in pedidos_cliente if p['ID do Pedido'] == id_escolhido), None)  # Busca o pedido na lista do cliente
    
    if pedido:  # Se o pedido foi encontrado
        print("\n" + "═"*50)  # Decorativo
        print(f"      DETALHES DO PEDIDO #{id_escolhido}")  # Título
        print("═"*50)  # Decorativo
        for chave, valor in pedido.items():  # Percorre todos os campos do cabeçalho do pedido
            print(f"{chave:<22}: {valor}")  # Imprime campo e valor
        
        print("-" * 50)  # Divisor
        print("ITENS DO PEDIDO:")  # Título da sublista
        itens_pedido = [item for item in todos_itens if item['ID do Pedido'] == id_escolhido]  # Filtra itens desse pedido
        
        if itens_pedido:  # Se houver itens
            for item in itens_pedido:  # Percorre itens
                print(f"• {item['Produto']} | Qtd: {item['Quantidade']} | Subtotal: R$ {item['Valor Item (R$)']}")  # Lista item
        else:  # Pedido fantasma sem itens
            print("Nenhum item encontrado para este pedido.")  # Avisa erro
        print("═"*50)  # Decorativo
        input("\nPressione Enter para voltar ao painel...")  # Pausa a tela
    else:  # ID digitado não pertence a este cliente ou não existe
        print("\n❌ ID não encontrado na lista deste cliente.")  # Avisa erro

def adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=None):  # Função de criação de venda
    """Lança um novo pedido, permitindo nome automático ou manual."""
    produtos_disponiveis = carregar_produtos()  # Carrega o estoque atualizado
    if not produtos_disponiveis:  # Se não houver estoque disponível
        return  # Aborta a criação do pedido

    novo_id = gerar_novo_id_pedido(cabecalhos)  # Gera o ID para a nova venda
    data_pedido = datetime.now().strftime("%d-%m-%Y %H:%M")  # Define a data da venda agora
    
    if nome_sugerido:  # Se a função recebeu um nome pronto (da gestão de clientes)
        nome_cliente = nome_sugerido  # Usa o nome sugerido
        print(f"\nLançando pedido para: {nome_cliente.upper()}")  # Informa o usuário
    else:  # Se for uma venda avulsa
        nome_cliente = input("\nNome do Cliente: ")  # Pede o nome

    try:  # Tenta realizar o processo de venda
        adicionar_item_a_pedido(novo_id, todos_itens, produtos_disponiveis)  # Abre a interface de inclusão de itens
        
        valor_total = calcular_valor_total_pedido(novo_id, todos_itens)  # Soma tudo que foi incluído
        if valor_total == 0.0:  # Se o usuário não adicionou nada e saiu
            print("\n❌ Pedido sem itens. Cancelando operação.")  # Cancela o registro
            return  # Aborta

        print(f"\n--- Finalizando Pedido ID {novo_id} ---")  # Início do fechamento financeiro
        print(f"VALOR TOTAL: R$ {valor_total:.2f}")  # Mostra o valor total calculado

        forma_pagamento = selecionar_opcao("Forma de Pagamento", OPCOES_FORMA_PAGAMENTO)  # Escolhe forma
        status_pagamento = selecionar_opcao("Status do Pagamento", OPCOES_STATUS_PAGAMENTO)  # Escolhe status financeiro
        status_pedido = selecionar_opcao("Status do Pedido", OPCOES_STATUS_PEDIDO)  # Escolhe status logístico
        
        data_hora_entrega = ""  # Inicializa vazio
        data_vencimento_prazo = ""  # Inicializa vazio
        valor_pago = "0.00"  # Inicializa valor padrão
        data_pagamento = ""  # Inicializa vazio
        
        if status_pedido == 'Pendente':  # Se o pedido for para depois
            data_hora_entrega = solicitar_data_hora_entrega()   # Pede agendamento

        if status_pagamento == 'Pago':  # Se já pagou tudo
            valor_pago = f"{valor_total:.2f}"  # Valor pago é igual ao total
            data_pagamento = datetime.now().strftime("%d-%m-%Y %H:%M")  # Data do pagamento é agora
            
        elif status_pagamento == 'Parcial':  # Se deu uma entrada
            print("\n--- REGISTRO INICIAL DE PAGAMENTO PARCIAL ---")  # Título
            temp_cabecalho = {'Valor Total (R$)': f"{valor_total:.2f}", 'Valor Pago (R$)': '0.00'}  # Cria objeto temporário
            registrar_pagamento_parcial(temp_cabecalho)  # Chama função de abatimento
            
            valor_pago = temp_cabecalho['Valor Pago (R$)']  # Extrai o valor pago final do temporário
            data_pagamento = temp_cabecalho.get('Data do Pagamento', "")  # Pega data do registro
            status_pagamento = temp_cabecalho['Status do Pagamento']  # Pega status (pode ter virado 'Pago')

            if status_pagamento == 'Parcial':  # Se após o pagamento ainda faltar dinheiro
                print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO RESTANTE ---")  # Título
                data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)  # Pede prazo de 30 dias

        elif status_pagamento == 'Pendente':  # Se não pagou nada (venda fiado/prazo)
            valor_pago = "0.00"  # Zerado
            print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO TOTAL ---")  # Título
            data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)  # Pede prazo
        
        novo_cabecalho = {  # Monta o dicionário final do pedido para o CSV
            'ID do Pedido': str(novo_id),
            'Data do Pedido': data_pedido,
            'Nome do Cliente': nome_cliente,
            'Valor Total (R$)': f"{valor_total:.2f}",
            'Valor Pago (R$)': valor_pago,
            'Forma de Pagamento': forma_pagamento,
            'Status do Pagamento': status_pagamento,
            'Data do Pagamento': data_pagamento,
            'Data Vencimento Prazo': data_vencimento_prazo,
            'Status do Pedido': status_pedido,
            'Data/Hora Entrega': data_hora_entrega
        }
        
        cabecalhos.append(novo_cabecalho)  # Adiciona à lista em memória
        salvar_cabecalhos(cabecalhos)  # Salva tudo no arquivo de cabeçalhos
        salvar_itens(todos_itens)  # Salva todos os itens (incluindo os novos)
        print("\n✅ Pedido registrado com sucesso!")  # Feedback
        
    except Exception as e:  # Captura qualquer erro inesperado
        print(f"\n❌ Ocorreu um erro inesperado: {e}")  # Exibe erro para depuração

def editar_pedido(cabecalhos, todos_itens):  # Função de manutenção de pedidos existentes
    """Edita um pedido existente com recálculo automático de valores."""
    id_pedido = input("\nDigite o ID do pedido que deseja editar: ").strip()  # Pede o ID
    
    pedido = next((p for p in cabecalhos if p['ID do Pedido'] == id_pedido), None)  # Tenta localizar o pedido
    
    if not pedido:  # Se não achar
        print(f"❌ Pedido ID {id_pedido} não encontrado.")  # Avisa erro
        return  # Sai
    alterou_itens = False  # Flag para saber se precisaremos recalcular o total no fim
    while True:  # Menu de edição
        print(f"\n" + "═"*50)  # Decorativo
        print(f"      EDITANDO PEDIDO #{id_pedido} - {pedido['Nome do Cliente']}")  # Cabeçalho da edição
        print("═"*50)  # Decorativo
        print("1. Adicionar/Remover/Alterar Itens (Produtos)")  # Opção 1
        print("2. Registrar Pagamento (Dar Baixa)")  # Opção 2
        print("3. Alterar Status do Pedido (Entrega/Retirada)")  # Opção 3
        print("4. SALVAR E SAIR")  # Opção 4
        print("5. Cancelar Edição")  # Opção 5
        
        opcao = input("\nEscolha uma opção: ")  # Pede opção

        if opcao == '1':  # Editar produtos
            adicionar_item_a_pedido(id_pedido, todos_itens, carregar_produtos())  # Abre interface de itens
            alterou_itens = True  # Marca que o total financeiro pode ter mudado
            print("📝 Alteração de itens registrada.")  # Feedback

        elif opcao == '2':  # Dar baixa no pagamento
            registrar_pagamento_parcial(pedido)  # Abre interface financeira

        elif opcao == '3':  # Mudar status logístico
            novo_status = selecionar_opcao("Status do Pedido", OPCOES_STATUS_PEDIDO)  # Escolhe novo status
            pedido['Status do Pedido'] = novo_status  # Atualiza no dicionário
            if novo_status == 'Entregue' and not pedido['Data/Hora Entrega']:  # Se foi entregue agora
                pedido['Data/Hora Entrega'] = datetime.now().strftime("%d-%m-%Y %H:%M")  # Registra data da entrega

        elif opcao == '4':  # Finalizar edições e salvar
            if alterou_itens:  # Se mexeu nos produtos
                print("\n🔄 Recalculando valor total com base nos itens atualizados...")  # Título
                novo_total = calcular_valor_total_pedido(id_pedido, todos_itens)  # Soma itens novamente
                
                pedido['Valor Total (R$)'] = f"{novo_total:.2f}"  # Atualiza o custo total do pedido
                
                valor_pago = float(pedido.get('Valor Pago (R$)', 0))  # Pega quanto o cliente já pagou
                if valor_pago < novo_total:  # Se o que foi pago não cobre o novo total
                    if pedido['Status do Pagamento'] == 'Pago':  # E o status era 'Pago'
                        pedido['Status do Pagamento'] = 'Parcial'  # Rebaixa para parcial (deve dinheiro)
                        print("⚠️ Alerta: O valor total aumentou. Status alterado para 'Parcial'.")  # Avisa
                elif valor_pago >= novo_total and novo_total > 0:  # Se o novo total é menor ou igual ao que já foi pago
                    pedido['Status do Pagamento'] = 'Pago'  # Garante status de quitado

            salvar_cabecalhos(cabecalhos)  # Grava no disco
            salvar_itens(todos_itens)  # Grava no disco
            print("\n✅ Alterações salvas com sucesso!")  # Feedback
            break  # Sai do menu de edição

        elif opcao == '5':  # Desistir das mudanças (Nota: mudanças em itens são gravadas apenas no final nesta lógica)
            print("\nEdição descartada.")  # Feedback
            break  # Sai do menu
            
        else:  # Opção inválida
            print("\n⚠️ Opção inválida. Tente novamente.")  # Avisa erro

def gerenciar_por_cliente(cabecalhos, todos_itens):  # Função principal de atendimento por pessoa
    """Filtra pedidos por nome ou automatiza cadastro de novo cliente."""
    nome_busca = input("\nDigite o nome do cliente para gerenciar: ").strip()  # Pede nome para buscar
    
    if not nome_busca:  # Se enter vazio
        print("⚠️ Nome não pode ser vazio.")  # Avisa erro
        return  # Sai

    pedidos_cliente = [p for p in cabecalhos if nome_busca.lower() in p['Nome do Cliente'].lower()]  # Filtra pedidos que contenham o texto digitado
    
    if not pedidos_cliente:  # Se não achou ninguém com esse nome
        print(f"\n🟡 Cliente '{nome_busca}' não encontrado.")  # Avisa
        confirmar = input(f"Deseja cadastrar e lançar pedido para '{nome_busca}' agora? (S/N): ").upper()  # Sugere cadastro novo
        if confirmar == 'S':  # Se aceitar
            adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=nome_busca)  # Abre venda com esse nome
            return  # Sai para atualizar dados
        else:  # Se recusar
            return  # Sai

    nome_exato = pedidos_cliente[0]['Nome do Cliente']  # Pega o nome como está no cadastro para o título
    
    while True:  # Painel do cliente
        total_devedor_acumulado = 0.0  # Soma das dívidas
        print(f"\n" + "═"*75)  # Decorativo
        print(f"    PAINEL DE GESTÃO: {nome_exato.upper()}")  # Título com nome do cliente
        print("═"*75)  # Decorativo
        
        print(f"{'ID':<5} | {'DATA PEDIDO':<18} | {'TOTAL':<10} | {'SALDO':<10} | {'STATUS'}")  # Cabeçalho da tabela
        print("-" * 75)  # Divisor
        
        for p in pedidos_cliente:  # Lista cada pedido do cliente
            v_total = float(p['Valor Total (R$)'])  # Pega total
            v_pago = float(p.get('Valor Pago (R$)', '0.00'))  # Pega pago
            saldo = v_total - v_pago  # Calcula quanto falta pagar
            total_devedor_acumulado += saldo  # Soma ao total devedor do cliente
            print(f"{p['ID do Pedido']:<5} | {p['Data do Pedido']:<18} | {v_total:<10.2f} | {saldo:<10.2f} | {p['Status do Pagamento']}")  # Linha formatada
        
        print("\n💰 HISTÓRICO DE LANÇAMENTOS (PAGAMENTOS):")  # Seção de extrato
        tem_pagamento = False  # Flag para verificar se houve algum pagamento
        for p in pedidos_cliente:  # Busca nos pedidos
            if p.get('Data do Pagamento') and float(p.get('Valor Pago (R$)', 0)) > 0:  # Se houver data e valor pago
                print(f"   • {p['Data do Pagamento']} --> Recebido R$ {p['Valor Pago (R$)']} (Pedido #{p['ID do Pedido']})")  # Mostra recebimento
                tem_pagamento = True  # Marca que houve registro
        
        if not tem_pagamento:  # Se não houve nenhum pagamento
            print("   (Nenhum pagamento registrado)")  # Avisa histórico limpo

        print("-" * 75)  # Divisor
        print(f"💸 TOTAL A RECEBER DESTE CLIENTE: R$ {total_devedor_acumulado:.2f}")  # Mostra dívida total do cliente
        print("-" * 75)  # Divisor
        
        print("1. Lançar Novo Pedido")  # Opção 1
        print("2. EDITAR PEDIDO (Pagamentos, Itens, Excluir)")  # Opção 2
        print("3. VER DETALHES DE UM PEDIDO (Ver Itens)")  # Opção 3
        print("4. Voltar ao Menu Principal")  # Opção 4
        
        op = input("\nEscolha uma opção: ")  # Pede opção

        if op == '1':  # Vender mais para este cliente
            adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=nome_exato)  # Abre venda
            cabecalhos = carregar_cabecalhos()  # Recarrega dados do disco
            pedidos_cliente = [p for p in cabecalhos if nome_exato.lower() in p['Nome do Cliente'].lower()]  # Re-filtra para atualizar painel
        elif op == '2':  # Editar algum pedido da lista
            editar_pedido(cabecalhos, todos_itens)  # Abre edição por ID
            cabecalhos = carregar_cabecalhos()  # Recarrega dados
            pedidos_cliente = [p for p in cabecalhos if nome_exato.lower() in p['Nome do Cliente'].lower()]  # Re-filtra
        elif op == '3':  # Ver espelho do pedido
            visualizar_detalhes_cliente(pedidos_cliente, todos_itens)  # Abre detalhes
        elif op == '4':  # Sair do painel do cliente
            break  # Sai do loop

def visualizar_pedidos(cabecalhos):  # Função de visão geral
    """Imprime todos os cabeçalhos de pedidos em formato de tabela."""
    if not cabecalhos:  # Se não houver nenhum pedido no sistema
        print("\nNenhum pedido encontrado.")  # Avisa
        return  # Sai

    print("\n--- Todos os Pedidos (Visão Geral) ---")  # Título
    
    larguras = {campo: len(campo) for campo in CAMPOS_CABECALHO}  # Calcula a largura mínima baseada no nome das colunas
    for pedido in cabecalhos:  # Percorre todos os pedidos
        for campo in CAMPOS_CABECALHO:  # Percorre cada campo
            larguras[campo] = max(larguras[campo], len(pedido.get(campo, '')))  # Ajusta a largura da coluna para o maior dado encontrado

    linha_cabecalho = " | ".join(campo.ljust(larguras[campo]) for campo in CAMPOS_CABECALHO)  # Monta a linha de títulos
    print(linha_cabecalho)  # Imprime títulos
    print("-" * len(linha_cabecalho))  # Imprime sublinhado

    for pedido in cabecalhos:  # Percorre pedidos para imprimir dados
        linha_dados = " | ".join(pedido.get(campo, '').ljust(larguras[campo]) for campo in CAMPOS_CABECALHO)  # Monta linha de dados alinhada
        print(linha_dados)  # Imprime dados do pedido
        
def menu_principal():  # Função de entrada do sistema
    inicializar_csv()  # Garante que os arquivos existam ao iniciar

    while True:  # Loop do sistema principal
        cabecalhos = carregar_cabecalhos()  # Carrega pedidos atualizados
        todos_itens = carregar_itens()  # Carrega itens atualizados

        print("\n" + "="*40)  # Decorativo
        print("      SISTEMA DE GESTÃO v2.0")  # Título do sistema
        print("="*40)  # Decorativo
        print("1. GESTÃO DE CLIENTES (Venda/Edição/Detalhes)")  # Botão 1
        print("2. Visualizar Todos os Pedidos (Geral)")  # Botão 2
        print("3. Sair")  # Botão 3
        print("-" * 40)  # Decorativo

        escolha = input("Escolha uma opção: ")  # Pede escolha

        if escolha == '1':  # Entrar no fluxo de clientes
            gerenciar_por_cliente(cabecalhos, todos_itens)  # Chama função
        elif escolha == '2':  # Ver relatório geral
            visualizar_pedidos(cabecalhos)  # Chama função
        elif escolha == '3':  # Sair do programa
            print("\nEncerrando sistema. Até logo!")  # Despedida
            break  # Quebra o loop principal e encerra
        else:  # Erro de menu
            print("\n⚠️ Opção inválida.")  # Avisa erro

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    menu_principal()  # Inicia o programa pela função principal