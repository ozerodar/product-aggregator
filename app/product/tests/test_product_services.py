"""Tests for services that are used in product module"""

from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from product.services import register_product


class ProductServicesTest(SimpleTestCase):
    """Test for product services"""

    @patch('requests.post')  # This mocks 'requests.post'
    @patch('product.services.get_token', autospec=True)
    def test_register_product(self, mock_post, mock_get_token):
        """Test that the product was registered at an external service after creation"""

        mock_get_token.return_value = 'fake token'
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
        mock_post.raise_for_status = Mock()

        payload = {"name": "Test Product", "description": "This is a test product"}
        register_product(payload)

        # Check that the mock POST was called
        mock_post.assert_called_once()
        mock_get_token.assert_called_once()
