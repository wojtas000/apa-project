# Quickstart
1. Install packages with
```
pip install -r requirements.txt
```
2. Copy `.env.example` into `.env` and fill the required environmental variables
3. Start fastAPI server by running
```
fastapi run --reload app/main.py
```
4. Start redis worker for background task processing with
```
python -m scripts.start_worker

```
5. Background task monitoring at `localhost:8000/rq/`
6. Admin panel at `localhost:8000/admin/`