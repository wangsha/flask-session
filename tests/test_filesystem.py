import tempfile

import flask
from flask_session.filesystem import FileSystemSession


class TestFileSystemSession:

    def retrieve_stored_session(self, key, app):
        return app.session_interface.cache.get(key)

    def test_filesystem_default(self, app_utils):
        app = app_utils.create_app(
            {"SESSION_TYPE": "filesystem", "SESSION_FILE_DIR": tempfile.gettempdir()}
        )

        # Should be using FileSystem
        with app.test_request_context():
            assert isinstance(
                flask.session,
                FileSystemSession,
            )
            app_utils.test_session(app)

            # Check if the session is stored in the filesystem
            cookie = app_utils.test_session_with_cookie(app)
            session_id = cookie.split(";")[0].split("=")[1]
            stored_session = self.retrieve_stored_session(f"session:{session_id}", app)
            assert stored_session.get("value") == "44"
