
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    """Injeta dados de autenticação no Local Storage para simular o login."""
    print("Injetando dados de autenticação no Local Storage...")
    driver.get("https://testes.codefolio.com.br/")
    firebase_key = 'firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]'
    firebase_value = '{"apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg", "appName": "[DEFAULT]", "createdAt": "1760400686052", "displayName": "Frederico Marques da Silva Barcelos", "email": "fredericobarcelos.aluno@unipampa.edu.br", "emailVerified": true, "isAnonymous": false, "lastLoginAt": "1762736760192", "phoneNumber": null, "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJJs29Oumy4niir5bs0zOS_IOeWlsXO1JRmVjNHXiFAtm1aZQ=s96-c", "providerData": [{"providerId": "google.com", "uid": "101352147922099288002", "displayName": "Frederico Marques da Silva Barcelos", "email": "fredericobarcelos.aluno@unipampa.edu.br", "phoneNumber": null}], "stsTokenManager": {"accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4MDI5MzRmZTBlZWM0NmE1ZWQwMDA2ZDE0YTFiYWIwMWUzNDUwODMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiRnJlZGVyaWNvIE1hcnF1ZXMgZGEgU2lsdmEgQmFyY2Vsb3MiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSkpzMjlPdW15NG5paXI1YnMwek9TX0lPZVdsc1hPMUpSbVZqTkhYaUZBdG0xYVpRPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3JlYWN0LW5hLXByYXRpY2EiLCJhdWQiOiJyZWFjdC1uYS1wcmF0aWNhIiwiYXV0aF90aW1lIjoxNzYyNzM2NzYwLCJ1c2VyX2lkIjoiTUcyeUNGdWRWUU9vaGtEaUtQODlUTHZZYjJWMiIsInN1YiI6Ik1HMnlDRnVkVlFPb2hrRGlLUDg5VEx2WWIyVjIiLCJpYXQiOjE3NjI5NTQ4NTgsImV4cCI6MTc2Mjk1ODQ1OCwiZW1haWwiOiJmcmVkZXJpY29iYXJjZWxvcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwMTM1MjE0NzkyMjA5OTI4ODAwMiJdLCJlbWFpbCI6WyJmcmVkZXJpY29iYXJjZWxvcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.F_jaQ4k6FSBdYMCNIlq1AxuGT1WcyXv4Dd4jIYVHJ9WLU_5TRdrKI1ZfEbgrC6l-xLx4fYkr7ifI2lZp4sjFGx4rY-rnqImfYKD15Omjmy9RQaYhGv4iT5qPDB-ODAGNYtVjxK89Qfr8YVyaW5voqKKuKMsdpybbpNYYNnvhsfp5AMYhF74e9HKxs7p2rCrvE4N46Su6-EHgZ3pXmOhXVNzuwzC9we6p5y0eyDrYlZjzY8Yf7_EAP0xDBUpHNEKl-_aA-RWGUFQMcfASMYl_0Zji6jN_Mz-VZvUhQHvdUZfzm63BGCaXEB0M3BdxN4qb8sHcIPN4zV7eHnSYXqoBBw", "expirationTime": 1762958458856, "refreshToken": "AMf-vBwdeUNDFfdSmS8nqQSCQtpyB9AlnSjtcW-3KOq7nHEdTCHfxaouALr0MmsCxIb4qbNIO38zHqTZcQ-Sp2esSsYsteT9xuzLB9czmVsSv-ZWlYKRTc0gukx_OirHYsRBM3clfzYbNEL3FQcCx1p9WsuswFaUy-G3-bb5rG68kfNgdsuKdSjwTIsbldJTGQmg4UnHR6AFkHysJsH-dvcuMdn0rPENpzyPsXlbq34a8B1bUbI-76veFN0sqMgNpX-IDGN8Ng7c1BW_ZNjfcbKyPSDGwtDgnxlXFXQu7yZ3booj7HXcKj2A7ikX4xlhIwHoiXM46J1amOL_jC6rxbRLzpzvw4CNkGqbqu7J5n2xsF0rNQzvOFMVaApOt2p0V3VRRwLY9MxwWHtlvgyQJlHRx_LgvpSicSmLFhepXS8FiDmlhTMxceZafnVUdzQ3P597WdVpWM4OCCcMFnWC0m34u8d5svY_vrCWP-qPxnENEc8gB1EfrcE"}, "tenantId": null, "uid": "MG2yCFudVQOohkDiKP89TLvYb2V2", "_redirectEventId": null}'
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
