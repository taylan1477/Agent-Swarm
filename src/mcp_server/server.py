import asyncio
import os
import psycopg2
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

app = Server("jarvis-memory-mcp")

# Database connection details (match with docker-compose.yml)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5433")
DB_NAME = os.environ.get("DB_NAME", "jarvis_memory")
DB_USER = os.environ.get("DB_USER", "jarvis")
DB_PASS = os.environ.get("DB_PASS", "jarvis_password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_memory (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            context TEXT,
            action TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="record_memory",
            description="Record agent's action and context into the shared database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "context": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["agent_id", "context", "action"]
            }
        ),
        types.Tool(
            name="retrieve_memory",
            description="Retrieve the latest memories/actions to understand the current state.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 5}
                },
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "record_memory":
        agent_id = arguments["agent_id"]
        context = arguments.get("context", "")
        action = arguments["action"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO agent_memory (agent_id, context, action) VALUES (%s, %s, %s)", 
                    (agent_id, context, action))
        conn.commit()
        cur.close()
        conn.close()
        return [types.TextContent(type="text", text=f"Memory recorded for {agent_id}.")]
        
    elif name == "retrieve_memory":
        limit = arguments.get("limit", 5)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT agent_id, timestamp, context, action FROM agent_memory ORDER BY timestamp DESC LIMIT %s", (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        result = "Recent Memories:\n"
        for row in rows:
            result += f"[{row[1]}] {row[0]}: {row[3]} (Context: {row[2]})\n"
            
        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text="Unknown tool")]

async def main():
    # Initialize the db schema
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Could not initialize DB (is postgres running?): {e}")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
