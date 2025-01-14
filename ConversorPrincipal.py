import streamlit as st
import pandas as pd
import io
import os
import datetime
import base64 
# Função para converter imagem em base64
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

logo_path = "logo.png"

if os.path.exists(logo_path):
    logo_base64 = get_base64_image(logo_path)
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" style="width:255px;">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.error("Logo não encontrada. Verifique o caminho do arquivo.")

# Conteúdo da aplicação
#st.title("Bem-vindo à Aplicação")
#st.write("Esta é a sua aplicação com uma logo personalizada!")

# Classe base com métodos comuns
class ClasseBase:
    def __init__(self):
        pass

    def exibir_mensagem_erro(self, mensagem):
        st.error(f"Erro: {mensagem}")

# Classe 1: Conversão baseada na primeira lógica
class Classe1(ClasseBase):
    def formatar_linha(self, linha):
        # Remove espaços em excesso antes e depois do ponto e vírgula
        partes = [parte.strip() for parte in linha.split(';')]

        # Verifica se a linha tem pelo menos 5 campos
        if len(partes) < 4:
            print(f"Linha ignorada (menos de 4 campos): {linha}")
            return None  # Retorna None para linhas mal formatadas ou com menos de 4 campos
        
        # Campo 1 (sem alterações, removendo espaços)
        campo1 = partes[0].strip()
        
        # Campo 2 (primeiros 11 dígitos)
        campo2 = partes[1][:11] 
        
        # Campo 3 (próximos 3 dígitos após os 11 primeiros)
        campo3 = partes[1][12:15]
        
        # Campo 4 (sem alterações)
        campo4 = partes[2].strip()
        
        try:
            # Converte o valor para float, arredonda para 2 casas decimais, e depois converte para string com a vírgula
            valor = f"{round(float(partes[3]), 2):.2f}".replace('.', ',')       
        except ValueError:
            print(f"Valor inválido no campo 4 (não numérico): {partes[3]}")
            return None  # Caso o valor no campo 4 não seja numérico, retorna None
        
        # Junta os campos novamente com o separador ';' e retorna
        return f"{campo1};{campo2};{campo3};{campo4};{valor}"

    def processar_arquivo(self, conteudo):
        linhas = conteudo.split('\n')
        linhas_formatadas = [self.formatar_linha(linha) for linha in linhas if linha.strip()]
        return '\n'.join(linhas_formatadas)


# Classe 2: Conversão baseada na segunda lógica
class Classe2(ClasseBase):
    def formatar_valor_parcela(self, valor):
        valor = valor.replace(",", ".")
        if valor.isdigit():
            valor = str(int(valor) / 100)
        try:
            valor = float(valor)
            valor = f"{valor:.2f}"
        except ValueError:
            valor = "0.00"
        return valor

    def formatar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        return cpf

    def gerar_arquivo_txt(self, dados):
        output = io.StringIO()
        for index, row in dados.iterrows():
            linha = (
                f"{row['matricula'].zfill(10)}"
                f"{row['cpf'].zfill(11)}"
                f"{row['nome'].upper():<50}"
                f"{row['codigo_estabelecimento']:>3}"
                f"{row['orgao']:>3}"
                f"{row['codigo_desconto']:<4}"
                f"{str(row['valor_parcela']).zfill(10)}"
                f"{str(row['prazo_total']).zfill(3)}"
                f"{row['competencia']}"
                f"{row['codigo_operacao']}"
            )
            output.write(linha + '\n')
        return output.getvalue()


# Classe 3: Converter arquivo Excel para arquivo TXT
class Classe3(ClasseBase):
    def formatar_valor_parcela(self, valor):
        valor = valor.replace(",", ".")
        if valor.isdigit():
            valor = str(int(valor) / 100)
        try:
            valor = float(valor)
            valor = f"{valor:.2f}"
        except ValueError:
            valor = "0.00"
        return valor

    def formatar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        return cpf

    def gerar_arquivo_txt(self, dados):
        output = io.StringIO()
        for index, row in dados.iterrows():
            linha = (
                f"{row['matricula'].zfill(13)}"
                f"{row['cpf'].zfill(11)}"
                f"{row['nome'].upper():<50}"
                f"{row['codigo_estabelecimento'].zfill(2)}"
                f"{row['orgao']:>3}"
                f"{row['codigo_desconto']:<4}"
                f"{str(row['valor_parcela']).zfill(10)}"
                f"{row['competencia']}"
                f"{row['codigo_operacao']}"
            )
            output.write(linha + '\n')
        return output.getvalue()
    
