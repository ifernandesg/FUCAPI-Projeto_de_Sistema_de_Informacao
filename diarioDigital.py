import sqlite3
from datetime import datetime
import os
from textwrap import dedent

class DiarioEletronico:
    def __init__(self):
        self.conn = sqlite3.connect('diario.db')
        self.criar_tabela()
        
    def criar_tabela(self):
        """Cria a tabela de entradas se não existir"""
        query = """
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            conteudo TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()
    
    def adicionar_entrada(self, conteudo):
        """Adiciona uma nova entrada ao diário"""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "INSERT INTO entradas (data_hora, conteudo) VALUES (?, ?)"
        self.conn.execute(query, (data_hora, conteudo))
        self.conn.commit()
    
    def listar_entradas(self):
        """Retorna todas as entradas do diário"""
        query = "SELECT data_hora, conteudo FROM entradas ORDER BY datetime(data_hora) DESC"
        cursor = self.conn.execute(query)
        return cursor.fetchall()
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Exibe o menu principal"""
    print(dedent("""
    ========================================
            DIÁRIO ELETRÔNICO v2.0          
    ========================================
    1. Escrever no diário
    2. Ler entradas anteriores
    3. Buscar por termo
    4. Sair
    ========================================
    """))

def escrever_entrada(diario):
    """Permite ao usuário escrever uma nova entrada"""
    limpar_tela()
    print("Escreva sua entrada (digite 'fim' em uma linha nova para terminar):\n")
    
    linhas = []
    while True:
        linha = input()
        if linha.lower() == 'fim':
            break
        linhas.append(linha)
    
    if linhas:
        conteudo = '\n'.join(linhas)
        diario.adicionar_entrada(conteudo)
        print("\n✅ Entrada salva com sucesso!")
    else:
        print("\n⚠️ Nenhum conteúdo foi digitado.")
    
    input("\nPressione Enter para continuar...")

def ler_entradas(diario):
    """Exibe todas as entradas do diário"""
    limpar_tela()
    entradas = diario.listar_entradas()
    
    if not entradas:
        print("Nenhuma entrada encontrada no diário.")
    else:
        print("ENTRADAS DO DIÁRIO".center(50))
        print("="*50)
        for data_hora, conteudo in entradas:
            print(f"\n📅 {data_hora}")
            print("-"*50)
            print(conteudo)
            print("="*50)
    
    input("\nPressione Enter para continuar...")

def buscar_entradas(diario):
    """Busca entradas por termo"""
    limpar_tela()
    termo = input("Digite o termo que deseja buscar: ").strip().lower()
    
    if not termo:
        print("Nenhum termo de busca foi informado.")
        input("\nPressione Enter para continuar...")
        return
    
    query = """
    SELECT data_hora, conteudo FROM entradas 
    WHERE LOWER(conteudo) LIKE ? 
    ORDER BY datetime(data_hora) DESC
    """
    cursor = diario.conn.execute(query, (f'%{termo}%',))
    resultados = cursor.fetchall()
    
    limpar_tela()
    print(f"RESULTADOS PARA: '{termo}'".center(50))
    print("="*50)
    
    if not resultados:
        print("\nNenhuma entrada encontrada com o termo especificado.")
    else:
        for data_hora, conteudo in resultados:
            print(f"\n📅 {data_hora}")
            print("-"*50)
            print(conteudo)
            print("="*50)
    
    input("\nPressione Enter para continuar...")

def main():
    """Função principal do programa"""
    diario = DiarioEletronico()
    
    try:
        while True:
            limpar_tela()
            mostrar_menu()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                escrever_entrada(diario)
            elif opcao == '2':
                ler_entradas(diario)
            elif opcao == '3':
                buscar_entradas(diario)
            elif opcao == '4':
                print("\nObrigado por usar o Diário Eletrônico. Até mais!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")
    finally:
        diario.fechar()

if __name__ == "__main__":
    main()