"""
Serviço centralizado para gerenciamento de uploads de arquivos
Suporta imagens e documentos PDF
"""
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Literal

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


class UploadService:
    """Serviço para gerenciar uploads de arquivos"""

    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx"}
    ALLOWED_ALL_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOCUMENT_EXTENSIONS

    def __init__(self):
        self.base_upload_dir = Path(settings.UPLOAD_DIR)
        self.max_file_size = settings.MAX_FILE_SIZE

    def _validate_file_extension(
        self, filename: str, allowed_types: Literal["image", "document", "all"]
    ) -> bool:
        """Valida a extensão do arquivo"""
        ext = Path(filename).suffix.lower()

        if allowed_types == "image":
            return ext in self.ALLOWED_IMAGE_EXTENSIONS
        elif allowed_types == "document":
            return ext in self.ALLOWED_DOCUMENT_EXTENSIONS
        else:  # all
            return ext in self.ALLOWED_ALL_EXTENSIONS

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Gera um nome único para o arquivo"""
        ext = Path(original_filename).suffix.lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}{ext}"

    async def save_file(
        self,
        file: UploadFile,
        folder: str,
        allowed_types: Literal["image", "document", "all"] = "all",
    ) -> dict:
        """
        Salva um arquivo no diretório de uploads

        Args:
            file: Arquivo a ser salvo
            folder: Subpasta dentro de uploads (ex: 'properties', 'tenants')
            allowed_types: Tipo de arquivo permitido ('image', 'document', 'all')

        Returns:
            dict com informações do arquivo salvo {filename, url, size, type}
        """
        # Validar extensão
        if not self._validate_file_extension(file.filename, allowed_types):
            allowed_exts = (
                self.ALLOWED_IMAGE_EXTENSIONS
                if allowed_types == "image"
                else self.ALLOWED_DOCUMENT_EXTENSIONS
                if allowed_types == "document"
                else self.ALLOWED_ALL_EXTENSIONS
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido. Extensões aceitas: {', '.join(allowed_exts)}",
            )

        # Ler conteúdo do arquivo
        content = await file.read()
        file_size = len(content)

        # Validar tamanho
        if file_size > self.max_file_size:
            max_mb = self.max_file_size / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo muito grande. Tamanho máximo: {max_mb}MB",
            )

        # Criar diretório se não existir
        upload_folder = self.base_upload_dir / folder
        upload_folder.mkdir(parents=True, exist_ok=True)

        # Gerar nome único e salvar arquivo
        unique_filename = self._generate_unique_filename(file.filename)
        file_path = upload_folder / unique_filename

        with open(file_path, "wb") as f:
            f.write(content)

        # Retornar informações do arquivo
        file_url = f"/uploads/{folder}/{unique_filename}"
        file_type = Path(file.filename).suffix.lower()[1:]  # Remove o ponto

        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "url": file_url,
            "size": file_size,
            "type": file_type,
        }

    async def save_multiple_files(
        self,
        files: List[UploadFile],
        folder: str,
        allowed_types: Literal["image", "document", "all"] = "all",
        max_files: int = 10,
    ) -> List[dict]:
        """
        Salva múltiplos arquivos

        Args:
            files: Lista de arquivos
            folder: Subpasta dentro de uploads
            allowed_types: Tipo de arquivo permitido
            max_files: Número máximo de arquivos permitidos

        Returns:
            Lista de dicts com informações dos arquivos salvos
        """
        if len(files) > max_files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número máximo de arquivos excedido. Máximo: {max_files}",
            )

        saved_files = []
        for file in files:
            file_info = await self.save_file(file, folder, allowed_types)
            saved_files.append(file_info)

        return saved_files

    def delete_file(self, file_url: str) -> bool:
        """
        Deleta um arquivo do sistema

        Args:
            file_url: URL do arquivo (ex: /uploads/properties/20231116_abc123.jpg)

        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            # Remover '/uploads/' do início da URL
            relative_path = file_url.replace("/uploads/", "")
            file_path = self.base_upload_dir / relative_path

            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def delete_multiple_files(self, file_urls: List[str]) -> dict:
        """
        Deleta múltiplos arquivos

        Args:
            file_urls: Lista de URLs dos arquivos

        Returns:
            dict com estatísticas {deleted: int, failed: int}
        """
        deleted = 0
        failed = 0

        for url in file_urls:
            if self.delete_file(url):
                deleted += 1
            else:
                failed += 1

        return {"deleted": deleted, "failed": failed}


# Instância singleton do serviço de upload
upload_service = UploadService()
