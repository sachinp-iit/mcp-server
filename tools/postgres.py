import os

import psycopg2

# Hard block dangerous SQL
BLOCKED_SQL_KEYWORDS = {
    "DROP",
    "TRUNCATE",
    "ALTER"
}

# Function to validate incoming postgresql queries against the Blocked Keyword
def validate_sql(sql: str):
    sql_upper = sql.upper()
    
    # Check whether the blocked keywords are part of any postgresql query
    for keyword in BLOCKED_SQL_KEYWORDS:
        if keyword in sql_upper:
            raise ValueError(f"Blocked SQL operation: {keyword}")


# PostgreSQL Executor Class
class PostgresExecutor:
    # Constructor to retrieve connectionstring from the Environment Variable
    def __init__(self):
        self.conn_str = os.getenv("NEON_DB_URL")
        if not self.conn_str:
            raise RuntimeError("NEON_DB_URL is not set")

    # Function to execute Postgresql Queries which are valid and not blocked queries
    def execute(self, query: str):
        validate_sql(query)
        with psycopg2.connect(self.conn_str) as conn, conn.cursor() as cur:
            cur.execute(query)
            if cur.description:
                return cur.fetchall()
            return {"rows_affected": cur.rowcount}
            
# Function to fetch entire postgresql metadata
def fetch_schema_metadata():
    sql = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    with psycopg2.connect(os.getenv("NEON_DB_URL")) as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

# Function to register tools i.e. creating a toolset
def register(mcp):
    executor = PostgresExecutor()

    # Creating Individual Tool
    @mcp.tool()
    def execute_sql(query: str):
        return executor.execute(query)

    # Creating Individual Tool
    @mcp.tool()
    def get_schema():
        return fetch_schema_metadata()

_executor = None

def _get_executor():
    global _executor
    if _executor is None:
        _executor = PostgresExecutor()
    return _executor

def execute_sql(query: str):
    return _get_executor().execute(query)

def get_schema():
    return fetch_schema_metadata()
