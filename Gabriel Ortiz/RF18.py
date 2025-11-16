import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
from datetime import datetime

TIMEOUT = 15
URL_BASE = "https://testes.codefolio.com.br/"

FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = "{\"apiKey\":\"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg\",\"appName\":\"[DEFAULT]\",\"createdAt\":\"1762298062528\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"emailVerified\":true,\"isAnonymous\":false,\"lastLoginAt\":\"1762375068503\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\",\"providerData\":[{\"providerId\":\"google.com\",\"uid\":\"116550479800107608553\",\"displayName\":\"Gabriel Camargo Ortiz\",\"email\":\"gabrielortiz.aluno@unipampa.edu.br\",\"phoneNumber\":null,\"photoURL\":\"https://lh3.googleusercontent.com/a/ACg8ocKuSOr2aosq5ewYTkVZmicWpmM78CrCaNWVg8T_Nu4wk5U76w=s96-c\"}],\"stsTokenManager\":{\"accessToken\":\"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiR2FicmllbCBDYW1hcmdvIE9ydGl6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0t1U09yMmFvc3E1ZXdZVGtWWG1pY1dwbU03OENyQ2FOV1ZnOFRfTnU0d2s1VTc2dz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjM3NTA2OCwidXNlcl9pZCI6IkRicWhoa2laRGROZWxNMXlsdlA3UW5vY2g2QTMiLCJzdWIiOiJEYnFoaGtpWkRkTmVsTTF5bHZQN1Fub2NoNkEzIiwiaWF0IjoxNzYyMzc4NTQwLCJleHAiOjE3NjIzODIxNDAsImVtYWlsIjoiZ2FicmllbG9ydGl6LmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE2NTUwNDc5ODAwMTA3NjA4NTUzIl0sImVtYWlsIjpbImdhYnJpZWxvcnRpei5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.gSpY-wiJTMD1UKbLdV0H_-88rP4EjZT97XJBNeJYcCvtaI_-aUFCHIsYjcb93IM7hdSyfaueJbZqSEgO-ue-U9oc57aDwWNSFIlKZ8dHbYxiFBhj5Mr5I3WrmUlis1e_CnpgWS3d8Zo_CIq2tUumGRmaBUdvA4hGRp7_m6s0JP7ex1dykS0hiXRbpjgKnJny3NKGQ5_vhRj8xeYdyxubDfEmx-iPFArxUQXwraglY8ULH8XmkR4GtDr3Dfgkm5u3JYAtd3YiCkEdJUcrLmXiCZNwoWW3dMJ67b7GvTL6ONt3yQMWYJktjJ8hBhC7KdkRYaJIRvHAdC0nhRy-HTslTw\",\"expirationTime\":1762382144118,\"refreshToken\":\"AMf-vBzXfOOx4uuxgjeYVCXhmoKwXhjZmcZLc2yQDBbi-wIQyJCuWkkSFmPl37Z7a9PuyCtXDvPttjH_tgdaS6JIh8oR9nQ-G-0qmuosOpocx9hazemh4Q85GVybUEOEVx5gw0ARBtN8jtdsOxYh8QQSCdKeI6on8GmoYPGif2wJ-ZZ3KpCUFlLw0t0JvUknlh0nxsfnei46Qu2aYSH1Tz2-5sUyn7E-ghbYkJH-H-AgcnDi8oWlCh5WTFzsCaSgva5-2cQHVaBNIzZKENltzah7iSf7SUiQj_WvCMLyg-FO87hNc--g6d-lULpNpwz9yScZnA1vJDinCnU7Cbl1pefFXRTA-nD4s1mkdHcvm7exzX5kd3TAbVNZ3CQ-JiU-7h-Mo5ISrsZZxHtCksr6w93Xk9KyYhYC8uAEIlx8xqlRL8KlsWOtXgzDEJWW_Fmk_W4LUaL2XBQh_tMfroBxm5EMW3UarWBUKw\",\"tenantId\":null},\"uid\":\"DbqhhkiZDdNelM1ylvP7Qnoch6A3\",\"_redirectEventId\":null}"


