A ideia principal desse projeto, é me desafiar, estudar e aprender a trabalhar com Python e suas bibliotecas, Git e a ferramenta Github, comentários detalhados em todo o código, estrutura inteligente e toda organização na criação de um código;
Inicialmente o banco de dados será feito com arquivos CSV dedicado no excel;
Usarei Engenharia de Prompt e Arquitetura com uma abordagem de pair programming com IA da google (Gemini);
Processo de desenvolvimento:
Como Engenheiro do sistema, defini os requisitos, a estrutura de dados e a lógica de negócio, utilizando a IA para a geração do código-fonte e refatoração, garantindo as boas práticas da linguagem Python.
Funcionalidades:
Registro de Pedidos: Adição de múltiplos produtos por cliente.
Controle de Pagamento: Suporte a pagamentos Totais, Pendentes ou Parciais (com cálculo automático de saldo devedor).
Gestão de Prazos: Validação de data de pagamento (limite de 30 dias após o pedido).
Agendamento: Definição de data e hora para entregas pendentes.
Persistência de Dados: Todos os dados são salvos em pedidos_cabecalho.csv e pedidos_itens.csv.
Como Executar o Programa:
1. Pré-requisitos
•	Python 3.x instalado.
•	O arquivo produtos.csv deve estar na mesma pasta do script (contendo as colunas: Código, Nome do Produto, Valor Unidade (R$), Qtd por Caixa, Valor Caixa (R$)).
2. Execução Rápida (Windows)
Se você está no Windows, basta dar um duplo clique no arquivo:
•	executar.bat
Isso abrirá o terminal e iniciará o sistema automaticamente sem que você precise digitar comandos.
3. Execução via Terminal
Caso prefira o terminal manual:
Abra o cmd;
Acesse a pasta onde salvou os arquivos;
Digite: python gerenciador_pedidos.py
Como Testar o Sistema:
Siga este roteiro para validar as funções principais:
Criar um Pedido:
Escolha a opção 1. Informe o nome de um cliente.
Adicione um produto (ex: digite o código de um produto que esteja no seu produtos.csv).
Defina o status como Parcial e registre um valor menor que o total para testar o cálculo de saldo.
Consultar Saldo Devedor:
Escolha a opção 3 (Buscar por ID) e digite o ID do pedido que acabou de criar.
O sistema exibirá o Valor Total, o Valor Pago e o Saldo Devedor.
Atualizar Pagamento:
Escolha a opção 4 (Editar), selecione o ID e vá em Alterar Pagamento.
Tente completar o valor para ver o status mudar automaticamente para Pago.
Verificar Arquivos:
Após fechar o programa, abra os arquivos .csv no Excel ou Bloco de Notas para garantir que as linhas foram gravadas corretamente.
Estrutura de Arquivos:
gerenciador_pedidos.py: Código fonte principal.
executar.bat: Atalho para execução no Windows.
produtos.csv: Banco de dados de produtos (Necessário).
pedidos_cabecalho.csv: Armazena os dados gerais dos pedidos.
pedidos_itens.csv: Armazena os itens individuais de cada pedido.
