import sqlite3

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

    def get_vcols(self, col, filter):
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
            query = f'SELECT * FROM hardware WHERE {col} = ?'
            self.cursor.execute(query, (filter,))
            registros = self.cursor.fetchall()

            # Retorna valores únicos da coluna especificada
            return list(set([linha[index] for linha in registros]))
        except Exception as e:
            return f'Erro: {e}'

    def close_conn(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conn.close()





basedata = BaseDados(r'/home/pablopassarini/Projetos/WebScraping/data_base/produtos.db')
#print(basedata.insert_hardware('Memória RAM Kingston Fury Beast, 8GB, 3200MHz, DDR4, CL16, Preto - KF432C16BB/8', 'RAM', 'https://www.kabum.com.br/produto/172365/memoria-ram-kingston-fury-beast-8gb-3200mhz-ddr4-cl16-preto-kf432c16bb-8', 'KABUM', '154.99', '18/01/2025'))
print(basedata.get_vcols('categoria', 'RAM'))