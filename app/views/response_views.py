from typing import List, Optional, Any, Dict
from fastapi.responses import JSONResponse
from fastapi import status


class Api:
    """Classe para padronizar respostas da API"""
    
    @staticmethod
    def success(
        data: Any = None, 
        message: str = "Operação realizada com sucesso",
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        """Resposta de sucesso padrão"""
        response_content = {
            "success": True,
            "message": message,
            "data": data
        }
        return JSONResponse(
            content=response_content,
            status_code=status_code
        )
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "Recurso criado com sucesso"
    ) -> JSONResponse:
        """Resposta para criação de recursos"""
        return Api.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def error(
        message: str = "Erro interno do servidor",
        errors: Optional[Dict] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> JSONResponse:
        """Resposta de erro padrão"""
        response_content = {
            "success": False,
            "message": message,
            "errors": errors
        }
        return JSONResponse(
            content=response_content,
            status_code=status_code
        )
    
    @staticmethod
    def not_found(message: str = "Recurso não encontrado") -> JSONResponse:
        """Resposta para recursos não encontrados"""
        return Api.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def validation_error(errors: Dict) -> JSONResponse:
        """Resposta para erros de validação"""
        return Api.error(
            message="Erro de validação",
            errors=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    @staticmethod
    def paginated(
        data: List[Any],
        total: int,
        page: int,
        per_page: int,
        message: str = "Dados recuperados com sucesso"
    ) -> JSONResponse:
        """Resposta paginada padrão"""
        total_pages = (total + per_page - 1) // per_page
        
        response_content = {
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        return JSONResponse(content=response_content)


class PropertyView:
    """Views específicas para propriedades"""
    
    @staticmethod
    def list_response(properties: List[Any], message: str = "Propriedades listadas com sucesso"):
        """Resposta para listagem de propriedades"""
        return Api.success(data=properties, message=message)
    
    @staticmethod
    def detail_response(property_obj: Any, message: str = "Propriedade encontrada"):
        """Resposta para detalhes de propriedade"""
        return Api.success(data=property_obj, message=message)
    
    @staticmethod
    def created_response(property_obj: Any):
        """Resposta para propriedade criada"""
        return Api.created(
            data=property_obj,
            message="Propriedade criada com sucesso"
        )
    
    @staticmethod
    def updated_response(property_obj: Any):
        """Resposta para propriedade atualizada"""
        return Api.success(
            data=property_obj,
            message="Propriedade atualizada com sucesso"
        )
    
    @staticmethod
    def deleted_response():
        """Resposta para propriedade deletada"""
        return Api.success(
            message="Propriedade deletada com sucesso"
        )
    
    @staticmethod
    def status_updated_response(property_obj: Any):
        """Resposta para status atualizado"""
        return Api.success(
            data=property_obj,
            message="Status da propriedade atualizado com sucesso"
        )


class TenantView:
    """Views específicas para inquilinos"""
    
    @staticmethod
    def list_response(tenants: List[Any], message: str = "Inquilinos listados com sucesso"):
        """Resposta para listagem de inquilinos"""
        return Api.success(data=tenants, message=message)
    
    @staticmethod
    def detail_response(tenant_obj: Any, message: str = "Inquilino encontrado"):
        """Resposta para detalhes de inquilino"""
        return Api.success(data=tenant_obj, message=message)
    
    @staticmethod
    def created_response(tenant_obj: Any):
        """Resposta para inquilino criado"""
        return Api.created(
            data=tenant_obj,
            message="Inquilino criado com sucesso"
        )
    
    @staticmethod
    def updated_response(tenant_obj: Any):
        """Resposta para inquilino atualizado"""
        return Api.success(
            data=tenant_obj,
            message="Inquilino atualizado com sucesso"
        )
    
    @staticmethod
    def deleted_response():
        """Resposta para inquilino deletado"""
        return Api.success(
            message="Inquilino deletado com sucesso"
        )