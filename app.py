from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from translator import Translator

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{word}")
async def root(word: str):
    wt = Translator(word)
    return wt.run()
