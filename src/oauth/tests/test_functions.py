import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from src.base.services import (get_path_upload_avatar,
                               get_path_upload_cover_album,
                               get_path_upload_track,
                               get_path_upload_cover_playlist,
                               validate_size_image)


class TestFileFunctions(unittest.TestCase):
    def setUp(self):
        class ExampleInstance:
            def __init__(self, id):
                self.id = id

        self.instance = ExampleInstance(id=1)
        self.valid_image = SimpleUploadedFile(
            "image.jpg", b"file_content", content_type="image/jpeg"
        )
        self.large_image = SimpleUploadedFile(
            "large_image.jpg", b"file_content" * 5000000, content_type="image/jpeg"
        )

    def test_get_path_upload_avatar(self):
        expected_path = "avatar/user_1/image.jpg"
        path = get_path_upload_avatar(self.instance, "image.jpg")
        self.assertEqual(path, expected_path)

    def test_get_path_upload_cover_album(self):
        expected_path = "album/user_1/image.jpg"
        path = get_path_upload_cover_album(self.instance, "image.jpg")
        self.assertEqual(path, expected_path)

    def test_get_path_upload_track(self):
        expected_path = "track/user_1/image.jpg"
        path = get_path_upload_track(self.instance, "image.jpg")
        self.assertEqual(path, expected_path)

    def test_get_path_upload_cover_playlist(self):
        expected_path = "playlist/user_1/image.jpg"
        path = get_path_upload_cover_playlist(self.instance, "image.jpg")
        self.assertEqual(path, expected_path)

    def test_validate_size_image_valid(self):
        try:
            validate_size_image(self.valid_image)
        except ValidationError:
            self.fail("validate_size_image raised ValidationError unexpectedly!")

    def test_validate_size_image_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            validate_size_image(self.large_image)
        exception = cm.exception
        self.assertEqual(exception.args[0], "Max size of file 2MB")
