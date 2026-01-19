from os import getenv
from pgvector.peewee import VectorField
from peewee import PostgresqlDatabase, Model, TextField, ForeignKeyField, IntegerField

from constants import PREDEFINED_TAGS

db = PostgresqlDatabase(
    database=getenv("DB_NAME"),
    host=getenv("DB_HOST"),
    port=int(getenv("DB_PORT")),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
)

class Documents(Model):
    name = TextField()
    class Meta:
        database = db
        db_table = 'documents'

class Tags(Model):
    name = TextField(unique=True)
    class Meta:
        database = db
        db_table = 'tags'

def seed_tags():
    with db.atomic():
        (
            Tags
            .insert_many(
                [{"name": name.strip().lower()} for name in PREDEFINED_TAGS]
            )
            .on_conflict_ignore()
            .execute()
        )


class DocumentTags(Model):
    document_id = ForeignKeyField(Documents, backref='document_tags', on_delete='CASCADE')
    tag_id = ForeignKeyField(Tags, backref='tag_documents', on_delete='CASCADE')
    class Meta:
        database = db
        db_table = 'document_tags'

class DocumentInformationChunks(Model):
    document_id = ForeignKeyField(Documents, backref='document_information_chunks', on_delete='CASCADE')
    chunk_index= IntegerField()
    page_index = IntegerField()
    chunk_content = TextField()
    embedding = VectorField(dimensions=768)
    class Meta:
        database = db
        db_table = 'document_information_chunks'


db.connect()
db.create_tables([Documents, Tags, DocumentTags, DocumentInformationChunks], safe=True)
seed_tags()

def set_diskann_query_rescore(k: int = 100):
    """
    Set the DiskANN top-K exact rescore parameter for pgvector vector search.
    This ensures the top `k` approximate results are rescored exactly.
    """
    with db.atomic():
        db.execute_sql(f"SET diskann.query_rescore_k = {k};")