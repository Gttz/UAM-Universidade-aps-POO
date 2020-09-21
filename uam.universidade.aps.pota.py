import PyQt5
import sys, sqlite3, os
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QLabel, QLineEdit, QPushButton, QHBoxLayout, QRadioButton, \
    QScrollArea, QTabWidget, QVBoxLayout, QMenuBar, QMessageBox, QAction, QListWidget, QMainWindow, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtCore import QCoreApplication, QRect, QTime, QDate


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle('Banco UAM')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(480, 225, 400, 300)
        self.Menu()
        self.Tabs()
        self.conn = sqlite3.connect("Conta_UAM.db")
        self.csr = self.conn.cursor()
        self.csr.execute("""CREATE TABLE IF NOT EXISTS contas(
        				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        				nome VARCHAR(100) NOT NULL,
        				endereco VARCHAR(50) NOT NULL,
        				fone VARCHAR(11) NOT NULL,
        				CPF VARCHAR(11) NOT NULL,
        				num_conta CHAR(3) NOT NULL,
        				saldo VARCHAR(15) NOT NULL,
        				tipo_conta VARCHAR(8) NOT NULL,
        				limite VARCHAR(15) NOT NULL);
        			""")
        self.show()

    def Tabs(self):
        self.tabwidget = QTabWidget()
        self.setCentralWidget(self.tabwidget)
        self.tabwidget.addTab(TabCadastro(), 'Cadastro')
        self.tabwidget.addTab(TabConsulta(), 'Consulta')
        self.tabwidget.addTab(TabMovimentacao(), 'Movimentação')

    def Menu(self):
        mainMenu = self.menuBar()

        InfoMenu = mainMenu.addMenu('Informações')
        ButtonInfo = QAction(QIcon('info.jpg'), 'Créditos', self)

        ButtonInfo.setShortcut('Ctrl+A')
        ButtonInfo.triggered.connect(self.creditos_clicked)
        InfoMenu.addAction(ButtonInfo)

        SairMenu = mainMenu.addMenu('Outros')
        ButtonSair = QAction(QIcon("icon.sair.png"), 'Sair', self)
        ButtonSair.setShortcut('Ctrl+E')
        ButtonSair.triggered.connect(self.close)
        SairMenu.addAction(ButtonSair)

    def creditos_clicked(self):
        QMessageBox.information(self, 'Creditos',
                                'Criador: Lucas Araújo\nCurso: Ciências da Computação\nMatéria: POO, '
                                '2º Semestre\nProfessora: Regiane Marucci',
                                QMessageBox.Ok)


