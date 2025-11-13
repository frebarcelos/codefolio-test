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

class CadastroMaterialExtraTest(unittest.TestCase):

    NOME_CURSO_ALVO = "RF 11,12 e 13 - Cadastro, Edição e Exclusão de Material Extra"
    MATERIAL_TITULO = "Material de Apoio PDF"
    MATERIAL_LINK = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    URL_BASE = "https://testes.codefolio.com.br/"
    FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
    FIREBASE_VALUE = """{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400677093","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1762623423706","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerId":"google.com","uid":"105856292510209699123"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjYyMzUwMSwidXNlcl9pZCI6Ik92S09rWUNLMmVUN3huM1FjUVRZblpTYjFSMzMiLCJzdWIiOiJPdktPa1lDSzJlVDd4bjNRY1FUWW5aU2IxUjMzIiwiaWF0IjoxNzYyNjczOTkwLCJleHAiOjE3NjI2Nzc1OTAsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm9jSmlkZXIiOiJnb29nbGUuY29tIn19.a-W_CUqU0ZP81ZpURu49b6cBrClWk0nqcraFGw47ktTuK3mqtIovg_dqmbZ7s5GghCdk6_twFA6ihdPuFbyLpCX8PZLAIcyQFQBeVQ11ql3oCDeGiQogXKw-sM5TIIix4gTgsS7IXhr6uNbkFCysLUSuA8H-bp10VsiU7R8fHz0BQTj0qExL6SCqCw05F76HXBuzxwyknYj1FeX53jGFdOmAhbHl9eHAhSkl7pBmkLBFkHqW9FXW1ttDGtg4Vh9UD_Inb432gglN-ZBPHy2ukSSrTOex430IDjJTdfZOhRe-jhscMnfLYWRS-9B1Y-dF7r-SJcW1_PTdCVuhYOhh0A","expirationTime":1762677590230,"refreshToken":"AMf-vBzmGoli8pLckXIHEHFjBsq9tdclxZJyoH1JbcdFrcPLRxGaM1rX9B8XHnnJ_XN05JfnkqyH5bYKdBmFud2NNZehSZM4mSXlBQU5HTmmV4vCyBk6T76D7ne-jyrdpzFvhApdJyMx-vyjhqUzyv2uMVdTxfj-pb6kZXAGW_a9tW7q0OA9CJ_KF1eGqx3DcSemtemLSxyxNo0A3gXeMMADVdpIgH8KmQbcFVfqEgr2Lh4C11_njx-Myfov2byzlZpc1zCivD1xCX5LLoEOgcCWMCp8_BEeHtwLeFGRS4DDxxpPH2-WcGpLJINOxCbUFQYeCfVT0bzzGjPgBKA28TQTmv7T0x8uCVBTUHNoVwpmpt9zFqO4QncobWpTnVT4ns7eQyRlBBNdTjSc9133whnn9bT3Wzfar0U2zh9VgFzjftgpgSx3UCNzJkCTvmicr38knaKKfpxGP6dDdqG4Ohjf_Ji9mPxzQw"},"tenantId":null,"uid":"OvKOkYCK2eT7xn3QcQTYnZSb1R33","_redirectEventId":null}"""

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        
        # Configura a pasta para RF11-CT01
        self.EVIDENCE_DIR = "Bernardo-Dorneles/img/RF11-CT01/"
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

    def test_cadastro_material_extra_rf11(self):
        """CT-01 - Cadastro de Material Extra (RF11)"""
        print(f"\n=== INICIANDO CT-01 - CADASTRO DE MATERIAL EXTRA ===")
        cadastrado = False
        
        try:
            self.navegar_para_gerenciamento_cursos()
            
            if not self.selecionar_curso_especifico(self.NOME_CURSO_ALVO):
                self.fail(f"Curso '{self.NOME_CURSO_ALVO}' não encontrado.")
            
            self.navegar_para_aba_materiais()
            
            # Preenche diretamente os campos e clica no botão
            self.preencher_e_adicionar_material()
            
            self.fechar_modal_sucesso()
            
            cadastrado = self.verificar_material_na_lista(self.MATERIAL_TITULO)
            
        except Exception as e:
            print(f"FALHA NO TESTE: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_fatal_rf11.png")
            self.fail(f"Erro: {e}")
            
        self.assertTrue(cadastrado, "FALHA NO ASSERT: O material extra não foi encontrado na lista após o cadastro.")
        print("CT-01 (RF11) - CADASTRO CONCLUÍDO COM SUCESSO!")

    # --- MÉTODOS AUXILIARES ---

    def navegar_para_gerenciamento_cursos(self):
        print("Navegando para Gerenciamento...")
        profile_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
        self.driver.execute_script("arguments[0].click();", profile_btn)
        
        menu_item = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")))
        menu_item.click()
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
        except:
            return False

    def navegar_para_aba_materiais(self):
        print("Abrindo aba Materiais Extras...")
        time.sleep(2)
        seletores = ["//*[contains(text(), 'MATERIAIS')]", "//*[contains(text(), 'Materiais')]", "//button[contains(., 'Materiais')]"]
        for seletor in seletores:
            try:
                aba = self.wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
                aba.click()
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                return
            except: continue
        raise Exception("Aba Materiais Extras não encontrada")

    def preencher_e_adicionar_material(self):
        print("Preenchendo formulário...")
        time.sleep(2) # Espera os campos carregarem
        
        print("Evidência 1: Formulário Vazio")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_01_antes_preencher.png")
        
        try:
            # --- ESTRATÉGIA ROBUSTA PARA ENCONTRAR OS CAMPOS ---
            # Tenta encontrar 'Nome do Material' por placeholder OU por label
            campo_nome = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//input[@placeholder='Nome do Material'] | //label[contains(., 'Nome do Material')]/following-sibling::div//input"
            )))
            campo_nome.clear()
            campo_nome.send_keys(self.MATERIAL_TITULO)
            
            # Tenta encontrar 'URL do Material' por placeholder OU por label
            campo_url = self.driver.find_element(By.XPATH, "//input[@placeholder='URL do Material'] | //label[contains(., 'URL do Material')]/following-sibling::div//input")
            campo_url.clear()
            campo_url.send_keys(self.MATERIAL_LINK)
            
            time.sleep(1)
            print("Evidência 2: Formulário Preenchido")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_02_preenchido.png")
            
            # Botão Roxo "ADICIONAR MATERIAL"
            print("Clicando em ADICIONAR MATERIAL...")
            btn_adicionar = self.driver.find_element(By.XPATH, "//button[contains(text(), 'ADICIONAR MATERIAL') or contains(text(), 'Adicionar Material')]")
            self.driver.execute_script("arguments[0].click();", btn_adicionar)
            
            time.sleep(3) # Espera salvar
            
        except Exception as e:
            print(f"Erro ao interagir com o formulário: {e}")
            raise

    def fechar_modal_sucesso(self):
        # Fecha popup se aparecer (Ok, Sucesso, Fechar)
        try:
            btn_ok = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok') or contains(., 'Fechar')]")))
            btn_ok.click()
            time.sleep(1)
        except: pass

    def verificar_material_na_lista(self, titulo):
        print(f"Verificando se '{titulo}' está na lista...")
        time.sleep(2)
        
        print("Evidência 3: Após Cadastro")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_03_apos_cadastro.png")
        
        # Procura pelo texto na área de materiais adicionados
        try:
            self.driver.find_element(By.XPATH, f"//*[contains(text(), '{titulo}')]")
            return True
        except:
            return False

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()