import pytest
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mcp_server"))

from server import call_tool

@pytest.mark.asyncio
async def test_read_document():
    result = await call_tool("read_document", {"filename": "sample_doc.txt"})
    assert "RV-101" in result[0].text

@pytest.mark.asyncio
async def test_search_documents():
    result = await call_tool("search_documents", {"keyword": "temperature"})
    assert "250" in result[0].text

@pytest.mark.asyncio
async def test_search_no_results():
    result = await call_tool("search_documents", {"keyword": "xyznonexistent"})
    assert "No matches" in result[0].text

@pytest.mark.asyncio
async def test_compliance_rules_found():
    result = await call_tool("get_compliance_rules", {"hazard_class": "Flammable liquid, Category 2"})
    assert "CO2" in result[0].text

@pytest.mark.asyncio
async def test_compliance_rules_unknown():
    result = await call_tool("get_compliance_rules", {"hazard_class": "radioactive"})
    assert "No specific rules" in result[0].text
