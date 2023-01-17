import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ElasticConnection:
    def __init__(self, credential_url: str) -> None:
        self.es_server = Elasticsearch(
            [credential_url],
            verify_certs=False,
            ssl_show_warn=False,
            timeout=30,
            max_retries=10,
            retry_on_timeout=True,
        )
    def get_api_calls(self, index: str, query: dict) -> list[dict]:

        try:
            hits = [hit['_source'] for hit in elasticsearch.helpers.scan(self.es_server, index=index, query=query, size=10000)]
            
            if not hits:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No data",
                )

            return hits
            
        except RequestError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Request Error"
            )

        except HTTPException:
            raise
        
        except Exception as e:
            logger.critical(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")