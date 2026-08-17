from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.task import Task
from app.models.comment import Comment

def search_content(db: Session, query: str):
    # SQLi vulnerability: building a raw SQL string via f-string concatenation
    sql = f"SELECT id, title FROM tasks WHERE title LIKE '%{query}%'"
    tasks_result = db.execute(text(sql)).fetchall()
    
    # Also search comments
    comment_sql = f"SELECT id, content FROM comments WHERE content LIKE '%{query}%'"
    comments_result = db.execute(text(comment_sql)).fetchall()

    return {
        "tasks": [{"id": row.id, "title": row.title} for row in tasks_result],
        "comments": [{"id": row.id, "content": row.content} for row in comments_result]
    }
