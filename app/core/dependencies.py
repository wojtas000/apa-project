from fastapi import Request, Depends

def get_ner_model(request: Request):
    return request.app.state.models["ner"]
