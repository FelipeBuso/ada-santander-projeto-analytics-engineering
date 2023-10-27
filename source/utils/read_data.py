import pandas as pd
import os


class ReadFile:
    """
    Classe para leitura e retorno de um dataframe a partir de um arquivo
    """

    def __init__(self) -> None:
        pass

    def read_csv_to_dataframe(
        self, directory, file_name, delimiter=",", compression=None
    ) -> pd.DataFrame:
        """
        Lê um arquivo CSV e retorna um DataFrame.

        Args:
            directory (str): O diretório onde o arquivo está localizado.
            file_name (str): O nome do arquivo CSV (com ou sem extensão .csv).
            delimiter (str): Caracter usado para separar cada linha.
            compression (str, optional): O tipo de compressão (por exemplo, 'gzip', 'zip', 'bz2', 'xz', None para não comprimido).

        Returns:
            pandas.DataFrame: O DataFrame criado a partir do arquivo CSV.
        """

        file_path = os.path.join(directory, file_name)

        try:
            if compression is None:
                df = pd.read_csv(file_path, delimiter=delimiter)
            else:
                df = pd.read_csv(
                    file_path, delimiter=delimiter, compression=compression
                )
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo CSV: {str(e)}")
