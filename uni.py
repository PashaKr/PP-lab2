import unittest
from unittest.mock import mock_open, patch
from main import DomainValidator, FileDomainExtractor


class TestDomainValidator(unittest.TestCase):
    def test_validate_correct_domain(self):
        # Проверяем корректные доменные имена
        self.assertTrue(DomainValidator.validate("example.com"))
        self.assertTrue(DomainValidator.validate("sub.domain.org"))


    def test_extract_from_text(self):
        # Проверяем извлечение доменных имён из текста
        text = "stankin.ru vk.com"
        result = DomainValidator.extract_from_text(text)
        self.assertEqual(result, ["stankin.ru", "vk.com"])

    def test_extract_from_text_no_domains(self):
        # Проверяем случай, когда доменные имена отсутствуют
        text = "No domains here!"
        result = DomainValidator.extract_from_text(text)
        self.assertEqual(result, [])


class TestFileDomainExtractor(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="stankin.ru vk.com")
    def test_extract_domains_from_file(self, mock_file):
        extractor = FileDomainExtractor("fake_path.txt")
        result = extractor.extract()
        self.assertEqual(result, ["stankin.ru", "vk.com"])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_extract_file_not_found(self, mock_file):
        extractor = FileDomainExtractor("fake_path.txt")
        with self.assertRaises(ValueError) as context:
            extractor.extract()
        self.assertEqual(str(context.exception), "Файл по пути fake_path.txt не найден.")


if __name__ == "__main__":
    unittest.main()