class TabCadastro(QWidget):
    def __init__(self):
        super().__init__()
        self.labels()
        self.text_fields()
        self.buttons()

    def labels(self):
        self.label_nome = QLabel(self)
        self.label_nome.setText('Nome:')
        self.label_nome.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_nome.move(2, 25)
        self.label_nome.resize(100, 20)

        self.label_endereco = QLabel(self)
        self.label_endereco.setText('Endereço:')
        self.label_endereco.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_endereco.move(2, 50)
        self.label_endereco.resize(100, 20)

        self.label_telefone = QLabel(self)
        self.label_telefone.setText('Telefone:')
        self.label_telefone.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_telefone.move(2, 75)
        self.label_telefone.resize(100, 20)

        self.label_cpf = QLabel(self)
        self.label_cpf.setText('CPF:')
        self.label_cpf.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_cpf.move(2, 100)
        self.label_cpf.resize(100, 20)

        self.label_nconta = QLabel(self)
        self.label_nconta.setText('Nº da Conta:')
        self.label_nconta.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_nconta.move(2, 125)
        self.label_nconta.resize(100, 20)

        self.label_imagem = QLabel(self)
        self.label_imagem.setPixmap(QPixmap('logotipo.png'))
        self.label_imagem.move(215, 20)
        self.label_imagem.resize(175, 175)

    def text_fields(self):
        self.field_Nome = QLineEdit(self)
        self.field_Nome.move(100, 25)
        self.field_Nome.resize(87, 20)

        self.field_Endereco = QLineEdit(self)
        self.field_Endereco.move(100, 50)
        self.field_Endereco.resize(87, 20)

        self.field_Telefone = QLineEdit(self)
        self.field_Telefone.setInputMask('(##)#####-####')
        self.field_Telefone.move(100, 75)
        self.field_Telefone.resize(87, 20)

        self.field_cpf = QLineEdit(self)
        self.field_cpf.setInputMask('###.###.###-##')
        self.field_cpf.move(100, 100)
        self.field_cpf.resize(87, 20)

        self.field_nConta = QLineEdit(self)
        self.field_nConta.setInputMask('###')
        self.field_nConta.move(100, 125)
        self.field_nConta.resize(87, 20)

        hboxlayout = QHBoxLayout()

        self.radioContaSimples = QRadioButton('Conta Simples', self)
        self.radioContaSimples.setStyleSheet('QRadioButton {font:bold;font-size:20;color:"Black"}')
        self.radioContaSimples.move(2, 150)
        self.radioContaSimples.resize(120, 20)
        hboxlayout.addWidget(self.radioContaSimples)

        self.radioContaEspecial = QRadioButton('Conta Especial', self)
        self.radioContaEspecial.setStyleSheet('QRadioButton {font:bold;font-size:20;color:"#Black"}')
        self.radioContaEspecial.move(2, 172)
        self.radioContaEspecial.resize(120, 20)
        hboxlayout.addWidget(self.radioContaEspecial)

    def buttons(self):
        self.Button_Cadastrar = QPushButton('Cadastrar', self)
        self.Button_Cadastrar.move(150, 225)
        self.Button_Cadastrar.resize(87, 20)
        self.Button_Cadastrar.clicked.connect(self.cadastrar_clicked)

    def cadastrar_clicked(self):
        self.conn = sqlite3.connect("Conta_UAM.db")
        self.csr = self.conn.cursor()
        self.csr.execute("SELECT num_conta FROM contas")
        lista_contas = self.csr.fetchall()
        lista = [list(lista_contas[x]) for x in range(len(lista_contas))]
        rows = [lista[x][0] for x in range(len(lista))]

        if self.field_Nome.text() == '' or self.field_Endereco.text() == '' or self.field_Telefone.text() == '' \
                or self.field_cpf.text() == '' or self.field_nConta.text() == '':
            erro = QMessageBox()
            erro.setWindowTitle('Erro!')
            erro.setText('Tem algo faltando no seu cadastro!')
            erro.setIcon(QMessageBox.Critical)
            x = erro.exec_()
        elif self.field_nConta.text() in rows:
            erro = QMessageBox()
            erro.setWindowTitle('Erro!')
            erro.setText('Este número de conta já existe !')
            erro.setIcon(QMessageBox.Critical)
            x = erro.exec_()

        elif self.radioContaSimples.isChecked() == False and self.radioContaEspecial.isChecked() == False:
            erro = QMessageBox()
            erro.setWindowTitle('Erro!')
            erro.setText('Selecione o tipo de conta!')
            erro.setIcon(QMessageBox.Critical)
            x = erro.exec_()
        else:
            self.sucesso()

    def sucesso(self):
        nome = self.field_Nome.text()
        endereco = self.field_Endereco.text()
        fone = self.field_Telefone.text()
        cpf = self.field_cpf.text()
        num_conta = self.field_nConta.text()
        if self.radioContaSimples.isChecked():
            tipo_conta = self.radioContaSimples.text()
            limite = 0
            saldo = limite
        elif self.radioContaEspecial.isChecked():
            tipo_conta = self.radioContaEspecial.text()
            limite = 500
            saldo = 0

        try:
            self.conn = sqlite3.connect("Conta_UAM.db")
            self.csr = self.conn.cursor()
            self.csr.execute("""
        		INSERT INTO contas (nome, endereco, fone, cpf, num_conta, saldo, tipo_conta, limite)
        		VALUES (?,?,?,?,?,?,?,?)
        		""", (nome, endereco, fone, cpf, num_conta, saldo, tipo_conta, limite))
            self.conn.commit()
        except Exception as e:
            self.errors(e)

        Cadastrado = QMessageBox()
        Cadastrado.setWindowTitle('Cadastro Concluido!')
        Cadastrado.setText('Conta cadastrada com sucesso!')
        Cadastrado.setIcon(QMessageBox.Information)
        x = Cadastrado.exec_()
        self.field_Nome.clear()
        self.field_Endereco.clear()
        self.field_Telefone.clear()
        self.field_cpf.clear()
        self.field_nConta.clear()
        self.radioContaSimples.setChecked(False)
        self.radioContaEspecial.setChecked(False)

    def errors(self, e):
        hora = QTime.currentTime()
        hr_err = hora.toString("hh:mm:ss")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"{hr_err} \n{e} \n{exc_type} \n{fname} \n{exc_tb.tb_lineno} \n"
        print(err)


