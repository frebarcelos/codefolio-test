import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class CadastroQuizTest(unittest.TestCase):

    NOME_CURSO_ALVO = "RF 14, 15 e 16 Criação, edição e exclusão de Quiz"
    PERGUNTA = "O Git e o GitHub são a mesma coisa?"
    OPCAO_1 = "Sim, são nomes diferentes para o mesmo programa."
    OPCAO_2 = "Não, o Git é a ferramenta e o GitHub é a plataforma na nuvem." 
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
    FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438261679","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763590598431","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"providerId":"google.com","uid":"105856292510209699123","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6MTc2MzU5MDU5OCwidXNlcl9pZCI6Ijh6VmJ0WWxFVlpib1hYd1ZOWDZlSTNaaGV6dDIiLCJzdWIiOiI4elZidFlsRVZaYm9YWHdWTlg2ZUkzWmhlenQyIiwiaWF0IjoxNzYzNzQ3ODc0LCJleHAiOjE3NjM3NTE0NzQsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.1_SGXCVUdDP77of1Dq17sjvr7oaFB6LrHwNkcdBOli0utPUxHz4rvKETnThcPV8sVk2GJtdUxFJhNNvcXfnyxzTUYQHe6AHAfpyljkW80lHdGIv5_BFnTVXd9uhwR1LjSiqYYxdsIMlDeCahaBk99rsa2hOS4dDQL6rxveO2NGsB9_BT6kjbZphSFywugTZbj_4g9fMixxuBdCEbmlsnq0R9vk3PiwBHLAdeV5it9lZ3LXLCAAER80ZyN_e-726sxvxFqsUTcnqMABCafVTMBuD8lvMrWtQ-7IenkdpCdnVWdC4H5Zd9foO1HUoB94wstIti1tjZZ5HcTiFkuaCYGQ","expirationTime":1763751478217,"refreshToken":"AMf-vBwFZCN9xYE7fhB3CnOkT90ir-eR9pNGK5RSVLJmnrmUHvxjcEj7UTVeD7SMl18v0GHpLgu8wgTbXnmz7X_4BCJYwvSqvH0AXUamMm16ljveuxBjFRp0EgoUjJf5g5l-ffuoHbaF-l5zbkWhMJX-uKXFp8jwAmtJxQg8VI6URceVe5fBQsoigbAzaEsiWYjyTLzruDSfCkC-de4uaapxSIL-Kg4bHPL4jgfGacHWICwZK-64IgrmFzmkaiN0DbxdyJlSO0T5sxF-HpHPld8QMeEfj0xklXmDYjLR3K_RE16-XkuHkePIFGum5EWAQpAjLvvW4sEBgRa_7jFn7wuXM_vgjlHYnUgRfHOwmLwpgJj02HUpTSPHSdr8Kcqe8EHPi4qgW0GkGThfrwZBIYjx69jahYlnPanHCCwPFRNol7f5aSbzT8cjE6eEAnSuGRMyHx0W-3UVkCP-rCV6bp0tBNHji6Ib6A"},"tenantId":null,"uid":"8zVbtYlEVZboXXwVNX6eI3Zhezt2","_redirectEventId":null}"""

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        
        self.EVIDENCE_DIR = "Bernardo-Dorneles/img/RF14-CT01/"
        os.makedirs(self.EVIDENCE_DIR, exist_ok=True)
        
        self.configurar_autenticacao()

    def configurar_autenticacao(self):
        self.driver.get(self.URL_BASE)
        try:
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", self.FIREBASE_KEY, self.FIREBASE_VALUE)
        except Exception as e:
            self.driver.quit()
            raise
        self.driver.refresh()
        time.sleep(3)

    def test_cadastro_quiz_rf14(self):
        print(f"\n=== INICIANDO CT-01 - CADASTRO DE QUIZ (RF14) ===")
        sucesso = False
        
        try:
            self.navegar_para_gerenciamento_cursos()
            if not self.selecionar_curso_especifico(self.NOME_CURSO_ALVO):
                self.fail(f"Curso '{self.NOME_CURSO_ALVO}' não encontrado.")
            self.navegar_para_aba_quiz()
            self.adicionar_quiz_inicial()
            self.expandir_quiz_criado()
            self.clicar_adicionar_questao()
            self.preencher_formulario_questao()
            self.salvar_questao()
            self.fechar_modal_sucesso()
            sucesso = self.verificar_pergunta_na_lista(self.PERGUNTA)
            
        except Exception as e:
            print(f"FALHA NO TESTE: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_fatal_rf14.png")
            self.fail(f"Erro: {e}")
            
        self.assertTrue(sucesso, "FALHA NO ASSERT: A pergunta não foi encontrada na lista do quiz.")
        print("CT-01 (RF14) - CADASTRO DE QUIZ CONCLUÍDO COM SUCESSO!")


    def navegar_para_gerenciamento_cursos(self):
        print("Navegando para Gerenciamento...")
        profile_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
        self.driver.execute_script("arguments[0].click();", profile_btn)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']"))).click()
        self.wait.until(EC.url_contains("/manage-courses"))

    def selecionar_curso_especifico(self, nome_curso):
        print(f"Procurando curso: '{nome_curso}'...")
        time.sleep(2)
        try:
            xpath_botao = f"//*[contains(text(), '{nome_curso}')]/following::button[contains(., 'Gerenciar Curso')][1]"
            botao = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            time.sleep(1)
            botao.click()
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return True
        except: return False

    def navegar_para_aba_quiz(self):
        print("Abrindo aba Quiz...")
        time.sleep(2)
        try:
            aba = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'QUIZ') or contains(text(), 'Quiz')]")))
            self.driver.execute_script("arguments[0].click();", aba)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            raise Exception("Aba Quiz não encontrada")

    def adicionar_quiz_inicial(self):
        print("Adicionando Quiz ao vídeo...")
        try:
            btn_add = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'adicionar quiz')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_add)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn_add)
            
            print("Aguardando modal de sucesso...")
            try:
                btn_ok = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(., 'OK')]"
                )))
                btn_ok.click()
                print("Modal fechado com sucesso.")
                time.sleep(2)
            except:
                print("Modal de sucesso intermediário não apareceu ou fechou sozinho.")
            
        except Exception as e:
            print(f"Erro ao adicionar quiz inicial: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_botao_add_quiz.png")
            raise

    def expandir_quiz_criado(self):
        print("Expandindo Quiz (Usando data-testid)...")
        time.sleep(2)
        try:
            seta_svg = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@data-testid='ExpandMoreIcon']"
            )))
            botao_expandir = seta_svg.find_element(By.XPATH, "./parent::*")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_expandir)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", botao_expandir)
            time.sleep(3) 
        except Exception as e:
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_expandir.png")
            raise Exception("Não foi possível expandir o quiz.")

    def clicar_adicionar_questao(self):
        print("Clicando em '+ ADICIONAR QUESTÃO'...")
        time.sleep(1)
        print("Evidência 1: Antes do Cadastro")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_01_antes_cadastro.png")
        try:
            btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'adicionar questão')]"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input")))
        except Exception as e:
            print(f"Erro ao clicar em adicionar questão: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_clique_adicionar_questao.png")
            raise

    def preencher_formulario_questao(self):
        print("Preenchendo formulário da questão...")
        time.sleep(1)
        print("Evidência 2: Formulário Aberto")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_02_formulario.png")
        
        try:
            campo_pergunta = self.driver.find_element(By.XPATH, "//label[contains(., 'Pergunta')]/following-sibling::div//input | //input[@placeholder='Pergunta']")
            campo_pergunta.send_keys(self.PERGUNTA)
            
            input_op1 = self.driver.find_element(By.XPATH, "//label[contains(., 'Opção 1')]/following::input[1]")
            input_op1.send_keys(Keys.CONTROL + "a")
            input_op1.send_keys(Keys.DELETE)
            input_op1.send_keys(self.OPCAO_1)
            
            input_op2 = self.driver.find_element(By.XPATH, "//label[contains(., 'Opção 2')]/following::input[1]")
            input_op2.send_keys(Keys.CONTROL + "a")
            input_op2.send_keys(Keys.DELETE)
            input_op2.send_keys(self.OPCAO_2)
            
            print("Marcando a opção 2 como correta...")
            check_btn = self.driver.find_element(By.XPATH, "//label[contains(., 'Opção 2')]/following::button[1]")
            self.driver.execute_script("arguments[0].click();", check_btn)
            
            time.sleep(1)
            print("Evidência 3: Preenchido")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_03_preenchido.png")
            
        except Exception as e:
            print(f"Erro ao preencher questão: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_preencher_form.png")
            raise

    def salvar_questao(self):
        print("Salvando questão...")
        try:
            btn_salvar = self.driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'salvar questão')]")
            self.driver.execute_script("arguments[0].click();", btn_salvar)
            time.sleep(3)
        except:
            raise Exception("Botão SALVAR QUESTÃO não encontrado")

    def fechar_modal_sucesso(self):
        try:
            btn_ok = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok') or contains(., 'Fechar')]")))
            btn_ok.click()
            time.sleep(1)
        except: pass

    def verificar_pergunta_na_lista(self, texto_pergunta):
        print(f"Verificando se a pergunta '{texto_pergunta[:20]}...' apareceu...")
        time.sleep(2)
        print("Evidência 4: Após Salvar")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_04_apos_salvar.png")
        
        try:
            self.driver.find_element(By.XPATH, f"//*[contains(text(), '{texto_pergunta}')]")
            return True
        except:
            return False

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()