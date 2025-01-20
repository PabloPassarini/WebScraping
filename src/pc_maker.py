import sqlite3, requests, os, re
from bs4 import BeautifulSoup
import streamlit as st
class BaseDados:
    def __init__(self, db):
        """
        Inicializa a conexão com o banco de dados.
        :param db: Caminho para o arquivo do banco de dados SQLite.
        """
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def insert_hardware(self, produto, categoria, link, loja, valor_avista, ultima_att):
        """
        Insere um registro na tabela 'hardware'.
        :param produto: Nome do produto.
        :param categoria: Categoria do produto.
        :param link: Link do produto.
        :param loja: Nome da loja.
        :param valor_avista: Valor à vista do produto.
        :param ultima_att: Data da última atualização.
        :return: 'OK' em caso de sucesso ou uma mensagem de erro.
        """
        try:
            self.cursor.execute(
                '''
                INSERT INTO hardware (produto, categoria, link, loja, valor_avista, ultima_att)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (produto, categoria, link, loja, valor_avista, ultima_att)
            )
            self.conn.commit()
            return 'OK'
        except Exception as e:
            return f'Erro: {e}'  # Corrigido para capturar todos os tipos de exceção

    def get_cat(self, col, filter):
        """
        Retorna todos os registros da tabela 'hardware' que atendem ao filtro em uma coluna.
        :param col: Nome da coluna usada como filtro.
        :param filter: Valor usado como filtro.
        :return: Lista de registros ou uma mensagem de erro.
        """
        try:
            query = f'SELECT * FROM hardware WHERE {col} = ?'
            self.cursor.execute(query, (filter,))
            return self.cursor.fetchall()
        except Exception as e:
            return f'Erro: {e}'

    def get_vcols(self, col):
        """
        Retorna valores únicos de uma coluna específica com base em um filtro.
        :param col: Nome da coluna usada como filtro.
        :param filter: Valor usado como filtro.
        :return: Lista de valores únicos ou uma mensagem de erro.
        """
        try:
            # Lista de colunas disponíveis na tabela
            colunas = ['produto', 'categoria', 'link', 'loja', 'valor_avista', 'ultima_att']
            
            # Verifica se a coluna existe e obtém seu índice
            if col not in colunas:
                raise ValueError(f"Coluna '{col}' inválida.")
            index = colunas.index(col)

            # Executa a consulta com o filtro
            query = f"SELECT {col} FROM hardware"
            self.cursor.execute(query)
            registros = self.cursor.fetchall()

            # Retorna valores únicos da coluna especificada
            #return list(set([linha[index] for linha in registros]))
            return list(registros[0])
        except Exception as e:
            return f'Erro: {e}'

    def close_conn(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conn.close()


class WebScraping():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def get_values(self, link):
        if 'kabum' in link:
            loja = 'KABUM'
            tag_preco = 'h4'
            class_preco = 'sc-5492faee-2 ipHrwP finalPrice'

            tag_nome_prod = 'h1'
            class_nome_prod = 'sc-58b2114e-6 brTtKt'

        try:
            response = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            valor = soup.find_all(tag_preco, class_=re.compile(class_preco))[0].text
            valor = valor[3:]
            
            nome_prod = soup.find_all(tag_nome_prod, class_=re.compile(class_nome_prod))[0].text
            return [valor, nome_prod]
        
        except Exception as e:
            return [f'Erro: {e}']
            

bd = BaseDados(r'/home/pablopassarini/Projetos/WebScraping/data_base/produtos.db')
categorias = bd.get_vcols('categoria')

st.sidebar.title('Produtos')
cat_sb = st.sidebar.selectbox('Categoria:', (categorias))