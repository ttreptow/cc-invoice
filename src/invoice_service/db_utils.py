from contextlib import contextmanager


@contextmanager
def scoped_session(session_maker):
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
