import sqlite3

class base_Dados():
    def __init__(self, db):
        self.db = db
    
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def insert_hardware(self, produto, categoria, link, loja, valor_avista, ultima_att):
        try:
            self.cursor.execute('''
                                    INSERT INTO hardware (produto, categoria, link, loja, valor_avista, ultima_att)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                ''', (produto, categoria, link, loja, valor_avista, ultima_att))
            self.conn.commit()
            return 'OK'
        except NameError as e:
            return f'Erro: {e}'   
    
    def close_conn(self):
        self.conn.close() 




basedata = base_Dados(r'/home/pablopassarini/Projetos/WebScraping/data_base/produtos.db')
print(basedata.insert_hardware('Memória RAM Kingston Fury Beast, 8GB, 3200MHz, DDR4, CL16, Preto - KF432C16BB/8', 'RAM', 'https://www.kabum.com.br/produto/172365/memoria-ram-kingston-fury-beast-8gb-3200mhz-ddr4-cl16-preto-kf432c16bb-8', 'KABUM', '154.99', '18/01/2025'))