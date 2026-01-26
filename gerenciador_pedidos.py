import csv
import os
from datetime import datetime, timedelta

# --- Configurações de Arquivos ---
ARQUIVO_CABECALHO = 'pedidos_cabecalho.csv'
ARQUIVO_ITENS = 'pedidos_itens.csv'
ARQUIVO_PRODUTOS = 'produtos.csv' 

# Cabeçalhos dos arquivos 
CAMPOS_CABECALHO = [
    'ID do Pedido', 'Data do Pedido', 'Nome do Cliente', 
    'Valor Total (R$)', 'Valor Pago (R$)', 'Forma de Pagamento', 
    'Status do Pagamento', 'Data do Pagamento', 'Data Vencimento Prazo', 
    'Status do Pedido', 'Data/Hora Entrega'
]

CAMPOS_ITENS = [
    'ID do Item', 'ID do Pedido', 'Produto', 
    'Quantidade', 'Valor Item (R$)'
]

# --- Constantes para os Menus ---
OPCOES_STATUS_PAGAMENTO = ['Pago', 'Pendente', 'Parcial']
OPCOES_STATUS_PEDIDO = ['Entregue', 'Pendente']
OPCOES_FORMA_PAGAMENTO = ['Pix', 'Dinheiro', 'Prazo']

# =================================================================
#               FUNÇÕES DE INICIALIZAÇÃO E UTILIDADE 
# =================================================================

def inicializar_csv():
    """Cria ou verifica os arquivos CSV com cabeçalhos."""
    if not os.path.exists(ARQUIVO_CABECALHO):
        with open(ARQUIVO_CABECALHO, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_CABECALHO)
            escritor.writeheader()
    
    if not os.path.exists(ARQUIVO_ITENS):
        with open(ARQUIVO_ITENS, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_ITENS)
            escritor.writeheader()
    
def carregar_cabecalhos():
    """Carrega todos os cabeçalhos de pedidos."""
    if not os.path.exists(ARQUIVO_CABECALHO):
        return []
   # CÓDIGO CORRIGIDO
    with open(ARQUIVO_CABECALHO, mode='r', newline='', encoding='utf-8', errors='ignore') as f:
        leitor = csv.DictReader(f)
        return list(leitor)

def carregar_itens():
    """Carrega todos os itens de pedidos."""
    if not os.path.exists(ARQUIVO_ITENS):
        return []
    # CÓDIGO CORRIGIDO
    with open(ARQUIVO_ITENS, mode='r', newline='', encoding='utf-8', errors='ignore') as f:
        leitor = csv.DictReader(f)
        return list(leitor)

