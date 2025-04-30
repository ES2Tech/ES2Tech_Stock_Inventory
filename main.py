from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

class EditRequest(BaseModel):
    row_number: int
    values: list[str]

@app.post("/edit")
def edit_row(data: EditRequest):
    service = build('sheets', 'v4', credentials=credentials)
    sheet_id = "YOUR_SHEET_ID"
    range_str = f"Sheet1!A{data.row_number}:R{data.row_number}"

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_str,
        valueInputOption="USER_ENTERED",
        body={"values": [data.values]}
    ).execute()
    return {"status": "수정됨", "updatedCells": result.get("updatedCells", 0)}

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://es2tech.github.io"],  # 또는 로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경변수에서 인증 정보 가져오기
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# 스프레드시트 설정
SPREADSHEET_ID = "1FzxaxY9bmx2lY9QXCPADwHuHKqwhlNr4Q0_D-r8SsvE"
RANGE = "Sheet1"

# POST로 받을 데이터 모델
class RowData(BaseModel):
    values: list

@app.post("/append")
def append_row(row: RowData):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [row.values]}
    ).execute()
    return {"status": "추가됨"}
