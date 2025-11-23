
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_base = "https://testes-codefolio.web.app/"
time_out = 10
id_deslogado = "-OeNFj3mimZ_UQTPIshl"
def login(driver):
    """Injeta dados de autenticação no Local Storage para simular o login."""
    print("Injetando dados de autenticação no Local Storage...")
    driver.get(url_base)
    firebase_key = 'firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]'
    firebase_value = '{"apiKey": "AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co", "appName": "[DEFAULT]", "createdAt": "1763469197986", "displayName": "Frederico Marques da Silva Barcelos", "email": "fredericobarcelos.aluno@unipampa.edu.br", "emailVerified": true, "isAnonymous": false, "lastLoginAt": "1763469197986", "phoneNumber": null, "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJJs29Oumy4niir5bs0zOS_IOeWlsXO1JRmVjNHXiFAtm1aZQ=s96-c", "providerData": [{"providerId": "google.com", "uid": "101352147922099288002", "displayName": "Frederico Marques da Silva Barcelos", "email": "fredericobarcelos.aluno@unipampa.edu.br", "phoneNumber": null}], "stsTokenManager": {"accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4MDI5MzRmZTBlZWM0NmE1ZWQwMDA2ZDE0YTFiYWIwMWUzNDUwODMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiRnJlZGVyaWNvIE1hcnF1ZXMgZGEgU2lsdmEgQmFyY2Vsb3MiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSkpzMjlPdW15NG5paXI1YnMwek9TX0lPZVdsc1hPMUpSbVZqTkhYaUZBdG0xYVpRPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3Rlc3Rlcy1jb2RlZm9saW8iLCJhdWQiOiJ0ZXN0ZXMtY29kZWZvbGlvIiwiYXV0aF90aW1lIjoxNzYzNDY5MTk4LCJ1c2VyX2lkIjoiMm5rdm90Z3NuNGc1UmZQQ1hLRmh0cnZwR0I3MiIsInN1YiI6IjJua3ZvdGdzbjRnNVJmUENYS0ZodHJ2cEdCNzIiLCJpYXQiOjE3NjM0NzQyMjMsImV4cCI6MTc2MzQ3NzgyMywiZW1haWwiOiJmcmVkZXJpY29iYXJjZWxvcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwMTM1MjE0NzkyMjA5OTI4ODAwMiJdLCJlbWFpbCI6WyJmcmVkZXJpY29iYXJjZWxvcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.D0jOI4vy-UAyodDeiCORbQgS5oMW3-7wNc0r95GiO_DR6yE45klfv5y6v5bbS7hBEINL2XfVRl2fzLpyDcLnQG4BIEbnpO1hdV1054jmxWZhSR2f0uQD8d_GtkNP23NFLS2LUtZf2AU9YWsZFKbjkJddC6A1H53Xiu1N_A4JB0XL1vhNQl1YknuSCaRGXFRcN0z14woAgqjVFGpF_5_muygbHIz_kPhshFOv9SC1CxfbotXSJBXkrN_w6ouxCLLTWPppzPwMFI6A-Jpxzvk3sZ7phbAQhECdmrJ9JKcNdD4zgQDSYnBSpn5XC7OXcqtcqYTj-eKraDl-sKVAVnnfzg", "expirationTime": 1763477824304, "refreshToken": "AMf-vBxAbZmv_lKQ9dvCDqS8Pn5k_3R_HdSst9xEGX75hRTnE0t-08LVi-jyXgw4nb172MKz0vH8COGbTdqCqU9utc-jjsxKoFZHTV1kHjzhugo_p2YGDaXjsRFKzvYIvWGx9kIzWqYbCm3OoUiPDIPzu_R8mybqWjfJUmsl66Rq5eI1O-ju_l5D22n8lMbfRza_blOqFtHWTdgrNRS_SM7zvUAUMi4U9_BdUyqtgYEKASHIBLmX0ccFfITYPhCBav8Lc8tKodkRtMW1flXC9tUQCEn10S8TGJRdxXq6Yf8pM3RXYUgDL2W74jyOpNrppbU7zAk4h2ChNaeAK2kvuV3V5MCMB4Agg-C-3THr7JQQVh8w92-40woWO55xDHY8mYF4CGG4cAna9_xUSMnnZBB58SxfK97WdXkF12UHu0TPfZ4JDUK1Se-IRUkgEdCGnSrN9aZBMBawFs5JFQUZf1aP2XBYl1UheeKu3tvs1WmsiEaxqmuiOlA"}, "tenantId": null, "uid": "2nkvotgsn4g5RfPCXKFhtrvpGB72", "_redirectEventId": null}'
    try:
        driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            firebase_key ,
            firebase_value
        )
        print("Injeção no Local Storage bem-sucedida.")
    except Exception as e:
        print(f"Falha crítica ao injetar no Local Storage: {e}")
        driver.quit()
        raise RuntimeError("Falha no setup do Local Storage") from e
    driver.refresh()
    time.sleep(2) # Pausa para garantir que o login seja processado

def verificar_login(driver, wait):
    """Verifica se o login foi bem-sucedido."""
    print("Verificando se o login foi processado...")
    try:
        print("Aguardando 5s para o Firebase SDK processar o login...")
        time.sleep(5)
        profile_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
        driver.execute_script("arguments[0].click();", profile_button)
        print("Clicou no botão de perfil para abrir o menu.")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[normalize-space()='Sair']")))
        print("Login validado com sucesso!")
        driver.execute_script("document.body.click();")
    except Exception as e:
        print("--- ERRO NA VALIDAÇÃO DO LOGIN ---")
        print(f"Causa provável: O token no 'FIREBASE_VALUE' expirou ou está incorreto.")
        print(f"Exceção: {e}")
        raise AssertionError("Falha na injeção de sessão do Firebase. O token pode estar expirado.")