class Classe4(ClasseBase):
    def formatar_valor_parcela(self, valor):
        """
        Formata o valor da parcela para o formato correto:
        - Converte ',' para '.'
        - Adiciona zeros à esquerda para totalizar 15 caracteres, incluindo casas decimais (12,2)
        """
        valor = valor.replace(",", ".")
        try:
            valor = float(valor)
            valor_formatado = f"{valor:015.2f}".replace(".", ",")
        except ValueError:
            valor_formatado = "000000000000,00"
        return valor_formatado.zfill(15)

    def formatar_cpf(self, cpf):
        """
        Remove formatações do CPF e adiciona zeros à esquerda se necessário para totalizar 11 caracteres.
        """
        cpf = cpf.replace(".", "").replace("-", "")
        return cpf.zfill(11)

    def gerar_arquivo_txt(self, dados):
        """
        Gera o conteúdo do arquivo TXT no layout esperado:
        - Unidade: 2 caracteres
        - Código de Verba: 3 caracteres
        - Matrícula: 12 caracteres
        - Parcelas Atual: 2 caracteres
        - Total de Parcelas: 2 caracteres
        - Valor da Parcela: 15 caracteres (12 inteiros, 2 decimais)
        - CPF: 11 caracteres
        - Folha Referência: 6 caracteres (MMAAAA)
        """
        output = io.StringIO()
        for index, row in dados.iterrows():
            linha = (
                f"{str(row['unidade']).zfill(2)}"  # Unidade
                f"{str(row['codigo_verba']).zfill(10)}"  # Código de Verba
                f"{str(row['matricula']).zfill(12)}"  # Matrícula
                f"{str(row['parcelas_atual']).zfill(2)}"  # Parcelas Atual
                f"{str(row['total_parcelas']).zfill(2)}"  # Total de Parcelas
                f"{self.formatar_valor_parcela(row['valor_parcela'])}"  # Valor da Parcela
                f"{row['cpf'].zfill(11)}"  # CPF
                f"{str(row['folha_referencia']).zfill(6)}"  # Folha Referência
            )
            output.write(linha + '\n')
        return output.getvalue()
    

