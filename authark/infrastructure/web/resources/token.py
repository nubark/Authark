from typing import Any, Dict, Tuple
from flask import request, jsonify
from flask.views import MethodView
from ..schemas import TokenRequestSchema, TokenSchema


class TokenResource(MethodView):

    def __init__(self, resolver) -> None:
        self.session_coordinator = resolver['SessionCoordinator']
        self.auth_coordinator = resolver['AuthCoordinator']
        self.tenant_supplier = resolver['TenantSupplier']

    def get(self) -> str:
        return "Authentication endpoint. Please 'Post' to '/auth'"

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Request token.
        tags:
          - Tokens
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenRequest'
        responses:
          201:
            description: "Token created"
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Token"
        """

        token_request_dict = TokenRequestSchema().load(request.data)
        tenant_dict = self.tenant_supplier.get_tenant(
            token_request_dict['tenant'])
        self.session_coordinator.set_tenant(tenant_dict)

        if 'refresh_token' in token_request_dict:
            tokens = self.auth_coordinator.refresh_authenticate(
                token_request_dict['refresh_token'])
        else:
            username = token_request_dict.get('username')
            password = token_request_dict.get('password')
            client = token_request_dict.get('client')
            tokens = self.auth_coordinator.authenticate(
                username, password, client)

        token_dict = TokenSchema()

        return jsonify(tokens), 200
