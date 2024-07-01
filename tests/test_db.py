import pytest
from django.db import connections
from django.db.utils import OperationalError

@pytest.mark.django_db
def test_database_connection():
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        pytest.fail("Database connection failed")
