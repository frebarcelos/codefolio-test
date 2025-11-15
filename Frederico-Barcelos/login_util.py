
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    """Injeta dados de autenticação no Local Storage para simular o login."""
    print("Injetando dados de autenticação no Local Storage...")
    driver.get("https://testes.codefolio.com.br/")
    firebase_key = 'firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]'
    firebase_value = '{"apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg", "appName": "[DEFAULT]", "createdAt": "1762960014023", "displayName": "Frederico Barcelos", "email": "frebarcelos@gmail.com", "emailVerified": true, "isAnonymous": false, "lastLoginAt": "1762960677738", "phoneNumber": null, "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJH_pOq1T632cU3dzGf8vgZvgY2XeUhtdt_ZKGnMrTOoBQ6xA=s96-c", "providerData": [{"providerId": "google.com", "uid": "112220717969770670435", "displayName": "Frederico Barcelos", "email": "frebarcelos@gmail.com", "phoneNumber": null}], "stsTokenManager": {"accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4MDI5MzRmZTBlZWM0NmE1ZWQwMDA2ZDE0YTFiYWIwMWUzNDUwODMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiRnJlZGVyaWNvIEJhcmNlbG9zIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0pIX3BPcTFUNjMyY1UzZHpHZjh2Z1p2Z1kyWGVVaHRkdF9aS0duTXJUT29CUTZ4QT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2Mjk2MDY3NywidXNlcl9pZCI6IjFYaU1tZ3lhVUVWemRUNGdrcmNJOGtkZmRDSDIiLCJzdWIiOiIxWGlNbWd5YVVFVnpkVDRna3JjSThrZGZkQ0gyIiwiaWF0IjoxNzYyOTYwNjc3LCJleHAiOjE3NjI5NjQyNzcsImVtYWlsIjoiZnJlYmFyY2Vsb3NAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTIyMjA3MTc5Njk3NzA2NzA0MzUiXSwiZW1haWwiOlsiZnJlYmFyY2Vsb3NAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.JuvDixemuXur3-o86nRikiLEkz8e4A8jbCy4PkN2fAFHipQUCmWs4HgaE3w7Z3t6A8UTj_lN6efdYVcBaBRaW6AHJeW4HujcLGmA1a7krGKHE-LcLys-F-9Je2F9mLe4YHH9IAcawpfTco6CAXVb4kNhcqH5n3MVyMxEkH3em4aEgDGziN81FXXqaSO_ALPHq4iLYlZFetH8Quf1VWCNdUtOM7Dhfcsgr8St8dJMoVnbyNEu3fPDSEFSl-9i2nanPgoD0xXXvwxd1Q6Q7JxB5JDtxaxszczLPjkpOfgOe_h-tnFc8gGN-AmytXf3-YJnc7miArBrRjyFIQ6umZHWRg", "expirationTime": 1762964278507, "refreshToken": "AMf-vByq2q6fe6QDCQSCZOsCHStCTaN8zekxa3sLkHo14D1xotdJBhGkR-zKSoYbP2WQapTphIphc4kdrgsvnTGbaV5JIKMrJub9Nr6F6LwxivCw019h6bXQPUqq4mEyYB4SszztSaHLl2gMuGR27D-TKAt1UfBsBKFUtS0EiuzwFFaSRue-5lKvYVp3mUnQviyS8iVHeS8o4y8RXcujMcT42W8ZNflh5XELmuJv1GnXotbVuRfSl0pk0gfO4TyrktmXrni8dMs2XxdxM45-dpHa--9eHYY6nfpdD9OeanphNlF4qekSfHcnNZciNgB2khYSXeu2ZYK_WSIlJ-sYwkz2Q_igfqB7hcek8wPCW_-YpvSft9UmN8IfYk8V2-J5vIUl7HbukMCO3tE76AwU5eF2SLYv1VKlMZog85c4LqiQNRYuRASzISnqDa38y9GhxB7MTpQWBTOP"}, "tenantId": null, "uid": "1XiMmgyaUEVzdT4gkrcI8kdfdCH2", "_redirectEventId": null}'
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
