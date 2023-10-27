import great_expectations as gx
import pandas as pd
import dotenv
import shutil
import os
from datetime import datetime

def load_postgres_instance_datasource_asset(context):
    """ Cria ou carrega o Datasource, o Data Asset e o objeto Batch Request para a validação 
    com o Great Expectations. É a primeira etapa do workflow, sendo a definição dos dados
    que serão validados. Esta função conecta a uma instância de Banco de Dados Postgres.

    Args:
        context (gx.Context): Objeto configurado de Contexto do projeto

    Returns:
        gx.Batch_Request: objeto de batch_request com definição dos dados a serem processados.
    """
    # Environment
    dotenv.load_dotenv()
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT_CONTAINER')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

    POSTGRES_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"


    # Datasource - engine
    datasource_name = "postgres_src"
    datasource = context.datasources.get(datasource_name, None)
    if datasource == None:
        datasource = context.sources.add_postgres(name=datasource_name, connection_string=POSTGRES_URI, )


    # Data Asset - connection
    asset_name = 'listings_asset'
    asset_table_name = "g1_listings"  # SQL table
    list_asset_names = [asset_obj.name for asset_obj in datasource.assets]
    if asset_name in list_asset_names:
        table_asset = datasource.get_asset('reviews', None)
    else:
        table_asset = datasource.add_table_asset(name=asset_name, table_name=asset_table_name, schema_name='raw')
        # add_query_asset
    data_asset = context.get_datasource( datasource_name ).get_asset( asset_name )

    batch_request = table_asset.build_batch_request()
    return batch_request



def load_csv_datasource_asset_raw(context, datasource_name: str, asset_name:str, layer_name='raw'):
    """ Cria ou carrega o Datasource, o Data Asset e o objeto Batch Request para a validação 
    com o Great Expectations. É a primeira etapa do workflow, sendo a definição dos dados
    que serão validados.

    Args:
        context (gx.Context): Objeto configurado de Contexto do projeto
        datasource_name (str): Nome do Datasource.
        asset_name (str): Nome do Asset
        layer_name (str, optional): Nome da camada de dados (raw, trusted ou specs). Defaults to 'raw'.

    Returns:
        gx.Batch_Request: objeto de batch_request com definição dos dados a serem processados.
    """
    
    file_data_regex = asset_name + '\.csv\.gz'
    
    # Datasource - engine
    datasource = context.datasources.get(datasource_name, None)
    if datasource == None:
        datasource = context.sources.add_pandas_filesystem(datasource_name, base_directory='./data')


    # Data Asset - connection
    list_asset_names = [asset_obj.name for asset_obj in datasource.assets]
    if asset_name in list_asset_names:
        table_asset = datasource.get_asset(asset_name)
    else:
        table_asset = datasource.add_csv_asset(asset_name, batching_regex=file_data_regex)

    batch_request = table_asset.build_batch_request()
    return batch_request


def load_df_datasource_asset_trusted(context, df, datasource_name: str, asset_name:str):
    """ Cria ou carrega o Datasource, o Data Asset e o objeto Batch Request para a validação 
    com o Great Expectations. É a primeira etapa do workflow, sendo a definição dos dados
    que serão validados.

    Args:
        context (gx.Context): Objeto configurado de Contexto do projeto
        datasource_name (str): Nome do Datasource.
        asset_name (str): Nome do Asset
        layer_name (str, optional): Nome da camada de dados (raw, trusted ou specs). Defaults to 'raw'.

    Returns:
        gx.Batch_Request: objeto de batch_request com definição dos dados a serem processados.
    """
    # Datasource - engine
    datasource = context.datasources.get(datasource_name, None)
    if datasource == None:
        datasource = context.sources.add_pandas(datasource_name)


    # Data Asset - connection
    list_asset_names = [asset_obj.name for asset_obj in datasource.assets]
    if asset_name in list_asset_names:
        data_asset = datasource.get_asset(asset_name)
    else:
        data_asset = datasource.add_dataframe_asset(name=asset_name)

    batch_request = data_asset.build_batch_request(dataframe=df)
    return batch_request



# Monitoramento RAW - Reviews
def suite_monitoring_execution(
        asset_name: str, 
        datasource_name='airbnb', 
        data_context_path = '.', 
        layer_name='raw', 
        suite_name_str=None,
        batch_request_input=None):
    """ Função de execução do Monitoramento para um dado CSV. Cria o suite ou obtém o existente com o nome
    para criar o Checkpoint de Validação da Qualidade dos dados. Por fim, garante a execução do Checkpoint.

    Args:
        asset_name (str): Nome do asset
        datasource_name (str, optional): Nome do Datasource a ser criado ou usado.. Defaults to 'airbnb'.
        data_context_path (str, optional): Diretório do Data Context. Defaults to '.'.

    Returns:
        checkpoint_result: Resultado da execução do Checkpoint.
    """
    if suite_name_str == None:
        suite_name = f'{layer_name}_{asset_name}'
    else:
        suite_name = f'{layer_name}_{suite_name_str}'

    # Data Context
    context = gx.data_context.FileDataContext.create(project_root_dir=data_context_path)

    # Batch request
    if batch_request_input == None:
        batch_request = load_csv_datasource_asset_raw(
            context=context, datasource_name=datasource_name, asset_name=asset_name, layer_name=layer_name)
    else:
        batch_request = batch_request_input

    # Suite
    if suite_name not in context.list_expectation_suite_names():
        context.add_or_update_expectation_suite(suite_name)

    # Checkpoint Validation
    checkpoint = context.add_or_update_checkpoint(
        name=f"{suite_name}",
        validations=[{
            "batch_request": batch_request,
            "expectation_suite_name": suite_name,
            }])

    checkpoint_result = checkpoint.run(run_name=suite_name)
    return checkpoint_result