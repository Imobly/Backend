from fastapi import status


class TestAuthEndpoints:
    """Testes dos endpoints de autenticação"""

    def test_register_user(self, client):
        """Testar registro de novo usuário"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "senha123",
            "full_name": "New User",
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert data["is_active"] is True
        assert data["is_superuser"] is False
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client):
        """Testar registro com email duplicado"""
        user_data = {
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "senha123",
        }

        # Primeiro registro deve funcionar
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Segundo registro com mesmo email deve falhar
        user_data["username"] = "user2"
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email já cadastrado" in response.json()["detail"]

    def test_register_duplicate_username(self, client):
        """Testar registro com username duplicado"""
        user_data = {
            "email": "user1@example.com",
            "username": "duplicateuser",
            "password": "senha123",
        }

        # Primeiro registro deve funcionar
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Segundo registro com mesmo username deve falhar
        user_data["email"] = "user2@example.com"
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username já está em uso" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Testar registro com email inválido"""
        user_data = {
            "email": "invalidemail",
            "username": "testuser",
            "password": "senha123",
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_weak_password(self, client):
        """Testar registro com senha fraca"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "123",  # Muito curta
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_success(self, client, sample_user):
        """Testar login com credenciais válidas"""
        login_data = {"username": sample_user["username"], "password": "senha123"}

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_with_email(self, client, sample_user):
        """Testar login usando email ao invés de username"""
        login_data = {"username": sample_user["email"], "password": "senha123"}

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client, sample_user):
        """Testar login com senha incorreta"""
        login_data = {"username": sample_user["username"], "password": "senhaerrada"}

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Credenciais inválidas" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Testar login com usuário inexistente"""
        login_data = {"username": "naoexiste", "password": "senha123"}

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me(self, client, auth_headers):
        """Testar obtenção de dados do usuário autenticado"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "username" in data
        assert "password" not in data
        assert "hashed_password" not in data

    def test_get_me_without_token(self, client):
        """Testar obtenção de perfil sem token"""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_me_invalid_token(self, client):
        """Testar obtenção de perfil com token inválido"""
        headers = {"Authorization": "Bearer token_invalido"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_me(self, client, auth_headers):
        """Testar atualização de dados do usuário"""
        update_data = {
            "full_name": "Nome Atualizado",
            "email": "novoemail@example.com",
        }

        response = client.put("/api/v1/auth/me", headers=auth_headers, json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["email"] == update_data["email"]

    def test_change_password(self, client, auth_headers):
        """Testar alteração de senha"""
        password_data = {"current_password": "senha123", "new_password": "novasenha456"}

        response = client.post(
            "/api/v1/auth/change-password", headers=auth_headers, json=password_data
        )

        assert response.status_code == status.HTTP_200_OK
        assert "sucesso" in response.json()["message"].lower()

        # Verificar que consegue fazer login com nova senha
        login_data = {"username": "testuser", "password": "novasenha456"}
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK

    def test_change_password_wrong_current(self, client, auth_headers):
        """Testar alteração de senha com senha atual incorreta"""
        password_data = {
            "current_password": "senhaerrada",
            "new_password": "novasenha456",
        }

        response = client.post(
            "/api/v1/auth/change-password", headers=auth_headers, json=password_data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "incorreta" in response.json()["detail"].lower()
