from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, index=True)

    date_created = Column(DateTime(timezone=True),
                          default=datetime.now(timezone.utc))
    date_updated = Column(DateTime(timezone=True), default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Todo {self.title} for user {self.user_id} at {self.date_created}>"
