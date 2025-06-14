import requests
from bs4 import BeautifulSoup


def check_login_page_gdpr(url):
    print(f"\n🔍 Analiză GDPR pentru pagina de logare: {url}\n")

    try:
        response = requests.get(url)
        
        if not response.url.startswith("https"):
            print("⚠️ Conexiunea nu este criptată (HTTPS lipsește).")
        else:
            print("✅ Conexiune criptată (HTTPS activ).")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Caută checkbox-uri gen "remember me"
        checkboxes = soup.find_all('input', {'type': 'checkbox'})
        if checkboxes:
            print("✅ Există opțiune de consimțământ (ex: 'Ține-mă minte').")
        else:
            print("⚠️ Nu există nicio opțiune de consimțământ vizibilă.")

        # Caută link către politica de confidențialitate
        privacy_links = soup.find_all('a', href=True)
        privacy_found = any("privacy" in link['href'].lower() or "confiden" in link.text.lower()
                            for link in privacy_links)

        if privacy_found:
            print("✅ Politica de confidențialitate este prezentă.")
        else:
            print("⚠️ Lipsă link către politica de confidențialitate.")

        # Caută câmpuri de email și parolă
        email_input = soup.find('input', {'type': 'email'})
        password_input = soup.find('input', {'type': 'password'})

        if email_input and password_input:
            print("✅ Formular de logare corect structurat (email + parolă).")
        else:
            print("⚠️ Formular de logare incomplet sau neconform.")

    except Exception as e:
        print(f"❌ Eroare la accesarea paginii: {e}")


# Exemplu de utilizare:
if __name__ == "__main__":
    # Exemplu generic (schimbă cu o pagină reală de logare dacă ai una)
    check_login_page_gdpr("https://yahoo.com/login")