class TestRF18ExclusaoAlunos(unittest.TestCase):

   
    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service) 
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        
        print("\nCarregando a URL base...")
        self.driver.get(URL_BASE)
        self.driver.execute_script("window.localStorage.clear();")
        print("Injetando novos dados de autenticação...")
        try:
            self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);",
                                 FIREBASE_KEY,
                                 FIREBASE_VALUE)
        except Exception as e:
            self.driver.quit()
            self.fail(f"Falha crítica ao injetar no Local Storage: {e}")

        self.driver.refresh()
        time.sleep(5) 

        try:
            seletor_perfil = (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
            profile_button = self.wait.until(EC.presence_of_element_located(seletor_perfil))
    
            self.driver.execute_script("arguments[0].click();", profile_button)
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//li[normalize-space()='Sair']")
            ))
            print("Login validado com sucesso!")
            self.driver.execute_script("document.body.click();")
        except Exception as e:
            print("--- ERRO NA VALIDAÇÃO DO LOGIN ---")
            print(f"Exceção: {e}")
            self.driver.quit()
            self.fail(f"Falha na injeção de sessão do Firebase. Verificação falhou.")


    def tearDown(self):
        print("Teste concluído, fechando o navegador.")
        if hasattr(self, 'driver'):
            self.driver.quit()

  

    def _navegar_para_gerenciar_curso(self, nome_curso):
        self.driver.get(URL_BASE + "manage-courses")
        self.wait.until(EC.url_contains("/manage-courses"))
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[normalize-space()='Criar Novo Curso']")
        ))
        time.sleep(1) 
       
        xpath_botao_gerenciar = f"""//h6[normalize-space()='{nome_curso}']/parent::div/following-sibling::div[contains(@class, 'MuiCardActions-root')]//button[normalize-space()='Gerenciar Curso']"""
        
        curso = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath_botao_gerenciar)
        ))
        self.driver.execute_script("arguments[0].click();", curso)
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h5[normalize-space()='Gerenciar Curso']") 
        ))

    def _clicar_na_aba_alunos(self):
        seletor_aba_alunos = (By.XPATH, "//button[@role='tab' and normalize-space()='Alunos']")
        aba_alunos = self.wait.until(EC.presence_of_element_located(seletor_aba_alunos))
        self.driver.execute_script("arguments[0].click();", aba_alunos)


    def test_rf18_exclusao_alunos(self):
        print("\nExecutando RF18: Excluir Aluno")
    
        NOME_CURSO = "Curso Selenium 1762542384178" 
        EMAIL_ALUNO = "gabrielcamargoortiz@gmail.com" 

        try:
            self._navegar_para_gerenciar_curso(NOME_CURSO)
            self._clicar_na_aba_alunos()

        
            print("Aba Alunos clicada. Esperando a tabela carregar...")
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//th[normalize-space()='Email']")
            ))
            
            print(f"Procurando o botão 'Excluir' para o aluno: {EMAIL_ALUNO}")
            seletor_lixeira = (
                By.XPATH,
                f"//tr[.//td[contains(., '{EMAIL_ALUNO}')]]//button[contains(@class, 'MuiIconButton-root')]"
                )

            botao_excluir = self.wait.until(EC.presence_of_element_located(seletor_lixeira))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_excluir)
            time.sleep(1.0)

            botao_excluir = self.wait.until(EC.element_to_be_clickable(seletor_lixeira))

            print("Clicando no botão lixeira...")
            self.driver.execute_script("arguments[0].click();", botao_excluir)
            time.sleep(2)

            print("Esperando o pop-up de confirmação...")
            try:
                self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@role, 'dialog') or contains(@class, 'MuiDialog-root')]")
                ))
            except:
                print(" pop up não apareceu!")
                raise
            time.sleep(1)   

            try:
                botao_confirmar = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, "//button[contains(normalize-space(),'Confirmar')]"
                    ))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_confirmar)
                time.sleep(0.5)

                self.driver.execute_script("arguments[0].click();", botao_confirmar)
                print("Clique no botão Confirmar realizado!")
                time.sleep(2)

                print("Clicando em salvar curso...")
                botao_salvar = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(., 'Salvar Curso')]"
                )))
                self.driver.execute_script("arguments[0].click();", botao_salvar)
                time.sleep(2)

            except Exception as e:
                print(f" Não foi possível clicar no botão Confirmar: {e}")
                raise   

            print("Aluno excluído. Verificando se ele desapareceu da tabela...")
            seletor_email_aluno = (By.XPATH, f"//td[contains(text(), '{EMAIL_ALUNO}')]")
            try:
                
                    WebDriverWait(self.driver, 7).until(
                        EC.invisibility_of_element_located(seletor_email_aluno)
                    )
                    print("✅Aluno removido da tabela com sucesso!")
            except :
                    print("O elemento ainda aparece. recarregando...")

                    time.sleep(2)
                    self.driver.refresh()
                    time.sleep(2)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)

                    try:
                        self._clicar_na_aba_alunos()
                        time.sleep(1)
                    except:
                        print("Nao foi possivel reclicar na aba alunos") 
                   
                    print("Descendo a página para carregar a tabela de alunos...")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)

                    print("Rechecando se o aluno ta na tabela...")
                    time.sleep(3)
                    alunos_restantes = self.driver.find_elements(
                        By.XPATH, f"//td[contains(text(), '{EMAIL_ALUNO}')]"
                    )
                    if len(alunos_restantes) > 0:
                        print(" O aluno AINDA ESTÁ NA TABELA. Exclusão NÃO ocorreu de verdade.")
                        self.fail("O aluno não foi excluído mesmo após recarregar a página!")

                    print(" Após refresh + scroll, aluno realmente sumiu!")
        except Exception as e:
             raise            

if __name__ == "__main__":
    unittest.main()