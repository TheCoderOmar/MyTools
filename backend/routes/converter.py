from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.converter_service import xml_to_json, json_to_xml

router = APIRouter()

class ConvertRequest(BaseModel):
    content: str

class ConvertResponse(BaseModel):
    converted: str

@router.post("/xml-to-json", response_model=ConvertResponse)
async def convert_xml_to_json(request: ConvertRequest):
    """Convert XML to JSON"""
    try:
        result = xml_to_json(request.content)
        return ConvertResponse(converted=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Conversion failed: {str(e)}")

@router.post("/json-to-xml", response_model=ConvertResponse)
async def convert_json_to_xml(request: ConvertRequest):
    """Convert JSON to XML"""
    try:
        result = json_to_xml(request.content)
        return ConvertResponse(converted=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Conversion failed: {str(e)}")