def salvar_cabecalhos(cabecalhos):
    """Salva a lista atualizada de cabeçalhos de pedidos."""
    with open(ARQUIVO_CABECALHO, mode='w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS_CABECALHO)
        escritor.writeheader()
        escritor.writerows(cabecalhos)

def salvar_itens(itens):
    """Salva a lista atualizada de itens de pedidos."""
    with open(ARQUIVO_ITENS, mode='w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS_ITENS)
        escritor.writeheader()
        escritor.writerows(itens)

def gerar_novo_id_pedido(cabecalhos):
    """Gera o próximo ID sequencial para pedidos."""
    if not cabecalhos:
        return 1
    max_id = max(int(p['ID do Pedido']) for p in cabecalhos)
    return max_id + 1

def gerar_novo_id_item(itens):
    """Gera o próximo ID sequencial para itens."""
    if not itens:
        return 1
    max_id = max(int(i['ID do Item']) for i in itens)
    return max_id + 1

def carregar_produtos():
    """Carrega todos os produtos do arquivo CSV de produtos (BD)."""
    if not os.path.exists(ARQUIVO_PRODUTOS):
        print(f"\n❌ Erro: Arquivo de produtos '{ARQUIVO_PRODUTOS}' não encontrado.")
        return {}
    
    produtos = {}
    # CÓDIGO CORRIGIDO (linha 95)
    # Adicionamos errors='ignore' para pular caracteres que o 'utf-8' não consegue decodificar
    with open(ARQUIVO_PRODUTOS, mode='r', newline='', encoding='utf-8', errors='ignore') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            produtos[linha['Código']] = linha
    return produtos

def selecionar_opcao(titulo, opcoes):
    """Exibe um menu de opções e força o usuário a escolher uma opção válida."""
    while True:
        print(f"\n--- {titulo} ---")
        for i, op in enumerate(opcoes):
            print(f"{i+1}. {op}")
        
        escolha = input("Selecione o número da opção: ")
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(opcoes):
                return opcoes[indice]
            else:
                print("⚠️ Opção inválida. Tente novamente.")
        except ValueError:
            print("⚠️ Entrada inválida. Digite apenas o número correspondente.")

def solicitar_data_hora_entrega():
    """Solicita a data e hora para agendamento de entrega, garantindo que seja futuro."""
    while True:
        data_str = input("Digite a Data de Entrega (DD-MM-AAAA): ")
        hora_str = input("Digite a Hora de Entrega (HH:MM): ")
        
        try:
            data_hora = datetime.strptime(f"{data_str} {hora_str}", "%d-%m-%Y %H:%M")
            if data_hora < datetime.now() - timedelta(minutes=1): 
                print("⚠️ A data e hora de entrega não podem ser no passado.")
                continue
            return data_hora.strftime("%d-%m-%Y %H:%M")
        except ValueError:
            print("⚠️ Formato de data ou hora inválido. Use DD-MM-AAAA e HH:MM.")

# 🎯 NOVA FUNÇÃO: Solicita a data de pagamento com limite de 30 dias do pedido
def solicitar_data_limite_pagamento(data_pedido_str, status_pagamento):
    """
    Solicita a data esperada para o pagamento (total ou restante), 
    validando que não ultrapasse 30 dias a partir da data do pedido.
    """
    DATA_FORMATO_PARSING = "%d-%m-%Y"
    DATA_FORMATO_DATETIME = "%d-%m-%Y %H:%M"
    
    # 1. Obter a data base do pedido para calcular o limite
    try:
        data_base_pedido = datetime.strptime(data_pedido_str, DATA_FORMATO_DATETIME).date()
    except ValueError:
        # Fallback para o caso de Data do Pedido estar vazia ou em formato antigo/diferente
        data_base_pedido = datetime.now().date()
        
    data_limite = data_base_pedido + timedelta(days=30)
    
    while True:
        prompt_status = "restante" if status_pagamento == 'Parcial' else ""
        data_str = input(
            f"Digite a Data Esperada para o Pagamento {prompt_status} (Máx: {data_limite.strftime(DATA_FORMATO_PARSING)}, DD-MM-AAAA): "
        )
        
        try:
            data_esperada = datetime.strptime(data_str, DATA_FORMATO_PARSING).date()
            data_atual = datetime.now().date()
            
            # 2. Validações
            if data_esperada < data_atual:
                print("⚠️ A data esperada deve ser hoje ou no futuro.")
                continue
            
            if data_esperada > data_limite:
                print(f"⚠️ A data de pagamento não pode ultrapassar 30 dias após o pedido ({data_limite.strftime(DATA_FORMATO_PARSING)}).")
                continue
            
            return data_str
        except ValueError:
            print("⚠️ Formato de data inválido. Use DD-MM-AAAA.")


def registrar_pagamento_parcial(cabecalho_alvo):
    """Permite registrar um novo pagamento para um pedido parcial."""
    while True:
        try:
            valor_total = float(cabecalho_alvo['Valor Total (R$)'])
            valor_pago_atual = float(cabecalho_alvo.get('Valor Pago (R$)', '0.00')) 
            valor_restante = valor_total - valor_pago_atual

            print(f"\nTotal do Pedido: R$ {valor_total:.2f}")
            print(f"Valor já Pago: R$ {valor_pago_atual:.2f}")
            print(f"Valor Restante: R$ {valor_restante:.2f}")

            if valor_restante <= 0:
                print("\n✅ O valor restante é R$ 0,00. O status já está como 'Pago'.")
                return

            novo_pagamento = float(input("Digite o valor do novo pagamento (R$): "))

            if novo_pagamento <= 0:
                print("⚠️ O valor do pagamento deve ser positivo.")
                continue

            novo_valor_pago = valor_pago_atual + novo_pagamento

            if novo_valor_pago > valor_total + 0.01: 
                print(f"⚠️ O novo valor excede o total. O máximo permitido para completar é R$ {valor_restante:.2f}.")
                continue
            
            cabecalho_alvo['Valor Pago (R$)'] = f"{novo_valor_pago:.2f}"
            
            if novo_valor_pago >= valor_total:
                cabecalho_alvo['Status do Pagamento'] = 'Pago'
                cabecalho_alvo['Data do Pagamento'] = datetime.now().strftime("%d-%m-%Y %H:%M")
                cabecalho_alvo['Data Vencimento Prazo'] = "" # Limpa o prazo ao completar
                print("\n✅ Pagamento completado! Status alterado para 'Pago'.")
            else:
                cabecalho_alvo['Status do Pagamento'] = 'Parcial'
                cabecalho_alvo['Data do Pagamento'] = datetime.now().strftime("%d-%m-%Y %H:%M") 
                # A data de vencimento será solicitada na função 'editar_pedido' ou 'adicionar_pedido'
                print(f"\n✅ R$ {novo_pagamento:.2f} registrado. Novo valor pago: R$ {novo_valor_pago:.2f}")
            
            return
        
        except ValueError:
            print("⚠️ Entrada inválida. Digite um valor numérico.")

def calcular_valor_total_pedido(id_pedido_alvo, todos_itens):
    """Calcula a soma total de todos os itens de um pedido específico."""
    total = 0.0
    for item in todos_itens:
        if item['ID do Pedido'] == str(id_pedido_alvo):
            total += float(item['Valor Item (R$)'])
    return total

def adicionar_item_a_pedido(id_pedido_alvo, todos_itens, produtos_disponiveis):
    """Adiciona um novo item ao pedido especificado."""
    while True:
        print("\n--- Adicionar Item ---")
        
        for codigo, produto in produtos_disponiveis.items():
            print(
                f"  [{codigo}] {produto['Nome do Produto']} | UN: R${float(produto['Valor Unidade (R$)']):.2f} "
                f"| CX ({produto['Qtd por Caixa']} un): R${float(produto['Valor Caixa (R$)']):.2f}"
            )

        codigo_produto = input("Digite o Código do Produto (Ex: P001, ou N para CANCELAR): ").upper()
        if codigo_produto == 'N':
            return

        produto_selecionado = produtos_disponiveis.get(codigo_produto)
        
        if not produto_selecionado:
            print(f"\n❌ Código de produto '{codigo_produto}' inválido. Tente novamente.")
            continue

        tipo_compra = input("Tipo de Compra (U para Unidade, C para Caixa): ").upper()
        if tipo_compra not in ['U', 'C']:
            print("\n❌ Tipo de compra inválida. Use 'U' ou 'C'. Tente novamente.")
            continue
            
        try:
            quantidade_compra = int(input(f"Quantidade de {'Unidades' if tipo_compra == 'U' else 'Caixas'} a comprar: "))
        except ValueError:
            print("\n❌ Quantidade inválida. Digite um número inteiro.")
            continue
            
        if tipo_compra == 'U':
            valor_unitario = float(produto_selecionado['Valor Unidade (R$)'])
            valor_do_item = quantidade_compra * valor_unitario
        else:
            valor_caixa = float(produto_selecionado['Valor Caixa (R$)'])
            valor_do_item = quantidade_compra * valor_caixa

        novo_item = {
            'ID do Item': str(gerar_novo_id_item(todos_itens)),
            'ID do Pedido': str(id_pedido_alvo),
            'Produto': produto_selecionado['Nome do Produto'],
            'Quantidade': str(quantidade_compra), 
            'Valor Item (R$)': f"{valor_do_item:.2f}"
        }
        
        todos_itens.append(novo_item)
        print(f"✅ Item '{produto_selecionado['Nome do Produto']}' adicionado com sucesso.")
        
        adicionar_mais = input("Adicionar outro item? (S/N): ").upper()
        if adicionar_mais != 'S':
            break

def remover_item_de_pedido(id_pedido_alvo, todos_itens):
    """Remove um item específico do pedido."""
    itens_do_pedido = [item for item in todos_itens if item['ID do Pedido'] == str(id_pedido_alvo)]

    if not itens_do_pedido:
        print("\n❌ Este pedido não possui itens registrados.")
        return

    print("\n--- Itens Atuais do Pedido ---")
    for i, item in enumerate(itens_do_pedido):
        print(f"[{i+1}] {item['Produto']} - Qtd: {item['Quantidade']} - Total: R$ {item['Valor Item (R$)']}")

    try:
        escolha_remocao = input("Digite o número do item para remover (ou 0 para CANCELAR): ")
        indice_remover = int(escolha_remocao) - 1
        
        if indice_remover < 0:
            return

        item_para_remover = itens_do_pedido[indice_remover]
        
        todos_itens[:] = [item for item in todos_itens if item['ID do Item'] != item_para_remover['ID do Item']]

        print(f"\n✅ Item '{item_para_remover['Produto']}' removido com sucesso.")

    except (ValueError, IndexError):
        print("\n❌ Opção inválida.")
        
def menu_edicao_itens(id_alvo, todos_itens, produtos_disponiveis):
    """Permite selecionar um item de um pedido para editar (Qtd/Valor) ou excluir."""
    
    while True:
        itens_do_pedido = [item for item in todos_itens if item['ID do Pedido'] == str(id_alvo)]

        print("\n--- ITENS ATUAIS DO PEDIDO ---")
        if not itens_do_pedido:
            print("Nenhum item registrado neste pedido.")
        
        opcoes_itens = []
        for i, item in enumerate(itens_do_pedido):
            opcoes_itens.append(f"[{item['Produto']}] Qtd: {item['Quantidade']} | Total: R$ {item['Valor Item (R$)']}")

        print("\nEscolha uma opção:")
        for i, op in enumerate(opcoes_itens):
            print(f"{i+1}. {op} (Editar/Excluir)")
        print(f"{len(opcoes_itens) + 1}. Adicionar Novo Item")
        print(f"{len(opcoes_itens) + 2}. VOLTAR ao Menu Principal de Edição")
        print("-" * 40)
        
        escolha = input("Selecione o número da opção: ")

        try:
            escolha_num = int(escolha)
        except ValueError:
            print("⚠️ Entrada inválida. Digite o número correspondente à opção.")
            continue

        if escolha_num == len(opcoes_itens) + 2:
            return 

        elif escolha_num == len(opcoes_itens) + 1:
            adicionar_item_a_pedido(id_alvo, todos_itens, produtos_disponiveis)
            
        elif 1 <= escolha_num <= len(opcoes_itens):
            item_alvo = itens_do_pedido[escolha_num - 1]
            
            print(f"\nDetalhes do Item: {item_alvo['Produto']}")
            print("1. Alterar Quantidade/Valor")
            print("2. EXCLUIR Item")
            acao = input("Escolha a ação (1 ou 2, ou qualquer outra tecla para CANCELAR): ")

            if acao == '1':
                print(f"Produto: {item_alvo['Produto']} | Valor Atual: R$ {item_alvo['Valor Item (R$)']}")
                
                tipo_compra = input("Tipo de Compra (U para Unidade, C para Caixa): ").upper()
                if tipo_compra not in ['U', 'C']:
                    print("\n❌ Tipo de compra inválido.")
                    continue
                    
                try:
                    nova_quantidade = int(input(f"Nova Quantidade de {'Unidades' if tipo_compra == 'U' else 'Caixas'} (Atual: {item_alvo['Quantidade']}): "))
                    novo_valor_item = float(input("Digite o NOVO Valor Total para este item (R$): "))
                except ValueError:
                    print("\n❌ Entrada inválida. Use números.")
                    continue

                item_alvo['Quantidade'] = str(nova_quantidade)
                item_alvo['Valor Item (R$)'] = f"{novo_valor_item:.2f}"
                print("\n✅ Quantidade/Valor do item atualizados manualmente.")

            elif acao == '2':
                todos_itens[:] = [item for item in todos_itens if item['ID do Item'] != item_alvo['ID do Item']]
                print(f"\n✅ Item '{item_alvo['Produto']}' removido.")
            
            else:
                print("Operação cancelada.")
                
        else:
            print("⚠️ Opção inválida.")

# =================================================================
#               FUNÇÕES PRINCIPAIS 
# =================================================================
            
def adicionar_pedido(cabecalhos, todos_itens):
    """Cria um novo pedido com múltiplos itens e lógica de seleção forçada."""
    produtos_disponiveis = carregar_produtos()
    if not produtos_disponiveis:
        return

    try:
        novo_id = gerar_novo_id_pedido(cabecalhos)
        print("\n--- INICIAR NOVO PEDIDO ---")
        
        data_pedido = datetime.now().strftime("%d-%m-%Y %H:%M") # Data de referência para 30 dias
        cliente = input("Nome do Cliente: ")
        
        adicionar_item_a_pedido(novo_id, todos_itens, produtos_disponiveis)
        
        valor_total = calcular_valor_total_pedido(novo_id, todos_itens)
        if valor_total == 0.0:
            print("\n❌ Pedido sem itens. Cancelando operação.")
            return

        print(f"\n--- Finalizando Pedido ID {novo_id} ---")
        print(f"VALOR TOTAL: R$ {valor_total:.2f}")

        # --- Seleções Forçadas ---
        forma_pagamento = selecionar_opcao("Forma de Pagamento", OPCOES_FORMA_PAGAMENTO)
        status_pagamento = selecionar_opcao("Status do Pagamento", OPCOES_STATUS_PAGAMENTO)
        status_pedido = selecionar_opcao("Status do Pedido", OPCOES_STATUS_PEDIDO)
        
        # Variáveis de inicialização
        data_hora_entrega = ""
        data_vencimento_prazo = ""
        valor_pago = "0.00"
        data_pagamento = ""
        
        if status_pedido == 'Pendente':
            data_hora_entrega = solicitar_data_hora_entrega() 

        # Lógica de Pagamento
        if status_pagamento == 'Pago':
            valor_pago = f"{valor_total:.2f}"
            data_pagamento = datetime.now().strftime("%d-%m-%Y %H:%M")
            data_vencimento_prazo = ""
            
        elif status_pagamento == 'Parcial':
            print("\n--- REGISTRO INICIAL DE PAGAMENTO PARCIAL ---")
            temp_cabecalho = {'Valor Total (R$)': f"{valor_total:.2f}", 'Valor Pago (R$)': '0.00'}
            registrar_pagamento_parcial(temp_cabecalho)
            
            valor_pago = temp_cabecalho['Valor Pago (R$)']
            data_pagamento = temp_cabecalho.get('Data do Pagamento', "")
            status_pagamento = temp_cabecalho['Status do Pagamento'] # Atualiza status (pode ter virado 'Pago')

            # 🎯 NOVO CÓDIGO AQUI: Se ainda for Parcial, solicita a data limite para o restante
            if status_pagamento == 'Parcial':
                print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO RESTANTE ---")
                data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)
            else:
                data_vencimento_prazo = "" # Limpa se virou Pago

        elif status_pagamento == 'Pendente':
            valor_pago = "0.00"
            data_pagamento = ""
            print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO TOTAL ---")
            data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)
        
        novo_cabecalho = {
            'ID do Pedido': str(novo_id),
            'Data do Pedido': data_pedido,
            'Nome do Cliente': cliente,
            'Valor Total (R$)': f"{valor_total:.2f}",
            'Valor Pago (R$)': valor_pago,
            'Forma de Pagamento': forma_pagamento,
            'Status do Pagamento': status_pagamento,
            'Data do Pagamento': data_pagamento,
            'Data Vencimento Prazo': data_vencimento_prazo,
            'Status do Pedido': status_pedido,
            'Data/Hora Entrega': data_hora_entrega
        }
        
        cabecalhos.append(novo_cabecalho)
        salvar_cabecalhos(cabecalhos)
        salvar_itens(todos_itens)
        print("\n✅ Pedido registrado com sucesso!")
        
    except ValueError:
        print("\n❌ Erro: Por favor, insira números válidos.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")


