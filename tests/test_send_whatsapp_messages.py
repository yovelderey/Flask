import unittest
from unittest.mock import patch, MagicMock
from send_whatsapp_messages import send_message, wait_for_response, clean_text

class TestSendMessage(unittest.TestCase):
    @patch('send_whatsapp_messages.WebDriverWait')
    @patch('send_whatsapp_messages.driver')
    def test_send_message(self, mock_driver, mock_wait):
        mock_wait.return_value.until.return_value = MagicMock()
        mock_driver.find_element.return_value = MagicMock()
        
        send_message('1234567890', 'Hello World')
        
        mock_wait.return_value.until.assert_called()
        mock_driver.find_element.assert_called()
    
    @patch('send_whatsapp_messages.WebDriverWait')
    @patch('send_whatsapp_messages.driver')
    def test_send_message_not_found(self, mock_driver, mock_wait):
        mock_wait.return_value.until.return_value = MagicMock()
        mock_driver.find_element.side_effect = Exception("Contact not found")
        
        with self.assertRaises(Exception):
            send_message('9876543210', 'Hello World')
    
    @patch('send_whatsapp_messages.WebDriverWait')
    @patch('send_whatsapp_messages.driver')
    def test_send_message_empty_message(self, mock_driver, mock_wait):
        mock_wait.return_value.until.return_value = MagicMock()
        mock_driver.find_element.return_value = MagicMock()
        
        send_message('1234567890', '')
        
        mock_wait.return_value.until.assert_called()
        mock_driver.find_element.assert_called()

    @patch('send_whatsapp_messages.WebDriverWait')
    @patch('send_whatsapp_messages.driver')
    def test_wait_for_response(self, mock_driver, mock_wait):
        mock_wait.return_value.until.return_value = MagicMock()
        mock_driver.find_elements.return_value = [MagicMock(text='Test response')]
        
        response = wait_for_response('1234567890', timeout=10)
        self.assertEqual(response, 'Test response')

    def test_clean_text(self):
        self.assertEqual(clean_text('  Hello World  '), 'Hello World')
        self.assertEqual(clean_text('\nHello\n'), 'Hello')

if __name__ == '__main__':
    unittest.main()
