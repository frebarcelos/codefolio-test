"""Utilitário de login para testes."""
import time


# ===================================================================
# IMPORTANTE: VOCÊ PRECISA PEGAR SEU PRÓPRIO TOKEN!
# 
# Como pegar:
# 1. Abra https://testes.codefolio.com.br/ no Chrome
# 2. Faça login normalmente
# 3. Aperte F12 (Developer Tools)
# 4. Vá na aba "Application" (ou "Aplicativo")
# 5. No menu lateral esquerdo: Storage > Local Storage > https://testes.codefolio.com.br
# 6. Procure pela chave que começa com "firebase:authUser:..."
# 7. Copie o NOME da chave (será algo como "firebase:authUser:AIzaSy...:[DEFAULT]")
# 8. Copie o VALOR (será um JSON grande)
# 9. Cole aqui embaixo substituindo os valores
# ===================================================================

def login(driver, url_base="https://testes-codefolio.web.app/"):
    """
    Faz login injetando token do Firebase no localStorage.
    
    Args:
        driver: Instância do WebDriver
        url_base: URL base da aplicação
    """
    # Credenciais do Andreus Dean (Professor)
    # Token gerado em: 24/11/2024
    # Expira em: 24/11/2024 às 15:47
    FIREBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
    FIREBASE_VALUE = """{"apiKey":"AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co","appName":"[DEFAULT]","createdAt":"1763932185417","displayName":"Andreus Dean Ferreira Almeida Rodrigues Vargas","email":"andreusvargas.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1764005130008","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocI5OLfGkiTXeHV8aEubMXmuTtOn1pyCEf5U5wGXqdmRp5axbw=s96-c","providerData":[{"providerId":"google.com","uid":"114530124225849729507","displayName":"Andreus Dean Ferreira Almeida Rodrigues Vargas","email":"andreusvargas.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocI5OLfGkiTXeHV8aEubMXmuTtOn1pyCEf5U5wGXqdmRp5axbw=s96-c"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQW5kcmV1cyBEZWFuIEZlcnJlaXJhIEFsbWVpZGEgUm9kcmlndWVzIFZhcmdhcyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJNU9MZkdraVRYZUhWOGFFdWJNWG11VHRPbjFweUNFZjVVNXdHWHFkbVJwNWF4Ync9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdGVzLWNvZGVmb2xpbyIsImF1ZCI6InRlc3Rlcy1jb2RlZm9saW8iLCJhdXRoX3RpbWUiOjE3NjQwMDUyNDEsInVzZXJfaWQiOiJtN0s1U2xKcVZrZUo1ZnJBZGxud213aDRIYzgzIiwic3ViIjoibTdLNVNsSnFWa2VKNWZyQWRsbndtd2g0SGM4MyIsImlhdCI6MTc2NDAwNTI0MSwiZXhwIjoxNzY0MDA4ODQxLCJlbWFpbCI6ImFuZHJldXN2YXJnYXMuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTQ1MzAxMjQyMjU4NDk3Mjk1MDciXSwiZW1haWwiOlsiYW5kcmV1c3Zhcmdhcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.Bxq-5Di46_QJbwTNoD-Udc3CIQYLfIwamK7sIPc_lsF_BU6ZJRDgsDqCr9gS22TiWTWg3ZakB6hjTSvY3rfDKpHbwQu_AaE8BeaXC9cjS4YKaya_3Zk7UFe9J7255jz1mwPvp5EzN4K2W--gbw0Kpqzs8AEsAWbmOW7Tep-e54_G2CDsuEW7aQx1hVcWtnXjMrPrOj4KwQr2q_XP8MO6ThtBw14GDf6SKspfEIs_8Xf1o448SUNuIvVfiSeV4dlnQBfWZI6st5Y_X0xLMgxEanx7lRFXHQ_CnpqmhpBGnobf1z29LwTQynPitwAL5s_fz29mEQyFJZ3B1h35PxLpEw","expirationTime":1764008841653,"refreshToken":"AMf-vBzilwznsutZ7oC1gFnD5V4QmKvRh-6l5FiPsWdEHBzqjnSqt2REL5S_NCvtOtzGl2ZpTo-3DoG7hQJ9tJAikcLno7fMDQnOX8HDRsD01CRLmEuC-HzOVYrwOLMJppB3f9P7SfkwjjU_mYUM7yhy-1Tj9fuS1nvAbzZfsaJjlIpEpc8xRRtYVpLmJOMPreHEksPIyoJmbfhLrWi7cG9zga_nuMzbljcJtwPazFDiycLHc6CIwLGNCeysbqvFZotojdzurXTsArLl6xqbsENzPrARWE0LKKDneWbalfPmkSpLCPCiNWvDdeoF7beH9bO03HUcKcKV60fwYuhQB4ssKu4hdmDSEKVswcI2jOz1Fgjw8qjXUpI8kVUSLEod_aRFT0K69x5wg-jZuNCy1zq-hKJ3ce9jIgR9kvNdEibA6iwZTXurJbGVa6DoBvlXES6wpQ4gtqIXOgw49l76vGmCI2nroF9syd6qNnPdKmJyrPrpUsP8SpDPyNYWhuxMb136spc8UpOc"},"tenantId":null,"uid":"m7K5SlJqVkeJ5frAdlnwmwh4Hc83","_redirectEventId":null}"""
    
    print("🔐 Fazendo login com credenciais do Andreus...")
    driver.get(url_base)
    
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        FIREBASE_KEY,
        FIREBASE_VALUE
    )
    
    driver.refresh()
    time.sleep(2)
    print("✅ Login realizado")


def verificar_login(driver, wait):
    """
    Verifica se o login foi bem-sucedido.
    
    Args:
        driver: Instância do WebDriver
        wait: Instância do WebDriverWait
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    
    print("🔍 Verificando login...")
    time.sleep(3)
    
    # Verifica se botão de perfil está presente
    profile_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
        )
    )
    
    print("✅ Login verificado com sucesso")