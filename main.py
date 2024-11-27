import re
import requests

class DomainValidator:
    DOMAIN_REGEX = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.[A-Za-z]{2,})+$"


    @classmethod
    def validate(cls, domain):
        """Проверяет, является ли строка синтаксически корректным доменным именем."""
        return re.match(cls.DOMAIN_REGEX, domain) is not None

    @classmethod
    def extract_from_text(cls, text):
        """Извлекает все корректные доменные имена из текста."""
        return re.findall(cls.DOMAIN_REGEX, text)


class FileDomainExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        """Читает файл и извлекает доменные имена."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return DomainValidator.extract_from_text(content)
        except FileNotFoundError:
            raise ValueError(f"Файл по пути {self.file_path} не найден.")


class URLDomainExtractor:
    def __init__(self, url):
        self.url = url

    def extract(self):
        """Загружает содержимое страницы по URL и извлекает доменные имена."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return DomainValidator.extract_from_text(response.text)
        except requests.RequestException as e:
            raise ValueError(f"Ошибка при загрузке страницы: {e}")


class DomainCheckerApp:
    def run(self):
        print("1. Проверить доменное имя")
        print("2. Найти доменные имена на веб-странице")
        print("3. Найти доменные имена в файле")
        choice = input("Выберите действие (1/2/3): ").strip()

        if choice == "1":
            self.check_domain()
        elif choice == "2":
            self.extract_domains_from_url()
        elif choice == "3":
            self.extract_domains_from_file()
        else:
            print("Неверный выбор. Завершение работы.")

    def check_domain(self):
        domain = input("Введите доменное имя для проверки: ").strip()
        if DomainValidator.validate(domain):
            print("Доменное имя корректно.")
        else:
            print("Доменное имя некорректно.")

    def extract_domains_from_url(self):
        url = input("Введите URL веб-страницы: ").strip()
        extractor = URLDomainExtractor(url)
        try:
            domains = extractor.extract()
            if domains:
                print("Найденные доменные имена:", domains)
            else:
                print("На странице доменные имена не найдены.")
        except ValueError as e:
            print(e)

    def extract_domains_from_file(self):
        file_path = input("Введите путь к файлу: ").strip()
        extractor = FileDomainExtractor(file_path)
        try:
            domains = extractor.extract()
            if domains:
                print("Найденные доменные имена в файле:", domains)
            else:
                print("В файле доменные имена не найдены.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    app = DomainCheckerApp()
    app.run()