def editar_pedido(cabecalhos, todos_itens):
    """Permite a edição completa dos itens, status e pagamentos de um pedido existente."""
    id_alvo = input("\nDigite o ID do pedido para EDITAR: ")
    cabecalho_alvo = next((c for c in cabecalhos if c['ID do Pedido'] == id_alvo), None)
    produtos_disponiveis = carregar_produtos()

    if not cabecalho_alvo:
        print(f"\n❌ Pedido com ID {id_alvo} não encontrado.")
        return

    while True:
        valor_total_atual = calcular_valor_total_pedido(id_alvo, todos_itens)
        cabecalho_alvo['Valor Total (R$)'] = f"{valor_total_atual:.2f}"
        
        print("\n" + "="*40)
        print(f"    EDITANDO PEDIDO ID: {id_alvo}")
        print("="*40)
        print(f"Cliente: {cabecalho_alvo['Nome do Cliente']}")
        print(f"Valor Total: R$ {cabecalho_alvo['Valor Total (R$)']}")
        print(f"Valor Pago: R$ {cabecalho_alvo.get('Valor Pago (R$)', '0.00')}")
        print(f"Status Pagamento: {cabecalho_alvo['Status do Pagamento']} | Forma: {cabecalho_alvo['Forma de Pagamento']}")
        print(f"Status Pedido: {cabecalho_alvo['Status do Pedido']} | Entrega: {cabecalho_alvo['Data/Hora Entrega']}")
        print("-" * 40)
        print("1. Editar Itens do Pedido (Adicionar/Remover/Alterar Qtd)") 
        print("2. Alterar Pagamento/Registrar Parcial")
        print("3. Alterar Status/Agendar Entrega")
        print("4. FINALIZAR EDIÇÃO e Salvar")
        print("-" * 40)

        escolha = input("Escolha uma opção de edição: ")

        if escolha == '1':
            menu_edicao_itens(id_alvo, todos_itens, produtos_disponiveis)

        elif escolha == '2':
            print("\n--- Alterar Dados de Pagamento ---")
            
            nova_forma = selecionar_opcao("Nova Forma de Pagamento", OPCOES_FORMA_PAGAMENTO)
            novo_status = selecionar_opcao("Novo Status do Pagamento", OPCOES_STATUS_PAGAMENTO)
            
            cabecalho_alvo['Forma de Pagamento'] = nova_forma

            if novo_status == 'Parcial':
                registrar_pagamento_parcial(cabecalho_alvo)
                novo_status = cabecalho_alvo['Status do Pagamento'] # Pode ter mudado para 'Pago'
                
                # 🎯 NOVO CÓDIGO AQUI: Se após o registro parcial, o status AINDA for Parcial, solicita novo prazo
                if novo_status == 'Parcial':
                    print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO RESTANTE ---")
                    data_pedido_base = cabecalho_alvo['Data do Pedido']
                    cabecalho_alvo['Data Vencimento Prazo'] = solicitar_data_limite_pagamento(data_pedido_base, novo_status)
                else:
                    cabecalho_alvo['Data Vencimento Prazo'] = "" # Limpa se virou Pago

            elif novo_status == 'Pago':
                cabecalho_alvo['Valor Pago (R$)'] = cabecalho_alvo['Valor Total (R$)']
                cabecalho_alvo['Data do Pagamento'] = datetime.now().strftime("%d-%m-%Y %H:%M") 
                cabecalho_alvo['Data Vencimento Prazo'] = "" # Limpa o prazo
            
            elif novo_status == 'Pendente':
                # Só zera o valor pago se o status anterior não for Parcial
                if cabecalho_alvo['Status do Pagamento'] != 'Pendente': 
                    cabecalho_alvo['Valor Pago (R$)'] = '0.00'
                cabecalho_alvo['Data do Pagamento'] = ""
                
                print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO TOTAL ---")
                data_pedido_base = cabecalho_alvo['Data do Pedido']
                cabecalho_alvo['Data Vencimento Prazo'] = solicitar_data_limite_pagamento(data_pedido_base, novo_status)

            cabecalho_alvo['Status do Pagamento'] = novo_status
            
            print(f"\n✅ Pagamento atualizado para Status: {novo_status} e Forma: {nova_forma}")
        
        elif escolha == '3':
            novo_status_pedido = selecionar_opcao("Novo Status do Pedido", OPCOES_STATUS_PEDIDO)
            
            if novo_status_pedido == 'Pendente':
                cabecalho_alvo['Data/Hora Entrega'] = solicitar_data_hora_entrega()
                print(f"✅ Entrega agendada para: {cabecalho_alvo['Data/Hora Entrega']}")
            elif novo_status_pedido == 'Entregue':
                cabecalho_alvo['Data/Hora Entrega'] = "ENTREGUE"
            
            cabecalho_alvo['Status do Pedido'] = novo_status_pedido
            print(f"\n✅ Status do Pedido atualizado para: {novo_status_pedido}")

        elif escolha == '4':
            salvar_cabecalhos(cabecalhos)
            salvar_itens(todos_itens)
            print(f"\n✅ Pedido ID {id_alvo} salvo e alterações finalizadas.")
            break
            
        else:
            print("\n⚠️ Opção inválida. Tente novamente.")
            