class TabConsulta(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.tabCad = TabCadastro()
        self.Components()
        self.conn = sqlite3.connect("Conta_UAM.db")
        self.csr = self.conn.cursor()
        self.setLayout(self.vbox)

    def Components(self):
        self.table = QTableWidget()
        self.vbox1 = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.lab_result = QLabel()

        self.label_nconta = QLabel(self)
        self.label_nconta.setText('Nº da Conta:')
        self.label_nconta.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')

        self.field_nConta = QLineEdit(self)
        self.field_nConta.setInputMask('###')
        self.field_nConta.returnPressed.connect(self.showSearch)

        self.button_Buscar = QPushButton('Buscar por Número', self)
        self.button_Buscar.clicked.connect(self.buttonbuscar_clicked)

        self.button_Listar = QPushButton('Listar todos', self)
        self.button_Listar.clicked.connect(self.buttonListar_clicked)

        self.button_Update = QPushButton('Atualizar tabela', self)
        self.button_Update.clicked.connect(self.showTable)

        self.vbox1.addWidget(self.table)
        self.hbox1.addWidget(self.label_nconta)
        self.hbox1.addWidget(self.field_nConta)
        self.hbox1.addWidget(self.button_Buscar)
        self.hbox1.addWidget(self.button_Listar)
        self.hbox1.addWidget(self.button_Update)
        self.vbox.addLayout(self.vbox1)
        self.vbox.addLayout(self.hbox1)
        self.label_nconta.hide()
        self.field_nConta.hide()
        self.button_Update.hide()

    def showTable(self):
        try:
            self.conn = sqlite3.connect("Conta_UAM.db")
            self.csr = self.conn.cursor()
            self.csr.execute("SELECT * FROM contas")
            ls = self.csr.fetchall()
            rows = [list(ls[x]) for x in range(len(ls))]

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(
                ("ID", "NOME", "ENDEREÇO", "FONE", "CPF", "CONTA", "TIPO", "SALDO", "LIMITE"))
            self.table.setVerticalHeaderLabels(("",) * len(rows))
            for x in range(len(rows)):
                self.table.setItem(x, 0, QTableWidgetItem(str(rows[x][0])))
                self.table.setItem(x, 1, QTableWidgetItem(rows[x][1]))
                self.table.setItem(x, 2, QTableWidgetItem(rows[x][2]))
                self.table.setItem(x, 3, QTableWidgetItem(rows[x][3]))
                self.table.setItem(x, 4, QTableWidgetItem(rows[x][4]))
                self.table.setItem(x, 5, QTableWidgetItem(rows[x][5]))
                self.table.setItem(x, 6, QTableWidgetItem(rows[x][7]))
                self.table.setItem(x, 7, QTableWidgetItem(rows[x][6]))
                self.table.setItem(x, 8, QTableWidgetItem(rows[x][8]))
                self.table.setColumnWidth(0, 20)
                self.table.setColumnWidth(1, 250)
                self.table.setColumnWidth(2, 150)
                self.table.setColumnWidth(3, 100)
                self.table.setColumnWidth(4, 100)
                self.table.setColumnWidth(5, 50)
                self.table.setColumnWidth(7, 50)
                self.table.setColumnWidth(6, 95)
                self.table.setColumnWidth(8, 50)
        except Exception as e:
            self.errors(e)

    def buttonListar_clicked(self):
        self.showTable()
        self.lab_result.hide()
        self.table.show()
        self.label_nconta.hide()
        self.field_nConta.hide()
        self.button_Buscar.show()
        self.button_Listar.hide()
        self.button_Update.show()

    def buttonbuscar_clicked(self):
        self.table.hide()
        self.lab_result.setText("")
        self.label_nconta.show()
        self.field_nConta.show()
        self.button_Buscar.hide()
        self.button_Listar.show()
        self.button_Update.hide()

    def showSearch(self):
        nConta = self.field_nConta.text()
        ce = self.tabCad.radioContaEspecial.text()
        self.field_nConta.clear()
        self.lab_result.show()
        try:
            self.conn = sqlite3.connect("Conta_UAM.db")
            self.csr = self.conn.cursor()
            self.csr.execute(f"SELECT * FROM contas WHERE num_conta = '{nConta}'")
            ls = self.csr.fetchall()
            rows = [list(ls[x]) for x in range(len(ls))]
            if rows[0][7] == ce:
                self.lab_result.setText(
                    f"Nome: {rows[0][1]} \nEndereço: {rows[0][2]} \nFone: {rows[0][3]} \nCPF: {rows[0][4]} \nNº conta: {rows[0][5]} \nTipo: {rows[0][7]} \nSaldo: {rows[0][6]} \nLimite: {rows[0][8]}")
                self.lab_result.setFont(QFont('Sanserif', 12, QFont.Bold))
                self.lab_result.setStyleSheet("color: 'darkblue'")
            else:
                self.lab_result.setText(
                    f"Nome: {rows[0][1]} \nEndereço: {rows[0][2]} \nFone: {rows[0][3]} \nCPF: {rows[0][4]} \nNº conta: {rows[0][5]} \nTipo: {rows[0][7]} \nSaldo: {rows[0][6]}")
                self.lab_result.setFont(QFont('Sanserif', 12, QFont.Bold))
                self.lab_result.setStyleSheet("color: 'darkblue'")
        except Exception as e:
            self.errors(e)
            self.lab_result.setText("CONTA INEXISTENTE.")
            self.lab_result.setFont(QFont('Sanserif', 16, QFont.Bold))
            self.lab_result.setStyleSheet("color: 'red'")

        self.vbox1.addWidget(self.lab_result)
        self.hbox1.addWidget(self.label_nconta)
        self.hbox1.addWidget(self.field_nConta)
        self.hbox1.addWidget(self.button_Listar)

    def errors(self, e):
        hora = QTime.currentTime()
        hr_err = hora.toString("hh:mm:ss")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"{hr_err} \n{e} \n{exc_type} \n{fname} \n{exc_tb.tb_lineno} \n"
        print(err)


class TabMovimentacao(QWidget):
    def __init__(self):
        super().__init__()
        self.tabCad = TabCadastro()
        self.Components()
        self.conn = sqlite3.connect("Conta_UAM.db")
        self.csr = self.conn.cursor()

    def Components(self):
        self.label_nconta = QLabel(self)
        self.label_nconta.setText('Nº da Conta:')
        self.label_nconta.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_nconta.move(2, 0)
        self.label_nconta.resize(100, 20)

        self.field_nConta = QLineEdit(self)
        self.field_nConta.setInputMask('###')
        self.field_nConta.move(2, 25)
        self.field_nConta.resize(87, 20)

        self.label_quantia = QLabel(self)
        self.label_quantia.setText('Quantia:')
        self.label_quantia.setStyleSheet('QLabel {font:bold;font-size:20;color:"Black"}')
        self.label_quantia.move(2, 50)
        self.label_quantia.resize(100, 20)

        self.field_Quantia = QLineEdit(self)
        self.field_Quantia.setInputMask('#############')
        self.field_Quantia.move(2, 75)
        self.field_Quantia.resize(87, 20)

        self.button_Sacar = QPushButton('Sacar', self)
        self.button_Sacar.move(125, 200)
        self.button_Sacar.resize(125, 20)
        self.button_Sacar.clicked.connect(self.buttonSacar_clicked)

        self.button_Depositar = QPushButton('Depositar', self)
        self.button_Depositar.move(125, 225)
        self.button_Depositar.resize(125, 20)
        self.button_Depositar.clicked.connect(self.buttonDepositar_clicked)

        self.label_imagem = QLabel(self)
        self.label_imagem.setPixmap(QPixmap('movimentacao.png'))
        self.label_imagem.move(210, 10)
        self.label_imagem.resize(175, 175)

    def buttonSacar_clicked(self):
        nConta = self.field_nConta.text()
        qnt = self.field_Quantia.text()
        ce = self.tabCad.radioContaEspecial.text()
        cs = self.tabCad.radioContaSimples.text()
        try:
            self.conn = sqlite3.connect("Conta_UAM.db")
            self.csr = self.conn.cursor()
            self.csr.execute(f"SELECT saldo,tipo_conta,limite FROM contas WHERE num_conta = '{nConta}'")
            ls = self.csr.fetchone()
            saldo = float(ls[0])
            limite = float(ls[2])
            sl = saldo + limite

            if (ls[1] == ce) and (float(qnt) > 0.0) and (float(qnt) <= sl):
                if (limite >= float(qnt)) and (saldo == 0.0):
                    limite -= float(qnt)
                    saldo = 0.0
                if (limite < float(qnt)) and (saldo < float(qnt)) and (sl >= float(qnt)):
                    sl -= float(qnt)
                    limite = sl
                    saldo = 0.0
                if (saldo >= float(qnt)) and (limite == 500.0):
                    limite = 500.0
                    saldo -= float(qnt)
                QMessageBox.information(self, 'Saque concluído', 'Saque realizado com sucesso!', QMessageBox.Ok)
                self.csr.execute("""UPDATE contas SET saldo = ?, limite = ? WHERE num_conta = ?""",
                                 (saldo, limite, nConta))
                self.conn.commit()
                self.field_nConta.clear()
                self.field_Quantia.clear()
            elif ls[1] == cs and float(qnt) >= 0 and saldo >= float(qnt):
                saldo -= float(qnt)
                QMessageBox.information(self, 'Saque concluído', 'Saque realizado com sucesso!', QMessageBox.Ok)
                self.csr.execute("""UPDATE contas SET saldo = ? WHERE num_conta = ?""", (saldo, nConta))
                self.conn.commit()
                self.field_nConta.clear()
                self.field_Quantia.clear()
            else:
                QMessageBox.information(self, 'Falha na operação', 'Saldo insuficiente', QMessageBox.Ok)
        except Exception as e:
            self.errors(e)

    def buttonDepositar_clicked(self):
        nConta = self.field_nConta.text()
        qnt = self.field_Quantia.text()
        ce = self.tabCad.radioContaEspecial.text()
        cs = self.tabCad.radioContaSimples.text()
        try:
            self.conn = sqlite3.connect("Conta_UAM.db")
            self.csr = self.conn.cursor()
            self.csr.execute(f"SELECT saldo,tipo_conta,limite FROM contas WHERE num_conta = '{nConta}'")
            ls = self.csr.fetchone()
            saldo = float(ls[0])
            limite = float(ls[2])
            if (ls[1] == ce):
                saldo += float(qnt)
                while (limite != 500.0) and (saldo != 0.0):
                    limite += 1.0
                    saldo -= 1.0
                    if (limite == 500.0) or (saldo == 0.0):
                        break
                QMessageBox.information(self, 'Depósito concluído', 'Depósito realizado com sucesso!', QMessageBox.Ok)
                self.csr.execute("""UPDATE contas SET saldo = ?, limite = ? WHERE num_conta = ?""",
                                 (saldo, limite, nConta))
                self.conn.commit()
                self.field_nConta.clear()
                self.field_Quantia.clear()
            elif (ls[1] == cs) and (float(qnt) >= 0):
                saldo += float(qnt)
                QMessageBox.information(self, 'Depósito concluído', 'Depósito realizado com sucesso!', QMessageBox.Ok)
                self.csr.execute("""UPDATE contas SET saldo = ? WHERE num_conta = ?""", (saldo, nConta))
                self.conn.commit()
                self.field_nConta.clear()
                self.field_Quantia.clear()
            else:
                QMessageBox.information(self, 'Falha na operação', 'Verifique o valor digitado e tente novamente.',
                                        QMessageBox.Ok)
        except Exception as e:
            self.errors(e)

    def errors(self, e):
        hora = QTime.currentTime()
        hr_err = hora.toString("hh:mm:ss")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"{hr_err} \n{e} \n{exc_type} \n{fname} \n{exc_tb.tb_lineno} \n"
        print(err)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
