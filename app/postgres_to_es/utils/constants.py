INDEX_NAME = 'movies'
DOCUMENT_BODY = {
    '_index': INDEX_NAME,
    '_id': None,
    '_source': {}
}

HOST = 'http://localhost'
PORT = 9200

LOGS_FORMAT = "|\t%(asctime)s – [%(levelname)s]: %(message)s. " \
              "Исполняемый файл – '%(filename)s': " \
              "функция – '%(funcName)s'(%(lineno)d)"
