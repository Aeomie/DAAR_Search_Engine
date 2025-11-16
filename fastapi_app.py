# fastapi_app.py
from fastapi import FastAPI
from engine import engine_text


from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    pattern: str
    texts: List[str]  # can handle one or multiple titles
    verbose: bool = False


app = FastAPI()

@app.post("/searchRegex")
def search_regex(pattern: str, text: str, verbose: bool = False):
    result = engine_text(pattern, text, mode="regex", verbose=verbose)
    return result


@app.post("/searchBoyer")
def search_boyer(request: SearchRequest):
    results = []
    for text in request.texts:
        engine_result = engine_text(
            request.pattern,
            text,
            mode="boyer",
            verbose=request.verbose  # always get total_count & indexes
        )
        if request.verbose:
            results.append({
                "text": text,
                "total_count": engine_result.get("total_count", 0),
                "indexes": engine_result.get("indexes", [])
            })
        else:
            results.append({
                "text": text,
                "total_count": engine_result.get("total_count", 0)
            })
    return {"results": results}

