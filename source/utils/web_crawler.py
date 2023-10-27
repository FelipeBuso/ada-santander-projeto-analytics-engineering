from bs4 import BeautifulSoup
import requests
import os


# def scrap_links_rio_de_janeiro():
#     pass

class crawler:
    def __init__(self):
        pass

    def _request_get_main_page(self) -> str:
        """ Realiza a GET da página principal de catálogo de dados do Inside Airbnb.

        Raises:
            ValueError: Caso ocorra falha na requisição.
        """
        # Página central de dados
        uri = 'http://insideairbnb.com/get-the-data'

        # Solicitação HTTP get da página
        response = requests.get(uri)

        # Verificação do status da requisição
        if response.status_code != 200:
            raise ValueError(f'A solicitação falhou com o código de status: {response.status_code}')

        # Acesso ao conteúdo da resposta
        return response.text
    
    @property
    def main_html_content(self) -> str:
        """ Propriedade de conteúdo do HTML da requisição da página principal. """
        return self._request_get_main_page()


    def _scrap_links_rio_de_janeiro(self, html_content: str) -> list:
        """ Extrai as URL dos dados para a cidade do Rio de janeiro.

        Args:
            html_content (str): Conteúdo HTML do página de dados.

        Returns:
            list[str]: Lista de URL dos dados.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Filtro para os dados do Rio de Janeiro
        airbnb_tables = []
        for i in soup('table', {'class': 'rio-de-janeiro'})[0]('a'):
            airbnb_tables.append(i.attrs['href'])

        # Filtra apra somente os dados
        data_list = [link for link in airbnb_tables if '/data/' in link]
        return data_list
    

    def download_data_from_rio_de_janeiro(self, url_list: list, data_folder: str) -> None:
        for uri_data in url_list:
            # Nome do arquivo
            basename = uri_data.split('/')[-1]

            # Requisição do dado
            response = requests.get(uri_data)

            file_path = os.path.join(data_folder, basename)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f'O arquivo foi baixado com sucesso e salvo em {file_path}')
            else:
                print(f'O download falhou. Código de status: {response.status_code}')