# Classe Principal que gerencia as interações
class ClassePrincipal:
    def __init__(self):
        self.opcoes_classes = {
            'SimplesConsig': Classe1(),
            'eConsig': Classe2(),
            'Casa Civil': Classe3(),
            'Consignet' : Classe4()
        }
    def executar(self):
        st.title('📝 Conversor de Arquivos de Lote')

        # Adiciona a seleção da classe na barra lateral
        classe_selecionada = st.sidebar.radio("Escolha o método de conversão:", list(self.opcoes_classes.keys()))
        
        # Exibe o conteúdo correspondente à classe selecionada
        if classe_selecionada == 'SimplesConsig':
            self.interface_classe1()
        elif classe_selecionada == 'eConsig':
            self.interface_classe2()
        elif classe_selecionada == 'Casa Civil':
            self.interface_classe3()
        elif classe_selecionada == 'Consignet':
            self.interface_classe4()

    def interface_classe1(self):
        conversor = self.opcoes_classes['SimplesConsig']
        st.subheader('🔄 Conversão Para SimplesConsig')
        arquivo_txt = st.file_uploader("Selecione o arquivo .txt para conversão", type=['txt'])

        if arquivo_txt is not None:
            conteudo = arquivo_txt.getvalue().decode('utf-8')
            st.text_area("Conteúdo do arquivo de entrada", conteudo, height=200)

            if st.button("Converter Arquivo", key="btn_converter_classe1"):
                try:
                    conteudo_convertido = conversor.processar_arquivo(conteudo)
                    st.text_area("Conteúdo do arquivo convertido", conteudo_convertido, height=200)
                    st.download_button("📥 Baixar Arquivo Convertido", conteudo_convertido, "arquivo_convertido_classe1.txt", "text/plain")
                except Exception as e:
                    conversor.exibir_mensagem_erro(e)

    def interface_classe2(self):
        conversor = self.opcoes_classes['eConsig']
        st.subheader('🆕 Conversão Para eConsig')

        mes_ano_atual = datetime.datetime.now().strftime("%m%Y")

        # Criar uma lista de registros
        if 'dados' not in st.session_state:
            st.session_state['dados'] = []

        # Formulário para adicionar os campos
        with st.form("formulario"):
            matricula = st.text_input('Matrícula (máx. 10 dígitos)', placeholder='Digite a Matrícula')
            cpf = st.text_input('CPF', placeholder='Digite o CPF')
            nome = st.text_input('Nome do Servidor', placeholder='Digite o Nome')
            codigo_desconto = st.text_input('Código de Desconto', placeholder='1234')
            valor_parcela = st.text_input('Valor da Parcela', placeholder='543,21')
            prazo_total = st.text_input('Prazo Total', value='999')
            competencia = st.text_input('Competência (MMAAAA)', value=mes_ano_atual)
            codigo_operacao = st.selectbox('Código de Operação', ['I', 'A', 'E'])

            submit_button = st.form_submit_button('Adicionar Registro')

            if submit_button:
                st.session_state['dados'].append({
                    'matricula': matricula,
                    'cpf': conversor.formatar_cpf(cpf),
                    'nome': nome,
                    'codigo_estabelecimento': '001',
                    'orgao': '001',
                    'codigo_desconto': codigo_desconto,
                    'valor_parcela': conversor.formatar_valor_parcela(valor_parcela),
                    'prazo_total': prazo_total,
                    'competencia': competencia,
                    'codigo_operacao': codigo_operacao
                })
                st.success('✅ Registro adicionado com sucesso!')
                st.session_state['matricula'] = ''
                st.session_state['cpf'] = ''
                st.session_state['nome'] = ''     
                

        # Exibir a tabela de registros adicionados
        if len(st.session_state['dados']) > 0:
            df = pd.DataFrame(st.session_state['dados'])
            st.write('📋 **Registros Adicionados:**')
            st.dataframe(df)

            # **Selecionar registro para editar ou excluir**
            opcoes = [f"Registro {i+1} - {row['nome']}" for i, row in df.iterrows()]
            registro_selecionado = st.selectbox('Selecione um registro para editar ou excluir', options=opcoes)

            # Identificar o índice do registro selecionado
            indice_selecionado = opcoes.index(registro_selecionado)

            # **Botões de excluir, editar e limpar lado a lado**
            col1, col2, col3 = st.columns(3)  # Cria três colunas para os botões ficarem lado a lado

            with col1:
                # **Botão para excluir o registro**
                if st.button('❌ Excluir Registro'):
                    st.session_state['dados'].pop(indice_selecionado)
                    st.success('✅ Registro excluído com sucesso!')
                    st.experimental_rerun()

            with col2:
                # **Botão para editar o registro**
                if st.button('✏️ Editar Registro'):
                    registro = st.session_state['dados'][indice_selecionado]

                    # Formulário para edição do registro
                    with st.form("formulario_edicao"):
                        matricula_edit = st.text_input('Matrícula', value=registro['matricula'])
                        cpf_edit = st.text_input('CPF', value=registro['cpf'])
                        nome_edit = st.text_input('Nome do Servidor', value=registro['nome'])
                        codigo_desconto_edit = st.text_input('Código de Desconto', value=registro['codigo_desconto'])
                        valor_parcela_edit = st.text_input('Valor da Parcela', value=registro['valor_parcela'])
                        prazo_total_edit = st.text_input('Prazo Total', value=registro['prazo_total'])
                        competencia_edit = st.text_input('Competência (MMAAAA)', value=registro['competencia'])
                        codigo_operacao_edit = st.selectbox('Código de Operação', ['I', 'A', 'E'], index=['I', 'A', 'E'].index(registro['codigo_operacao']))

                        salvar_edicao = st.form_submit_button('Salvar Edição')

                        if salvar_edicao:
                            st.session_state['dados'][indice_selecionado] = {
                                'matricula': matricula_edit,
                                'cpf': cpf_edit,
                                'nome': nome_edit,
                                'codigo_estabelecimento': '001',
                                'orgao': '001',
                                'codigo_desconto': codigo_desconto_edit,
                                'valor_parcela': conversor.formatar_valor_parcela(valor_parcela_edit),
                                'prazo_total': prazo_total_edit,
                                'competencia': competencia_edit,
                                'codigo_operacao': codigo_operacao_edit
                            }
                            st.success('✅ Registro editado com sucesso!')
                            st.experimental_rerun()

            with col3:
                # **Botão para limpar todos os registros**
                if st.button('🧹 Limpar Registros'):
                    st.session_state['dados'] = []
                    st.success('✅ Todos os registros foram limpos com sucesso!')
                    st.experimental_rerun()


            # Gerar o conteúdo do arquivo TXT (em memória)
            arquivo_txt = conversor.gerar_arquivo_txt(df)

            # Botão de download para baixar o arquivo TXT
            st.download_button(
                label='📥 Baixar Arquivo TXT',
                data=arquivo_txt,
                file_name='Arqui_confor_Layout.txt',
                mime='text/plain'
            )

    def interface_classe3(self):
        conversor = self.opcoes_classes['Casa Civil']
        st.subheader('🆕 Conversão Para Casa Civil')

        mes_ano_atual = datetime.datetime.now().strftime("%m%Y")

        # Criar uma lista de registros
        if 'dados' not in st.session_state:
            st.session_state['dados'] = []

        # Formulário para adicionar os campos
        with st.form("formulario"):
            matricula = st.text_input('Matrícula (máx. 10 dígitos)', placeholder='Digite a Matrícula')
            cpf = st.text_input('CPF', placeholder='Digite o CPF')
            nome = st.text_input('Nome do Servidor', placeholder='Digite o Nome')
            codigo_desconto = st.text_input('Código de Desconto', placeholder='1234')
            valor_parcela = st.text_input('Valor da Parcela', placeholder='Informe o Valor')
            prazo_total = st.text_input('Prazo Total', value='001')
            competencia = st.text_input('Competência (MMAAAA)', value=mes_ano_atual)
            codigo_operacao = st.selectbox('Código de Operação', ['I', 'A', 'E'])

            submit_button = st.form_submit_button('Adicionar Registro')

            if submit_button:
                st.session_state['dados'].append({
                    'matricula': matricula,
                    'cpf': conversor.formatar_cpf(cpf),
                    'nome': nome,
                    'codigo_estabelecimento': '01',
                    'orgao': '001',
                    'codigo_desconto': codigo_desconto,
                    'valor_parcela': conversor.formatar_valor_parcela(valor_parcela),
                    'prazo_total': prazo_total,
                    'competencia': competencia,
                    'codigo_operacao': codigo_operacao
                })
                st.success('✅ Registro adicionado com sucesso!')
                st.session_state['matricula'] = ''
                st.session_state['cpf'] = ''
                st.session_state['nome'] = ''     


        # Exibir a tabela de registros adicionados
        if len(st.session_state['dados']) > 0:
            df = pd.DataFrame(st.session_state['dados'])
            st.write('📋 **Registros Adicionados:**')
            st.dataframe(df)

            # **Selecionar registro para editar ou excluir**
            opcoes = [f"Registro {i+1} - {row['nome']}" for i, row in df.iterrows()]
            registro_selecionado = st.selectbox('Selecione um registro para editar ou excluir', options=opcoes)

            # Identificar o índice do registro selecionado
            indice_selecionado = opcoes.index(registro_selecionado)

            # **Botões de excluir, editar e limpar lado a lado**
            col1, col2, col3 = st.columns(3)  # Cria três colunas para os botões ficarem lado a lado

            with col1:
                # **Botão para excluir o registro**
                if  st.button('❌ Excluir Registro'):
                    st.session_state['dados'].pop(indice_selecionado)
                    st.success('✅ Registro excluído com sucesso!')
                    st.experimental_rerun()

            with col2:
                # **Botão para editar o registro**
                if st.button('✏️ Editar Registro'):
                    registro = st.session_state['dados'][indice_selecionado]

                    # Formulário para edição do registro
                    with st.form("formulario_edicao"):
                        matricula_edit = st.text_input('Matrícula', value=registro['matricula'])
                        cpf_edit = st.text_input('CPF', value=registro['cpf'])
                        nome_edit = st.text_input('Nome do Servidor', value=registro['nome'])
                        codigo_desconto_edit = st.text_input('Código de Desconto', value=registro['codigo_desconto'])
                        valor_parcela_edit = st.text_input('Valor da Parcela', value=registro['valor_parcela'])
                        prazo_total_edit = st.text_input('Prazo Total', value=registro['prazo_total'])
                        competencia_edit = st.text_input('Competência (MMAAAA)', value=registro['competencia'])
                        codigo_operacao_edit = st.selectbox('Código de Operação', ['I', 'A', 'E'], index=['I', 'A', 'E'].index(registro['codigo_operacao']))

                        salvar_edicao = st.form_submit_button('Salvar Edição')

                        if salvar_edicao:
                            st.session_state['dados'][indice_selecionado] = {
                                'matricula': matricula_edit,
                                'cpf': cpf_edit,
                                'nome': nome_edit,
                                'codigo_estabelecimento': '001',
                                'orgao': '001',
                                'codigo_desconto': codigo_desconto_edit,
                                'valor_parcela': conversor.formatar_valor_parcela(valor_parcela_edit),
                                'prazo_total': prazo_total_edit,
                                'competencia': competencia_edit,
                                'codigo_operacao': codigo_operacao_edit
                            }
                            st.success('✅ Registro editado com sucesso!')
                            st.experimental_rerun()

            with col3:
                # **Botão para limpar todos os registros**
                if  st.button('🧹 Limpar Registros'):
                    st.session_state['dados'] = []
                    st.success('✅ Todos os registros foram limpos com sucesso!')
                    st.experimental_rerun()
                    


            # Gerar o conteúdo do arquivo TXT (em memória)
            arquivo_txt = conversor.gerar_arquivo_txt(df)

            # Botão de download para baixar o arquivo TXT
            st.download_button(
                label='📥 Baixar Arquivo TXT',
                data=arquivo_txt,
                file_name='Arqui_confor_Layout.txt',
                mime='text/plain'
            )

    def interface_classe4(self):
        conversor = self.opcoes_classes['Consignet']  # Atualização para Classe04
        st.subheader('🆕 Conversão Para Consignet')

        mes_ano_atual = datetime.datetime.now().strftime("%m%Y")

        # Criar uma lista de registros
        if 'dados' not in st.session_state:
            st.session_state['dados'] = []

        # Formulário para adicionar os campos
        with st.form("formulario"):
            unidade = st.text_input(
                'Unidade',
                placeholder='Ex.: 01',
                value='01',
                max_chars=2
            )
            codigo_verba = st.text_input(
                'Código da Verba',
                placeholder='Ex.: 001',
                max_chars=3
            )
            matricula = st.text_input(
                'Matrícula do Servidor',
                placeholder='Digite a matrícula',
                max_chars=12
            )
            parcelas_atual = st.text_input(
                'Parcela Atual',
                value='01',
                max_chars=2,
                disabled=True  # Sempre será 01
            )
            total_parcelas = st.text_input(
                'Total de Parcelas',
                value='01',
                max_chars=2,
                disabled=True  # Sempre será 01
            )
            valor_parcela = st.text_input(
                'Valor da Parcela',
                placeholder='000000001000,15',
                max_chars=15
            ) 
            cpf = st.text_input(
                'CPF do Servidor',
                placeholder='00000000000',
                max_chars=11
            )
            folha_referencia = st.text_input(
                'Folha Referência (MMAAAA)',
                value=mes_ano_atual,
                max_chars=6
            )

            submit_button = st.form_submit_button('Adicionar Registro')

            if submit_button:
                # Aplicar formatação com zeros à esquerda
                unidade_formatada = unidade.zfill(2)
                codigo_verba_formatado = codigo_verba.zfill(3)
                matricula_formatada = matricula.zfill(12)
                valor_parcela_formatado = conversor.formatar_valor_parcela(valor_parcela)
                cpf_formatado = cpf.zfill(11)

                st.session_state['dados'].append({
                    'unidade': unidade_formatada,
                    'codigo_verba': codigo_verba_formatado,
                    'matricula': matricula_formatada,
                    'parcelas_atual': '01',
                    'total_parcelas': '01',
                    'valor_parcela': valor_parcela_formatado,
                    'cpf': cpf_formatado,
                    'folha_referencia': folha_referencia
                })
                st.success('✅ Registro adicionado com sucesso!')
                st.rerun()

        # Exibir a tabela de registros adicionados
        if len(st.session_state['dados']) > 0:
            df = pd.DataFrame(st.session_state['dados'])
            st.write('📋 **Registros Adicionados:**')
            st.dataframe(df)

            # Selecionar registro para editar ou excluir
            opcoes = [f"Registro {i + 1} - {row['matricula']}" for i, row in df.iterrows()]
            registro_selecionado = st.selectbox('Selecione um registro para editar ou excluir', options=opcoes)

            indice_selecionado = opcoes.index(registro_selecionado)

            col1, col2, col3 = st.columns(3)

            with col1:
                if  st.button('❌ Excluir Registro'):
                    st.session_state['dados'].pop(indice_selecionado)
                    st.success('✅ Registro excluído com sucesso!')
                    st.rerun()

            with col2:
                if st.button('✏️ Editar Registro'):
                    registro = st.session_state['dados'][indice_selecionado]

                    with st.form("formulario_edicao"):
                        unidade_edit = st.text_input('Unidade', value=registro['unidade'], max_chars=2)
                        codigo_verba_edit = st.text_input('Código da Verba', value=registro['codigo_verba'], max_chars=3)
                        matricula_edit = st.text_input('Matrícula', value=registro['matricula'], max_chars=12)
                        valor_parcela_edit = st.text_input('Valor da Parcela', value=registro['valor_parcela'], max_chars=15)
                        cpf_edit = st.text_input('CPF', value=registro['cpf'], max_chars=11)
                        folha_referencia_edit = st.text_input('Folha Referência', value=registro['folha_referencia'], max_chars=6)

                        salvar_edicao = st.form_submit_button('Salvar Edição')

                        if salvar_edicao:
                            st.session_state['dados'][indice_selecionado] = {
                                'unidade': unidade_edit.zfill(2),
                                'codigo_verba': codigo_verba_edit.zfill(3),
                                'matricula': matricula_edit,
                                'parcelas_atual': '01',
                                'total_parcelas': '01',
                                'valor_parcela': conversor.formatar_valor_parcela(valor_parcela_edit),
                                'cpf': cpf_edit.zfill(11),
                                'folha_referencia': folha_referencia_edit
                            }
                            st.success('✅ Registro editado com sucesso!')
                            st.rerun()

            with col3:
                if  st.button('🧹 Limpar Registros'):
                    st.session_state['dados'] = []
                    st.success('✅ Todos os registros foram limpos com sucesso!')
                    st.rerun()

            # Gerar conteúdo para o arquivo TXT
            arquivo_txt = conversor.gerar_arquivo_txt(df)

            # Botão para download do arquivo TXT
            st.download_button(
                label='📥 Baixar Arquivo TXT',
                data=arquivo_txt,
                file_name='Consignet_Layout.txt',
                mime='text/plain'
            )


# Execução da classe principal
if __name__ == "__main__":
    app = ClassePrincipal()
    app.executar()
