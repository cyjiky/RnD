from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from typing import List

from sheets_service import SheetService
from dtos import Coordinate

load_dotenv()

sheets_router = APIRouter()

main_service = SheetService()
sheet_id = os.getenv("SHEETS_ID")


@sheets_router.get("/")
def HelloWorld():
    return {"message:": "Hello World!"}


@sheets_router.post("/coordinates")
def coordinates(cords_results: List[Coordinate]):
    if not sheet_id:
        raise HTTPException(status_code=500, detail="Sheets ID not configured in .env")
    try:
        val = []

        for p in cords_results:
            row = ["X", p.X, "Y", p.Y]

            if p.Step is not None:
                row.extend(["Step", p.Step])

            val.append(row)

        data_list = {"range": "Лист1!A1", "values": val}

        body = {
            "valueInputOption": "USER_ENTERED",
            "data": data_list,
            "includeValuesInResponse": True,
            "responseValueRenderOption": "UNFORMATTED_VALUE",
        }

        resp = (
            main_service.spreadsheets()
            .values()
            .batchUpdate(
                spreadsheetId=sheet_id,
                body=body,
            )
            .execute()
        )

        return {"status": "succeess", "responce": resp}
    except Exception as e:
        return {"status": "error", "message": str(e)}
