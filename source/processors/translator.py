import argostranslate.package
import argostranslate.translate
import pandas as pd

class Translator:
    def __init__(self, from_code='de', to_code='en'):
        self.from_code = from_code
        self.to_code = to_code

    def translate(self, texts):
        if isinstance(texts, str):
            return argostranslate.translate.translate(texts, self.from_code, self.to_code)
        elif isinstance(texts, list):
            return [argostranslate.translate.translate(text, self.from_code, self.to_code) for text in texts]
        else:
            raise ValueError("Input must be either a string or a list of strings.")

    @staticmethod
    def install_package(self, from_code='de', to_code='en'):
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code,
                available_packages,
            ),
            None
        )
        if package_to_install and package_to_install not in argostranslate.package.get_installed_packages():
            argostranslate.package.install_from_path(package_to_install.download())