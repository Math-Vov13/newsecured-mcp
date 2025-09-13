from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from fastmcp.server.auth.providers.jwt import JWTVerifier, RSAKeyPair

# Generate a key pair for testing
key_pair = RSAKeyPair.generate()

# Configure your server with the public key
verifier = JWTVerifier(
    public_key=key_pair.public_key,
    issuer="https://test.yourcompany.com",
    audience="test-mcp-server"
)


mcp = FastMCP(auth=verifier)

@mcp.custom_route("/token", methods=["GET"])
def get_token(request: Request) -> PlainTextResponse:
    # Generate a test token using the private key
    test_token = key_pair.create_token(
        subject="test-user-123",
        issuer="https://test.yourcompany.com", 
        audience="test-mcp-server",
        scopes=["read", "write", "admin"]
    )
    return PlainTextResponse(test_token)

@mcp.tool
def echo_tool(message: str) -> str:
    return message


if __name__ == "__main__":
    mcp.run(transport="streamable-http")