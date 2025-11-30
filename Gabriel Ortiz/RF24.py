import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

TIMEOUT = 15
URL_BASE = "https://testes-codefolio.web.app/"

FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
FIREBASE_VALUE = "{\"apiKey\":\"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co\",\"appName\":\"[DEFAULT]\",\"createdAt\":\"1763469119436\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"emailVerified\":true,\"isAnonymous\":false,\"lastLoginAt\":\"1763503704340\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\",\"providerData\":[{\"providerId\":\"google.com\",\"uid\":\"116550479800107608553\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\"}],\"stsTokenManager\":{\"accessToken\":\"eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4MDI5MzRmZTBlZWM0NmE1ZWQwMDA2ZDE0YTFiYWIwMWUzNDUwODMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBDYW1hcmdvIE9ydGl6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0t1U09yMmFvc3E1ZXdZVGtWWm1pY1dwbU03OENyQ2FOV1ZnOFRfTnU0d2s1VTc2dz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6Im5aWkVCQjFOaENZbEpPa3VFVEptdEF1WWtrdTEiLCJzdWIiOiJuWlpFQkIxTmhDWWxKT2t1RVRKbXRBdVlra3UxIiwiaWF0IjoxNzYzNTAzNzA0LCJleHAiOjE3NjM1MDczMDQsImVtYWlsIjoiZ2FicmllbG9ydGl6LmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE2NTUwNDc5ODAwMTA3NjA4NTUzIl0sImVtYWlsIjpbImdhYnJpZWxvcnRpei5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.o709FnowybYLxxFiX__28WWqbbhHX3A9bq9zY0B3OQCoBlr1y32n6eYCklur41jVo2WcW9SmNKREmI4xmQhVEzMGKzlldwri5thZMpxx7HctgtFKYW3fxE9sLEsUIy17g7Bs9MbyihGFsLeqfMkGulFEphE7PUr4N-xNkIefQMtY2yqlQlePihnFQAJI8MBkz0kylZuWfeXARpuiKUaqUsqYLESsQxIK9rMWR7L-zn5eJOSJqNQpp_ktz6lbWWeeTdFn171VX4I21fdn0gEOyzOQ7gvFyO3n-xkvxZCx5XMynGcHCiOAqvUOon6DIoQc_LdQ3dfXyAZUqLLLQWY-Ag\",\"expirationTime\":1763507307329,\"refreshToken\":\"AMf-vByblqLWZmvUW00nxvGTjscnM-1u7jbUCrg7QexqXYOr-4qrRBg2LSds9fH8H5HsgvHvrlpe25bKkcMTdqbggTqLgmvqAIpEDN-jzHEuIYG6i1AN1u36fPCUY-MMaYuRCdyXi37Kf7zECG-xkYZM8S7zPjYPrTX8FnaJOm1NuOUDWtTVvoVyR5poDwHQHETyzzap9c0L7SCq7k7-nRdgjzjxel3QdD3DZkw36ZdyVoVjBHKdJFsh8fNfyGss3NqWkBk7ynWAea7TtdbVRYBmJcT5ZDfnnpfQvIeO6IauiFzw4YfhmNcuJxXYurJQiXfXVQv7pKySG4pAvPy5ORy31Z81Wvrem99psQJql9nOxdPXBEOdn_ZGdBbgQYnYfgf7eVJX56-UQDwbvuetohBnMCWUwHlBqzmbtN6u4BteQm6W4bDjSRTYEaGtOVfI4UcS0Ce_7xCZithCaMA9aJ7UoDUBKAePUg\"},\"tenantId\":null,\"uid\":\"nZZEBB1NhCYlJOkuETJmtAuYkku1\",\"_redirectEventId\":null}"

