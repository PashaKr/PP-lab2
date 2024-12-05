import re

class DomainValidator:
    DOMAIN_REGEX = r"\b(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}\b"

    @classmethod
    def validate(cls, domain):
        return re.match(cls.DOMAIN_REGEX, domain) is not None

    @classmethod
    def extract_from_text(cls, text):
        return re.findall(cls.DOMAIN_REGEX, text)


class FileDomainExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return DomainValidator.extract_from_text(content)
        except FileNotFoundError:
            raise ValueError(f"Файл по пути {self.file_path} не найден.")


class DomainCheckerApp:
    def run(self):
        print("1. Проверить доменное имя")
        print("2. Найти доменные имена в файле")
        choice = input("Выберите действие (1/2): ").strip()

        if choice == "1":
            self.check_domain()
        elif choice == "2":
            self.extract_domains_from_file()
        else:
            print("Неверный выбор. Завершение работы.")

    def check_domain(self):
        domain = input("Введите доменное имя для проверки: ").strip()
        if DomainValidator.validate(domain):
            print("Доменное имя корректно.")
        else:
            print("Доменное имя некорректно.")

    def extract_domains_from_file(self):
        file_path = input("Введите путь к файлу: ").strip()
        extractor = FileDomainExtractor(file_path)
        try:
            domains = extractor.extract()
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print("Содержимое файла:\n", content)
            if domains:
                print("Найденные доменные имена в файле:", domains)
            else:
                print("В файле доменные имена не найдены.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    app = DomainCheckerApp()
    app.run()
