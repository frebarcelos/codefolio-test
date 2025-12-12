"""
Utilitário de autenticação Firebase para testes Selenium
Injeta credenciais de Pietro Mendes Prauchner no localStorage
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_base = "https://testes-codefolio.web.app/"
time_out = 10

def login(driver):
    """Injeta dados de autenticação no Local Storage para simular o login."""
    print("Injetando dados de autenticação no Local Storage...")
    driver.get(url_base)
    firebase_key = 'firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]'
    firebase_value = '{"apiKey": "AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co", "appName": "[DEFAULT]", "createdAt": "1763922181724", "displayName": "Pietro Mendes Prauchner", "email": "pietroprauchner.aluno@unipampa.edu.br", "emailVerified": true, "isAnonymous": false, "lastLoginAt": "1763922181725", "phoneNumber": null, "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocLnOKcEKNkpWJldBkXRZxCcoC9XDjbX2wdobsbteoWtbLsWNw=s96-c", "providerData": [{"providerId": "google.com", "uid": "112719305460000187643", "displayName": "Pietro Mendes Prauchner", "email": "pietroprauchner.aluno@unipampa.edu.br", "phoneNumber": null}], "stsTokenManager": {"accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUGlldHJvIE1lbmRlcyBQcmF1Y2huZXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTG5PS2NFS05rcFdKbGRCa1hSWnhDY29DOVhEamJYMndkb2JzYnRlb1d0YkxzV053PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3Rlc3Rlcy1jb2RlZm9saW8iLCJhdWQiOiJ0ZXN0ZXMtY29kZWZvbGlvIiwiYXV0aF90aW1lIjoxNzYzOTIyMTkxLCJ1c2VyX2lkIjoidXlBNWxoazlUak1abFJxSnRNSmRhMmlTazdpMiIsInN1YiI6InV5QTVsaGs5VGpNWmxScUp0TUpkYTJpU2s3aTIiLCJpYXQiOjE3NjQyMDA1MDYsImV4cCI6MTc2NDIwNDEwNiwiZW1haWwiOiJwaWV0cm9wcmF1Y2huZXIuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTI3MTkzMDU0NjAwMDAxODc2NDMiXSwiZW1haWwiOlsicGlldHJvcHJhdWNobmVyLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.FFBFMVSEOTS4Ll4wGhlYy85GsvxZWhHAvib7kjhrAHHTk7Tjw7K5Bxr5I8ERofEwDzqg5S_xIprZCqM4nH9PR_vYebxbuYDPDgrjjP0zcc1tqZJUn1AARDQzj3vv_9mUdqbpvHdMCESqEXv0Gq2dK6SngIM2zEFA6nuQzuEZRfqFWreSYJcBIWRw6S64-XlzB9uJK1W2trQOXhDDGY7P_NfVCLUf3tvwLS-_h3rsZ2UjM9ZhV18Q06P_z20anYnMCTb11SsSh4SrBuHWi5nwtanQsX9Zgcu20Xfp1r8fTjiUhZbJUf-XlLzr6WBnT5q7Rh2r3blCw-ZOX_L1LGGByw", "expirationTime": 1764204110850, "refreshToken": "AMf-vBysJFaWqOIM2vAshop6VgdY1N6bO1MAQ26qbtxKewzz8r5uNcE9QzWG6J12_Y7W-2jkc-FgAOMbpM-R0IirQ5sHtINCIArppumLyccLWE8s87kMf45QjqwopcfY5gyANRTOfglnd0AhpTXSjbG8nJrZ6r9Jn0rROd07jGeyg1yi81xq2TS9OFH90x6vSA_6hRes3ZmwAC1XESxtVFjZGBG4U_oBpB-_dZCF30j6egaf3u8fs1k6cb1arbu-_3z0hlhBhPwWrBNu8YlUKvEQh2mjB4ApeZc_HxMtYLvpf_FFqIMIS-2rTAm8lnoj6L5FAhHcfZB_FNPtK4eOFvFe5BGM_UBp6yXNNtK4yFCa9ueeV-CRhiP8y6PnFz52R2B4k_ZGJ5Rf6xE6TGna8RgNtH-jW4fj3KHDLCXczkHnQtPQTtasoHK2jnoCu0ibU3z5KC27ahCVsoi6hQJhu0Vck-XZpPsJnw"}, "tenantId": null, "uid": "uyA5lhk9TjMZlRqJtMJda2iSk7i2", "_redirectEventId": null}'
    try:
        driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            firebase_key,
            firebase_value
        )
        print("Injeção no Local Storage bem-sucedida.")
    except Exception as e:
        print(f"Falha crítica ao injetar no Local Storage: {e}")
        driver.quit()
        raise RuntimeError("Falha no setup do Local Storage") from e
    driver.refresh()
    time.sleep(2)

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
