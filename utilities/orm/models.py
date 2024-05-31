"""Data models for loading and serving VPfG data in the web app.

ORM models serve to document data structures as well as simplify the communication
betweeen object-oriented representation of data in python code with the data in the SQL
database.

It is not necessary to use these ORM models when reading from or writing to the
database, but doing so can simplify and clarify the code as well as provide a level of
data validation.

Examples of usage:

Writing a new row
```
from utilities.orm.methods import get_session

candidate = Candidate(
    candidate_name='Taylor Swift',
    state='TN'
)
with get_session() as session:
    session.add(candidate)
    session.commit()  # SQLAlchemy knows to update the object in the database

```

Fetching a single candidate row from the database using SQLAlchemy querying
```
with get_session() as session:
    candidate = session.query(Candidate).filter(
        Candidate.candidate_name=='Taylor Swift',
        Candidate.state=='TN'
    ).first()
```

Fetching a single candidate row from the database using SQL query and ORM instantiation
```
from utilities.orm.methods import query

response = query(
    '''
    select * from candidate
    where candidate_name = %(name)s and state = %(state)s
    ''',
    parameters={'name': 'Taylor Swift', state='TN'}
)
candidate_data = response[0]
candidate = Candidate(**candidate_data)
```

Updating one row once you have fetched it
```
with get_session() as session:
    candidate = ...
    candidate.office = 'President'
    candidate.updated_at = datetime.datetime.now()
    session.commit()  # SQLAlchemy knows to update the object in the database

```

Deleting a row
```
with get_session() as session:
    candidate = ...
    session.delete(candidate)
    session.commit()

```

"""

import datetime
from typing import Literal

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CanvassResult(Base):
    __tablename__ = "canvass_result"
    canvass_result_id: Mapped[str] = mapped_column(primary_key=True)
    geotag: Mapped[str]
    memo: Mapped[str]
    created_at: Mapped[datetime.datetime]


class BatchAnalysis(Base):
    __tablename__ = "batch_analysis"
    batch_analysis_id: Mapped[str] = mapped_column(primary_key=True)
    gpt_input_prompt: Mapped[str]
    gpt_output: Mapped[str]
    created_at: Mapped[datetime.datetime]
