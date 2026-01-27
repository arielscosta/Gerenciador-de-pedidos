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
    """Permite listar, adicionar, remover e EDITAR quantidade e tipo (UN/CX)."""
    while True:
        itens_atuais = [item for item in todos_itens if item['ID do Pedido'] == id_pedido_alvo]
        
        print("\n" + "─"*60)
        print(f"📦 ITENS NO PEDIDO #{id_pedido_alvo}")
        print("─"*60)
        
        if not itens_atuais:
            print("   (Pedido Vazio)")
        else:
            for i, item in enumerate(itens_atuais, 1):
                print(f"{i}. {item['Produto']:<30} | Qtd: {item['Quantidade']:<4} | Total: R$ {item['Valor Item (R$)']}")
        
        print("-" * 60)
        print("A. Adicionar Novo Produto")
        print("E. EDITAR Item (Alterar Qtd ou Tipo UN/CX)")
        print("R. Remover Item (Excluir)")
        print("F. Finalizar e Recalcular Total")
        print("-" * 60)
        
        acao = input("Escolha uma ação: ").upper()

        if acao == 'F':
            break
        
        elif acao == 'E':
            if not itens_atuais:
                print("❌ Não há itens para editar.")
                continue
            try:
                idx = int(input("Digite o número da linha para EDITAR: ")) - 1
                if 0 <= idx < len(itens_atuais):
                    item_editando = itens_atuais[idx]
                    
                    # 1. Identifica qual é o produto original no produtos.csv
                    # Precisamos limpar o "(UN)" ou "(CX)" do nome para buscar no CSV
                    nome_limpo = item_editando['Produto'].replace(" (UN)", "").replace(" (CX)", "").strip()
                    
                    # Busca o produto correspondente no dicionário de produtos
                    prod_info = next((info for info in produtos_disponiveis.values() if info['Nome do Produto'] == nome_limpo), None)
                    
                    if not prod_info:
                        print("❌ Produto base não encontrado no estoque para recalcular.")
                        continue

                    print(f"\nEditando: {nome_limpo}")
                    print("1. Mudar para UNIDADE (R$ " + prod_info['Valor Unidade (R$)'] + ")")
                    print("2. Mudar para CAIXA (R$ " + prod_info['Valor Caixa (R$)'] + ")")
                    tipo_venda = input("Escolha o novo tipo: ")
                    
                    nova_qtd = int(input(f"Nova quantidade: "))
                    
                    if nova_qtd <= 0:
                        print("❌ Quantidade inválida.")
                        continue

                    # 2. Aplica o novo preço e nome
                    if tipo_venda == '1':
                        preco = float(prod_info['Valor Unidade (R$)'])
                        novo_nome = f"{nome_limpo} (UN)"
                    else:
                        preco = float(prod_info['Valor Caixa (R$)'])
                        novo_nome = f"{nome_limpo} (CX)"

                    # 3. Atualiza o item na lista principal
                    item_editando['Produto'] = novo_nome
                    item_editando['Quantidade'] = str(nova_qtd)
                    item_editando['Valor Item (R$)'] = f"{(nova_qtd * preco):.2f}"
                    
                    print(f"✅ Item atualizado: {novo_nome} x {nova_qtd}!")
                else:
                    print("❌ Linha inválida.")
            except ValueError:
                print("❌ Erro: Entrada inválida.")

        elif acao == 'A':
            # --- Lógica de Adicionar (Mantida igual para funcionar com seu CSV) ---
            print("\nPRODUTOS DISPONÍVEIS:")
            for cod, info in produtos_disponiveis.items():
                print(f"{cod:<5} | {info['Nome do Produto']:<30} | UN: {info['Valor Unidade (R$)']:<8} | CX: {info['Valor Caixa (R$)']}")
            
            codigo = input("\nCódigo: ").strip().zfill(2)
            if codigo in produtos_disponiveis:
                p = produtos_disponiveis[codigo]
                t = input("1. Unidade | 2. Caixa: ")
                q = int(input("Quantidade: "))
                pr = float(p['Valor Unidade (R$)']) if t == '1' else float(p['Valor Caixa (R$)'])
                nm = f"{p['Nome do Produto']} ({'UN' if t == '1' else 'CX'})"
                todos_itens.append({'ID do Pedido': id_pedido_alvo, 'Produto': nm, 'Quantidade': str(q), 'Valor Item (R$)': f"{(q*pr):.2f}"})
            else:
                print("❌ Código inválido.")

        elif acao == 'R':
            try:
                idx = int(input("Linha para remover: ")) - 1
                todos_itens.remove(itens_atuais[idx])
                print("🗑️ Item removido.")
            except:
                print("❌ Erro ao remover.")

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
            
def adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=None):
    """Lança um novo pedido, permitindo nome automático ou manual."""
    produtos_disponiveis = carregar_produtos()
    if not produtos_disponiveis:
        return

    novo_id = gerar_novo_id_pedido(cabecalhos)
    data_pedido = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    # Lógica de Nome Automatizada
    if nome_sugerido:
        nome_cliente = nome_sugerido
        print(f"\nLançando pedido para: {nome_cliente.upper()}")
    else:
        nome_cliente = input("\nNome do Cliente: ")

    try:
        # 1. Adiciona os itens ao pedido
        adicionar_item_a_pedido(novo_id, todos_itens, produtos_disponiveis)
        
        # 2. Calcula o total
        valor_total = calcular_valor_total_pedido(novo_id, todos_itens)
        if valor_total == 0.0:
            print("\n❌ Pedido sem itens. Cancelando operação.")
            return

        print(f"\n--- Finalizando Pedido ID {novo_id} ---")
        print(f"VALOR TOTAL: R$ {valor_total:.2f}")

        # --- Seleções de Status ---
        forma_pagamento = selecionar_opcao("Forma de Pagamento", OPCOES_FORMA_PAGAMENTO)
        status_pagamento = selecionar_opcao("Status do Pagamento", OPCOES_STATUS_PAGAMENTO)
        status_pedido = selecionar_opcao("Status do Pedido", OPCOES_STATUS_PEDIDO)
        
        # Inicialização de campos
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
            status_pagamento = temp_cabecalho['Status do Pagamento']

            if status_pagamento == 'Parcial':
                print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO RESTANTE ---")
                data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)
            else:
                data_vencimento_prazo = "" 

        elif status_pagamento == 'Pendente':
            valor_pago = "0.00"
            data_pagamento = ""
            print("\n--- REGISTRO DE DATA ESPERADA PARA PAGAMENTO TOTAL ---")
            data_vencimento_prazo = solicitar_data_limite_pagamento(data_pedido, status_pagamento)
        
        # Montagem do Dicionário (Corrigido para nome_cliente)
        novo_cabecalho = {
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
        
        cabecalhos.append(novo_cabecalho)
        salvar_cabecalhos(cabecalhos)
        salvar_itens(todos_itens)
        print("\n✅ Pedido registrado com sucesso!")
        
    except ValueError:
        print("\n❌ Erro: Por favor, insira números válidos.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")

def editar_pedido(cabecalhos, todos_itens):
    """Edita um pedido existente com recálculo automático de valores para evitar fraudes."""
    id_pedido = input("\nDigite o ID do pedido que deseja editar: ").strip()
    
    # Busca o pedido no cabeçalho
    pedido = next((p for p in cabecalhos if p['ID do Pedido'] == id_pedido), None)
    
    if not pedido:
        print(f"❌ Pedido ID {id_pedido} não encontrado.")
        return
    alterou_itens = False
    while True:
        print(f"\n" + "═"*50)
        print(f"      EDITANDO PEDIDO #{id_pedido} - {pedido['Nome do Cliente']}")
        print("═"*50)
        print("1. Adicionar/Remover/Alterar Itens (Produtos)")
        print("2. Registrar Pagamento (Dar Baixa)")
        print("3. Alterar Status do Pedido (Entrega/Retirada)")
        print("4. SALVAR E SAIR")
        print("5. Cancelar Edição")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            # Chama sua função de manipulação de itens
            adicionar_item_a_pedido(id_pedido, todos_itens, carregar_produtos())
            alterou_itens = True
            print("📝 Alteração de itens registrada.")

        elif opcao == '2':
            # Chama sua função de pagamento parcial/total
            registrar_pagamento_parcial(pedido)
            # Nota: registrar_pagamento_parcial já atualiza Status e Valor Pago

        elif opcao == '3':
            novo_status = selecionar_opcao("Status do Pedido", OPCOES_STATUS_PEDIDO)
            pedido['Status do Pedido'] = novo_status
            if novo_status == 'Entregue' and not pedido['Data/Hora Entrega']:
                pedido['Data/Hora Entrega'] = datetime.now().strftime("%d-%m-%Y %H:%M")

        elif opcao == '4':
            # --- TRAVA DE SEGURANÇA: RECALCULO AUTOMÁTICO ---
            if alterou_itens:
                print("\n🔄 Recalculando valor total com base nos itens atualizados...")
                novo_total = calcular_valor_total_pedido(id_pedido, todos_itens)
                
                # Atualiza o campo de valor total sem permitir edição manual
                pedido['Valor Total (R$)'] = f"{novo_total:.2f}"
                
                # Checagem de integridade: Se o total subiu e o status era 'Pago', vira 'Parcial'
                valor_pago = float(pedido.get('Valor Pago (R$)', 0))
                if valor_pago < novo_total:
                    if pedido['Status do Pagamento'] == 'Pago':
                        pedido['Status do Pagamento'] = 'Parcial'
                        print("⚠️ Alerta: O valor total aumentou. Status alterado para 'Parcial'.")
                elif valor_pago >= novo_total and novo_total > 0:
                    pedido['Status do Pagamento'] = 'Pago'

            salvar_cabecalhos(cabecalhos)
            salvar_itens(todos_itens)
            print("\n✅ Alterações salvas com sucesso!")
            break

        elif opcao == '5':
            print("\nEdição descartada.")
            break
            
        else:
            print("\n⚠️ Opção inválida. Tente novamente.")
            
# --- Funções de Visualização e Menu Principal ---

def visualizar_detalhes_cliente(pedidos_cliente, todos_itens):
    """Permite escolher um pedido da lista do cliente para ver detalhes e itens."""
    id_escolhido = input("\nDigite o ID do pedido que deseja ver detalhes: ").strip()
    
    # Busca o pedido dentro da lista filtrada do cliente
    pedido = next((p for p in pedidos_cliente if p['ID do Pedido'] == id_escolhido), None)
    
    if pedido:
        print("\n" + "═"*50)
        print(f"      DETALHES DO PEDIDO #{id_escolhido}")
        print("═"*50)
        for chave, valor in pedido.items():
            print(f"{chave:<22}: {valor}")
        
        print("-" * 50)
        print("ITENS DO PEDIDO:")
        itens_pedido = [item for item in todos_itens if item['ID do Pedido'] == id_escolhido]
        
        if itens_pedido:
            for item in itens_pedido:
                print(f"• {item['Produto']} | Qtd: {item['Quantidade']} | Subtotal: R$ {item['Valor Item (R$)']}")
        else:
            print("Nenhum item encontrado para este pedido.")
        print("═"*50)
        input("\nPressione Enter para voltar ao painel...")
    else:
        print("\n❌ ID não encontrado na lista deste cliente.")


def gerenciar_por_cliente(cabecalhos, todos_itens):
    """Filtra pedidos por nome ou automatiza cadastro de novo cliente."""
    nome_busca = input("\nDigite o nome do cliente para gerenciar: ").strip()
    
    if not nome_busca:
        print("⚠️ Nome não pode ser vazio.")
        return

    # Filtra os pedidos que contêm o nome buscado
    pedidos_cliente = [p for p in cabecalhos if nome_busca.lower() in p['Nome do Cliente'].lower()]
    
    # --- AUTOMAÇÃO PARA NOVO CLIENTE ---
    if not pedidos_cliente:
        print(f"\n🟡 Cliente '{nome_busca}' não encontrado.")
        confirmar = input(f"Deseja cadastrar e lançar pedido para '{nome_busca}' agora? (S/N): ").upper()
        if confirmar == 'S':
            # Chama o adicionar_pedido passando o nome já digitado
            adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=nome_busca)
            return
        else:
            return

    # Se encontrou, pega o nome exato do primeiro registro para o Painel
    nome_exato = pedidos_cliente[0]['Nome do Cliente']
    
    while True:
        total_devedor_acumulado = 0.0
        print(f"\n" + "═"*75)
        print(f"    PAINEL DE GESTÃO: {nome_exato.upper()}")
        print("═"*75)
        
        # Cabeçalho da tabela
        print(f"{'ID':<5} | {'DATA PEDIDO':<18} | {'TOTAL':<10} | {'SALDO':<10} | {'STATUS'}")
        print("-" * 75)
        
        for p in pedidos_cliente:
            v_total = float(p['Valor Total (R$)'])
            v_pago = float(p.get('Valor Pago (R$)', '0.00'))
            saldo = v_total - v_pago
            total_devedor_acumulado += saldo
            print(f"{p['ID do Pedido']:<5} | {p['Data do Pedido']:<18} | {v_total:<10.2f} | {saldo:<10.2f} | {p['Status do Pagamento']}")
        
        # Extrato de Pagamentos
        print("\n💰 HISTÓRICO DE LANÇAMENTOS (PAGAMENTOS):")
        tem_pagamento = False
        for p in pedidos_cliente:
            if p.get('Data do Pagamento') and float(p.get('Valor Pago (R$)', 0)) > 0:
                print(f"   • {p['Data do Pagamento']} --> Recebido R$ {p['Valor Pago (R$)']} (Pedido #{p['ID do Pedido']})")
                tem_pagamento = True
        
        if not tem_pagamento:
            print("   (Nenhum pagamento registrado)")

        print("-" * 75)
        print(f"💸 TOTAL A RECEBER DESTE CLIENTE: R$ {total_devedor_acumulado:.2f}")
        print("-" * 75)
        
        print("1. Lançar Novo Pedido")
        print("2. EDITAR PEDIDO (Pagamentos, Itens, Excluir)")
        print("3. VER DETALHES DE UM PEDIDO (Ver Itens)") # <-- NOVA OPÇÃO
        print("4. Voltar ao Menu Principal")
        
        op = input("\nEscolha uma opção: ")

        if op == '1':
            adicionar_pedido(cabecalhos, todos_itens, nome_sugerido=nome_exato)
            cabecalhos = carregar_cabecalhos()
            pedidos_cliente = [p for p in cabecalhos if nome_exato.lower() in p['Nome do Cliente'].lower()]
        elif op == '2':
            editar_pedido(cabecalhos, todos_itens)
            cabecalhos = carregar_cabecalhos()
            pedidos_cliente = [p for p in cabecalhos if nome_exato.lower() in p['Nome do Cliente'].lower()]
        elif op == '3':
            # CHAMADA DA NOVA FUNÇÃO
            visualizar_detalhes_cliente(pedidos_cliente, todos_itens) 
        elif op == '4':
            break

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
    inicializar_csv()

    while True:
        cabecalhos = carregar_cabecalhos()
        todos_itens = carregar_itens()

        print("\n" + "="*40)
        print("      SISTEMA DE GESTÃO ADEGA v2.0")
        print("="*40)
        print("1. GESTÃO DE CLIENTES (Venda/Edição/Detalhes)")
        print("2. Visualizar Todos os Pedidos (Geral)")
        print("3. Sair")
        print("-" * 40)

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            gerenciar_por_cliente(cabecalhos, todos_itens)
        elif escolha == '2':
            visualizar_pedidos(cabecalhos)
        elif escolha == '3':
            print("\nEncerrando sistema. Até logo!")
            break
        else:
            print("\n⚠️ Opção inválida.")

if __name__ == "__main__":
    menu_principal()