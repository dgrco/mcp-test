from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import json, os, asyncio

app = Server("mcp-learn")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="read_document",
            description="Read a process document by filename",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The document filename"}
                },
                "required": ["filename"]
            }
        ),
        types.Tool(
            name="search_documents",
            description="Search all documents for a keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Keyword to search for"}
                },
                "required": ["keyword"]
            }
        ),
        types.Tool(
            name="get_compliance_rules",
            description="Get compliance rules for a specific hazard class",
            inputSchema={
                "type": "object",
                "properties": {
                    "hazard_class": {"type": "string"}
                },
                "required": ["hazard_class"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "read_document":
        path = os.path.join(DATA_DIR, arguments["filename"])
        if not os.path.exists(path):
            return [types.TextContent(type="text", text=f"File not found: {arguments['filename']}")]
        with open(path) as f:
            return [types.TextContent(type="text", text=f.read())]

    elif name == "search_documents":
        keyword = arguments["keyword"]
        results = []
        for fname in os.listdir(DATA_DIR):
            fpath = os.path.join(DATA_DIR, fname)
            with open(fpath) as f:
                content = f.read()
            if keyword in content.lower():
                results.append(f"[{fname}]\n{content}")
            return [types.TextContent(type="text", text="\n\n".join(results) if results else "No matches found.")]
    
    elif name == "get_compliance_rules":
        rules = {
            "flammable liquid": "Store away from ignition sources. Inspect every 90 days. CO2 suppression required.",
            "corrosive": "PPE required at all times. Neutralisation kit on-site. Weekly inspections.",
        }
        hazard = arguments["hazard_class"].lower()
        for key, rule in rules.items():
            if key in hazard:
                return [types.TextContent(type="text", text=rule)]
        return [types.TextContent(type="text", text="No specific rules found for this hazard class.")]

    return [types.TextContent(type="text", text="Unknown tool")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
