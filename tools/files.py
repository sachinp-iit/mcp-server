import os


def register(mcp):
    @mcp.tool()
    def list_files(path: str = ".") -> list:
        """List files in a directory."""
        return os.listdir(path)

def list_files(path: str = ".") -> list:
    return os.listdir(path)