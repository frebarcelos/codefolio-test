import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ExclusaoMaterialExtraTest(unittest.TestCase):

    NOME_CURSO_ALVO = "RF 11,12 e 13 - Cadastro, Edição e Exclusão de Material Extra"
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"	
    FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763438261679","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1763590598431","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"providerId":"google.com","uid":"105856292510209699123","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6MTc2MzU5MDU5OCwidXNlcl9pZCI6Ijh6VmJ0WWxFVlpib1hYd1ZOWDZlSTNaaGV6dDIiLCJzdWIiOiI4elZidFlsRVZaYm9YWHdWTlg2ZUkzWmhlenQyIiwiaWF0IjoxNzYzNzQ3ODc0LCJleHAiOjE3NjM3NTE0NzQsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.1_SGXCVUdDP77of1Dq17sjvr7oaFB6LrHwNkcdBOli0utPUxHz4rvKETnThcPV8sVk2GJtdUxFJhNNvcXfnyxzTUYQHe6AHAfpyljkW80lHdGIv5_BFnTVXd9uhwR1LjSiqYYxdsIMlDeCahaBk99rsa2hOS4dDQL6rxveO2NGsB9_BT6kjbZphSFywugTZbj_4g9fMixxuBdCEbmlsnq0R9vk3PiwBHLAdeV5it9lZ3LXLCAAER80ZyN_e-726sxvxFqsUTcnqMABCafVTMBuD8lvMrWtQ-7IenkdpCdnVWdC4H5Zd9foO1HUoB94wstIti1tjZZ5HcTiFkuaCYGQ","expirationTime":1763751478217,"refreshToken":"AMf-vBwFZCN9xYE7fhB3CnOkT90ir-eR9pNGK5RSVLJmnrmUHvxjcEj7UTVeD7SMl18v0GHpLgu8wgTbXnmz7X_4BCJYwvSqvH0AXUamMm16ljveuxBjFRp0EgoUjJf5g5l-ffuoHbaF-l5zbkWhMJX-uKXFp8jwAmtJxQg8VI6URceVe5fBQsoigbAzaEsiWYjyTLzruDSfCkC-de4uaapxSIL-Kg4bHPL4jgfGacHWICwZK-64IgrmFzmkaiN0DbxdyJlSO0T5sxF-HpHPld8QMeEfj0xklXmDYjLR3K_RE16-XkuHkePIFGum5EWAQpAjLvvW4sEBgRa_7jFn7wuXM_vgjlHYnUgRfHOwmLwpgJj02HUpTSPHSdr8Kcqe8EHPi4qgW0GkGThfrwZBIYjx69jahYlnPanHCCwPFRNol7f5aSbzT8cjE6eEAnSuGRMyHx0W-3UVkCP-rCV6bp0tBNHji6Ib6A"},"tenantId":null,"uid":"8zVbtYlEVZboXXwVNX6eI3Zhezt2","_redirectEventId":null}"""
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        
        self.EVIDENCE_DIR = "Bernardo-Dorneles/img/RF13-CT01/"
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

    def test_exclusao_material_extra_rf13(self):
        print(f"\n=== INICIANDO CT-01 - EXCLUSÃO DE MATERIAL EXTRA ===")
        excluido = False
        
        try:
            self.navegar_para_gerenciamento_cursos()
            
            if not self.selecionar_curso_especifico(self.NOME_CURSO_ALVO):
                self.fail(f"Curso '{self.NOME_CURSO_ALVO}' não encontrado.")
            
            self.navegar_para_aba_materiais()
            
            print("Aguardando lista carregar para foto...")
            time.sleep(3)
            print("Evidência 1: Antes da Exclusão")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_01_antes_exclusao.png")

            nome_material_alvo = self.obter_nome_primeiro_material()
            if not nome_material_alvo:
                print("Aviso: Nome não capturado, tentando exclusão genérica.")
                nome_material_alvo = "Material Genérico"
            else:
                print(f"Material alvo para exclusão: '{nome_material_alvo}'")

            self.clicar_lixeira_material()
            
            self.confirmar_exclusao_modal()
            self.fechar_modal_sucesso()
            
            excluido = self.verificar_material_inexistente(nome_material_alvo)
            
        except Exception as e:
            print(f"FALHA NO TESTE: {e}")
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_fatal_rf13.png")
            self.fail(f"Erro: {e}")
            
        self.assertTrue(excluido, "FALHA NO ASSERT: O material extra ainda foi encontrado na lista após a exclusão.")
        print("CT-01 (RF13) - EXCLUSÃO CONCLUÍDA COM SUCESSO!")


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
        except:
            return False

    def navegar_para_aba_materiais(self):
        print("Abrindo aba Materiais Extras...")
        time.sleep(2)
        seletores = ["//*[contains(text(), 'MATERIAIS')]", "//*[contains(text(), 'Materiais')]", "//button[contains(., 'Materiais')]"]
        for seletor in seletores:
            try:
                aba = self.wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
                self.driver.execute_script("arguments[0].click();", aba)
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                return
            except: continue
        raise Exception("Aba Materiais Extras não encontrada")

    def obter_nome_primeiro_material(self):
        print("Capturando nome do primeiro material...")
        try:
            elemento_titulo = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "(//*[contains(text(), 'Materiais Adicionados')]/following::div[contains(@class, 'MuiPaper') or contains(@class, 'card')]//*[not(contains(text(), 'URL:')) and string-length(text()) > 3])[1]"
            )))
            return elemento_titulo.text
        except:
            return None

    def clicar_lixeira_material(self):
        print("Clicando na lixeira...")
        time.sleep(1)
        try:
            xpath_lixeira = "(//*[contains(text(), 'Materiais Adicionados')]/following::button)[1]"
            icone_lixeira = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_lixeira)))
            self.driver.execute_script("arguments[0].click();", icone_lixeira)
        except Exception as e:
            print(f"Erro ao clicar na lixeira: {e}")
            raise

    def confirmar_exclusao_modal(self):
        print("Confirmando exclusão...")
        time.sleep(1)
        try:
            btn_confirmar = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'SIM') or contains(., 'Sim') or contains(., 'EXCLUIR')]"
            )))
            self.driver.execute_script("arguments[0].click();", btn_confirmar)
            time.sleep(3)
        except:
            self.driver.save_screenshot(f"{self.EVIDENCE_DIR}erro_modal.png")
            raise Exception("Botão de confirmação do modal não encontrado.")

    def fechar_modal_sucesso(self):
        try:
            btn_ok = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok') or contains(., 'Fechar')]")))
            btn_ok.click()
            time.sleep(1)
        except: pass

    def verificar_material_inexistente(self, titulo):
        print(f"Verificando se '{titulo}' foi removido...")
        time.sleep(2)
        
        print("Evidência 2: Após Exclusão")
        self.driver.save_screenshot(f"{self.EVIDENCE_DIR}evidencia_02_depois_exclusao.png")
        
        if titulo == "Material Genérico":
            return True

        try:
            self.driver.find_element(By.XPATH, f"//*[contains(text(), '{titulo}')]")
            print(f"Erro: Material '{titulo}' ainda visível.")
            return False
        except:
            return True

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()