class TestRF24ExclusaoAvaliacoes(unittest.TestCase):

    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service) 
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        
        self.driver.get(URL_BASE)
        self.driver.execute_script("window.localStorage.clear();")
        try:
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", FIREBASE_KEY, FIREBASE_VALUE)
        except: self.driver.quit(); self.fail("Falha Token")

        self.driver.refresh()
        time.sleep(5) 
        try:
            self.driver.execute_script("document.body.click();")
        except: pass

    def tearDown(self):
        if hasattr(self, 'driver'): self.driver.quit()

    # Metodos de ajuda
    def _navegar_para_gerenciar_curso(self, nome_curso):
        self.driver.get(URL_BASE + "manage-courses")
        self.wait.until(EC.url_contains("/manage-courses"))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Criar Novo Curso']")))
        time.sleep(1) 
        xpath = f"""//h6[normalize-space()='{nome_curso}']/parent::div/following-sibling::div[contains(@class, 'MuiCardActions-root')]//button[normalize-space()='Gerenciar Curso']"""
        self.driver.execute_script("arguments[0].click();", self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[normalize-space()='Gerenciar Curso']")))

    def _clicar_na_aba_avaliacoes(self):
        print("Clicando na aba Avaliações...")
        xpath = "//button[@role='tab' and contains(., 'Avaliações')]"
        aba = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].click();", aba)

    def _lidar_com_modal_sucesso(self):
        try:
            botao_ok = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(), 'OK')]"
            )))
            time.sleep(1) 
            self.driver.execute_script("arguments[0].click();", botao_ok)
            print("Modal fechado com sucesso.")
            time.sleep(1) 
        except:
            print("Aviso: Modal de sucesso não apareceu ou fechou sozinho.")

    def _criar_avaliacao_temporaria(self, nome_temp):
        print(f"Criando avaliação temporária: {nome_temp}...")
        
        xpath_nome = "//label[contains(., 'Nome')]/following-sibling::div//input"
        input_nome = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_nome)))
        input_nome.click()
        input_nome.send_keys(nome_temp)
        
        xpath_peso = "//label[contains(., 'Percentual')]/following-sibling::div//input"
        input_peso = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_peso)))
        input_peso.click()
        input_peso.send_keys("1")
        time.sleep(0.5)
        input_peso.send_keys(Keys.TAB) 
        time.sleep(1)
        
        # Adicionar
        print("Clicando em Adicionar...")
        xpath_add = "//button[contains(., 'Adicionar') or contains(., 'ADICIONAR')]"
        btn_add = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_add)))
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_add)
        time.sleep(1) 
        self.driver.execute_script("arguments[0].click();", btn_add)
        time.sleep(1)
        
        #  Salvar Curso
        print("Salvando temporária...")
        btn_salvar = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Salvar Curso']")))
        self.driver.execute_script("arguments[0].click();", btn_salvar)
    
        self._lidar_com_modal_sucesso()

    # --- TESTE PRINCIPAL 
    def test_rf24_exclusao_avaliacao(self):
        print("\nExecutando RF24: Exclusão de Avaliação (MODO VISUAL)")
        NOME_CURSO = "Curso Python"
        NOME_PARA_EXCLUIR = f"Excluir {int(time.time())}" 

        try:
            self._navegar_para_gerenciar_curso(NOME_CURSO)
            self._clicar_na_aba_avaliacoes()

            self._criar_avaliacao_temporaria(NOME_PARA_EXCLUIR)

    
            print(f"--- INICIANDO EXCLUSÃO DE: {NOME_PARA_EXCLUIR} ---")
            
            tabela = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//table")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tabela)
            time.sleep(1)

            seletor_linha = (By.XPATH, f"//tr[.//td[contains(., '{NOME_PARA_EXCLUIR}')]]")
            linha = self.wait.until(EC.presence_of_element_located(seletor_linha))
            

            print("1. Localizando o botão Lixeira...")
            botao_excluir = linha.find_element(By.XPATH, ".//button[2]")                          
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_excluir)
            time.sleep(2) 
            
            print("Clicando na lixeira...")
            self.driver.execute_script("arguments[0].click();", botao_excluir)
            
            print("Linha excluída visualmente. ")
            time.sleep(2)

            print("Rolando para o topo para ver mensagem de sucesso...")
            self.driver.execute_script("window.scrollBy(0, -600);")
            time.sleep(3) 

            print("--- SALVANDO O CURSO ---")
            btn_salvar = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Salvar Curso']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_salvar); time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn_salvar)
            
            self._lidar_com_modal_sucesso()

            print(f"Verificando se '{NOME_PARA_EXCLUIR}' realmente sumiu...")
            
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, f"//td[contains(., '{NOME_PARA_EXCLUIR}')]")))
            
            print(" Sucesso ! Avaliação excluída.")
            time.sleep(2)

        except Exception as e:
            self.fail(f"Erro no RF24: {e}")

if __name__ == "__main__":
    unittest.main()