import unittest
from unittest.mock import patch
import requests
from bs4 import BeautifulSoup
from io import StringIO

from your_module_name import Proiect_TSS
class TestGDPRLoginPage(unittest.TestCase):

    @patch('builtins.print')
    @patch('requests.get')
    def test_login_page_gdpr_compliant(self, mock_get, mock_print):
        html_content = '''
            <html>
                <head><title>Login</title></head>
                <body>
                    <form>
                        <input type="email" name="email" />
                        <input type="password" name="password" />
                        <input type="checkbox" name="remember" />
                    </form>
                    <a href="/privacy-policy">Politica de confidențialitate</a>
                </body>
            </html>
        '''
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = str.encode(html_content)
        mock_response.url = 'https://yahoo.com/login'

        mock_get.return_value = mock_response

        check_login_page_gdpr("https://yahoo.com/login")

        expected_outputs = [
            "✅ Conexiune criptată (HTTPS activ).",
            "✅ Există opțiune de consimțământ",
            "✅ Politica de confidențialitate este prezentă.",
            "✅ Formular de logare corect structurat"
        ]

        output_text = "\n".join(call.args[0] for call in mock_print.call_args_list if call.args)
        for expected in expected_outputs:
            self.assertIn(expected, output_text)

    @patch('builtins.print')
    @patch('requests.get')
    def test_login_page_gdpr_non_compliant(self, mock_get, mock_print):
        html_content = '''
            <html>
                <head><title>Login</title></head>
                <body>
                    <form>
                        <!-- Fără câmpuri email/parolă -->
                    </form>
                    <!-- Fără checkbox, fără politică -->
                </body>
            </html>
        '''
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = str.encode(html_content)
        mock_response.url = 'http://yahoo.com/login' 
        mock_get.return_value = mock_response

        check_login_page_gdpr("http://yahoo.com/login")

        expected_warnings = [
            "⚠️ Conexiunea nu este criptată",
            "⚠️ Nu există nicio opțiune de consimțământ",
            "⚠️ Lipsă link către politica de confidențialitate",
            "⚠️ Formular de logare incomplet"
        ]

        output_text = "\n".join(call.args[0] for call in mock_print.call_args_list if call.args)
        for expected in expected_warnings:
            self.assertIn(expected, output_text)

if __name__ == '__main__':
    unittest.main()

 