# --- Funções de Visualização e Menu Principal ---

def visualizar_pedidos(cabecalhos):
    """Imprime todos os cabeçalhos de pedidos em formato de tabela."""
    if not cabecalhos:
        print("\nNenhum pedido encontrado.")
        return

    print("\n--- Todos os Pedidos (Visão Geral) ---")
    
    larguras = {campo: len(campo) for campo in CAMPOS_CABECALHO}
    for pedido in cabecalhos:
        for campo in CAMPOS_CABECALHO:
            larguras[campo] = max(larguras[campo], len(pedido.get(campo, '')))

    linha_cabecalho = " | ".join(campo.ljust(larguras[campo]) for campo in CAMPOS_CABECALHO)
    print(linha_cabecalho)
    print("-" * len(linha_cabecalho))

    for pedido in cabecalhos:
        linha_dados = " | ".join(pedido.get(campo, '').ljust(larguras[campo]) for campo in CAMPOS_CABECALHO)
        print(linha_dados)
        
def buscar_pedido(cabecalhos, id_pedido):
    """Busca um pedido específico por ID."""
    return next((c for c in cabecalhos if c['ID do Pedido'] == id_pedido), None)

def menu_principal():
    """Função principal que exibe o menu e executa as ações."""
    inicializar_csv()

    while True:
        cabecalhos = carregar_cabecalhos()
        todos_itens = carregar_itens()

        print("\n" + "="*30)
        print("    Gerenciador de Pedidos")
        print("="*30)
        print("1. Adicionar Novo Pedido")
        print("2. Visualizar Todos os Pedidos")
        print("3. Buscar Pedido por ID")
        print("4. Editar Pedido Existente")
        print("5. Sair")
        print("-" * 30)

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_pedido(cabecalhos, todos_itens)
        elif escolha == '2':
            visualizar_pedidos(cabecalhos)
        elif escolha == '3':
            id_busca = input("Digite o ID do pedido para buscar: ")
            pedido = buscar_pedido(cabecalhos, id_busca)
            if pedido:
                # 1. Recalcula o Valor Total dos Itens
                valor_total_itens = calcular_valor_total_pedido(id_busca, todos_itens)
                
                # 2. Obtém o Valor Pago do cabeçalho (garante que seja float, padrão 0)
                try:
                    valor_pago = float(pedido.get('Valor Pago (R$)', '0.00'))
                except ValueError:
                    valor_pago = 0.0
                
                # 3. Calcula o Saldo Devedor
                saldo_devedor = valor_total_itens - valor_pago
                
                print("\n--- Pedido Encontrado ---")
                for chave, valor in pedido.items():
                    print(f"   {chave}: {valor}")
                
                # --- EXIBINDO O SALDO DEVEDOR ---
                print(f"   " + "="*40)
                print(f"   VALOR TOTAL DO PEDIDO: R$ {valor_total_itens:.2f}")
                print(f"   VALOR PAGO REGISTRADO: R$ {valor_pago:.2f}")
                print(f"   SALDO DEVEDOR (A PAGAR): R$ {saldo_devedor:.2f}")
                print(f"   " + "="*40)
                
                itens_pedido = [item for item in todos_itens if item['ID do Pedido'] == id_busca]
                if itens_pedido:
                    print("\n   --- ITENS ---")
                    for item in itens_pedido:
                        print(f"   {item['Produto']} | Qtd: {item['Quantidade']} | Total: R$ {item['Valor Item (R$)']}")
            else:
                print(f"\n❌ Pedido com ID {id_busca} não encontrado.")
        elif escolha == '4':
            editar_pedido(cabecalhos, todos_itens)
        elif escolha == '5':
            print("\nObrigado por usar o Gerenciador de Pedidos. Até logo!")
            break
        else:
            print("\n⚠️ Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    menu_principal()