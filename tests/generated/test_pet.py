import requests
import pytest
import time
import json

BASE_URL = "https://petstore.swagger.io/v2"
PET_ENDPOINT = f"{BASE_URL}/pet"

# Helper function to generate a unique pet ID
def generate_unique_pet_id():
    """Generates a large, unique integer ID for pets."""
    # Using time.time_ns() for a high-resolution, unique integer ID
    return int(time.time_ns() / 1000) # Divide by 1000 to keep it within typical 64-bit integer range if needed

# Helper function to create a default valid pet payload
def create_valid_pet_payload(pet_id=None, name=None, status="available"):
    """
    Creates a dictionary representing a valid pet payload.
    Includes 'photoUrls' as it's a required field by the Swagger spec for POST /pet.
    """
    if pet_id is None:
        pet_id = generate_unique_pet_id()
    if name is None:
        name = f"TestPet_{pet_id}"
    return {
        "id": pet_id,
        "name": name,
        "photoUrls": ["http://example.com/photo.jpg"], # Required by Petstore API spec
        "status": status
    }

# --- Positive Test Cases ---
class TestCreatePetPositive:

    @pytest.mark.parametrize("status_value", ["available", "pending", "sold"])
    def test_create_pet_with_valid_status(self, status_value):
        """
        Test creating a pet with valid 'id', 'name', and 'status' set to 'available', 'pending', or 'sold'.
        """
        pet_id = generate_unique_pet_id()
        payload = create_valid_pet_payload(pet_id=pet_id, status=status_value)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for status '{status_value}', but got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == payload["name"]
        assert response_data["status"] == status_value

    @pytest.mark.parametrize("pet_name", [
        "My Pet-1!",
        "Doggo 2000",
        "Fluffy McFlufferson with spaces and special chars!@#$",
        "Pet Name with Numbers 12345"
    ])
    def test_create_pet_with_name_containing_spaces_special_chars_and_numbers(self, pet_name):
        """
        Test creating a pet with 'name' containing spaces, special characters, and numbers.
        """
        pet_id = generate_unique_pet_id()
        payload = create_valid_pet_payload(pet_id=pet_id, name=pet_name)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for name '{pet_name}', but got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == pet_name
        assert response_data["status"] == payload["status"]

# --- Negative Test Cases ---
class TestCreatePetNegative:

    @pytest.mark.parametrize("missing_field", ["id", "name", "status"])
    def test_create_pet_with_missing_required_field(self, missing_field):
        """
        Test attempting to create a pet with a missing required field ('id', 'name', or 'status').
        The Petstore API exhibits inconsistent error handling: 500 for missing 'id', 400 for 'name'/'status'.
        """
        payload = create_valid_pet_payload()
        del payload[missing_field]
        response = requests.post(PET_ENDPOINT, json=payload)

        expected_status_code = 500 if missing_field == "id" else 400
        assert response.status_code == expected_status_code, \
            f"Expected status code {expected_status_code} for missing '{missing_field}', got {response.status_code}. Response: {response.text}"

    @pytest.mark.parametrize("invalid_id_type", ["abc", 123.45, True])
    def test_create_pet_with_invalid_id_type(self, invalid_id_type):
        """
        Test attempting to create a pet where 'id' is a string, float, or boolean.
        The Petstore API returns 500 for these invalid ID types.
        """
        payload = create_valid_pet_payload(pet_id=invalid_id_type)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 500, \
            f"Expected status code 500 for invalid ID type '{type(invalid_id_type).__name__}', got {response.status_code}. Response: {response.text}"

    @pytest.mark.parametrize("invalid_name_type", [123, False])
    def test_create_pet_with_invalid_name_type(self, invalid_name_type):
        """
        Test attempting to create a pet where 'name' is an integer or boolean.
        The Petstore API returns 400 for these invalid 'name' types.
        """
        payload = create_valid_pet_payload(name=invalid_name_type)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 400, \
            f"Expected status code 400 for invalid name type '{type(invalid_name_type).__name__}', got {response.status_code}. Response: {response.text}"

    @pytest.mark.parametrize("invalid_status_type", [1, True])
    def test_create_pet_with_invalid_status_type(self, invalid_status_type):
        """
        Test attempting to create a pet where 'status' is an integer or boolean.
        The Petstore API returns 400 for these invalid 'status' types.
        """
        payload = create_valid_pet_payload(status=invalid_status_type)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 400, \
            f"Expected status code 400 for invalid status type '{type(invalid_status_type).__name__}', got {response.status_code}. Response: {response.text}"

    @pytest.mark.parametrize("invalid_status_value", ["unknown", "Available", "PENDING", "sOlD"])
    def test_create_pet_with_invalid_status_enum_or_casing(self, invalid_status_value):
        """
        Test attempting to create a pet with an invalid 'status' enum value or incorrect casing.
        The Petstore API returns 400 for these cases.
        """
        payload = create_valid_pet_payload(status=invalid_status_value)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 400, \
            f"Expected status code 400 for invalid status value '{invalid_status_value}', got {response.status_code}. Response: {response.text}"

    def test_create_pet_with_empty_name_string(self):
        """
        Test attempting to create a pet with 'name' as an empty string.
        The Petstore API returns 400 for an empty 'name' string.
        """
        payload = create_valid_pet_payload(name="")
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 400, \
            f"Expected status code 400 for empty name string, got {response.status_code}. Response: {response.text}"

    @pytest.mark.parametrize("invalid_id_value", [-1, 0])
    def test_create_pet_with_invalid_id_value_negative_or_zero(self, invalid_id_value):
        """
        Test attempting to create a pet with 'id' as a negative integer or zero.
        The Petstore API returns 500 for these invalid ID values.
        """
        payload = create_valid_pet_payload(pet_id=invalid_id_value)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 500, \
            f"Expected status code 500 for ID '{invalid_id_value}', got {response.status_code}. Response: {response.text}"

    def test_create_pet_with_empty_request_body(self):
        """
        Test attempting to create a pet with an empty request body ({}).
        The Petstore API returns 400 as required fields are missing.
        """
        response = requests.post(PET_ENDPOINT, json={})

        assert response.status_code == 400, \
            f"Expected status code 400 for empty request body, got {response.status_code}. Response: {response.text}"

    def test_create_pet_with_malformed_json_request_body(self):
        """
        Test attempting to create a pet with a malformed JSON request body.
        The Petstore API returns 400 for malformed JSON.
        """
        # Malformed JSON string (missing closing brace)
        malformed_json = '{"id": 123, "name": "Malformed", "status": "available",' 
        headers = {'Content-Type': 'application/json'}
        response = requests.post(PET_ENDPOINT, data=malformed_json, headers=headers)

        assert response.status_code == 400, \
            f"Expected status code 400 for malformed JSON, got {response.status_code}. Response: {response.text}"

    def test_create_pet_with_extra_unexpected_fields(self):
        """
        Test attempting to create a pet with extra, unexpected fields in the request body.
        The Petstore API typically ignores extra fields and processes the valid ones, returning 200.
        """
        pet_id = generate_unique_pet_id()
        payload = create_valid_pet_payload(pet_id=pet_id)
        payload["extraField"] = "unexpected_value"
        payload["another_extra"] = 123
        payload["category"] = {"id": 99, "name": "ExtraCategory"} # Also an extra field not explicitly in test plan

        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for request with extra fields, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == payload["name"]
        assert response_data["status"] == payload["status"]
        # Assert that the extra fields are NOT present in the response, as the API typically ignores them.
        assert "extraField" not in response_data
        assert "another_extra" not in response_data
        # The 'category' field is part of the schema, but if not explicitly provided in the base payload,
        # it might be treated as an 'extra' if the API doesn't default it.
        # In this case, the Petstore API *does* include 'category' if provided, so we should check it.
        assert response_data["category"]["id"] == 99
        assert response_data["category"]["name"] == "ExtraCategory"


# --- Boundary Test Cases ---
class TestCreatePetBoundary:

    def test_create_pet_with_max_int_id(self):
        """
        Test creating a pet with 'id' as the maximum allowed 32-bit signed integer value (2147483647).
        """
        max_int_id = 2147483647
        payload = create_valid_pet_payload(pet_id=max_int_id)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for max int ID, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == max_int_id
        assert response_data["name"] == payload["name"]

    def test_create_pet_with_min_positive_int_id(self):
        """
        Test creating a pet with 'id' as the minimum positive integer value (1).
        """
        min_positive_id = 1
        payload = create_valid_pet_payload(pet_id=min_positive_id)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for min positive ID, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == min_positive_id
        assert response_data["name"] == payload["name"]

    def test_create_pet_with_single_character_name(self):
        """
        Test creating a pet with 'name' as a single character string.
        """
        single_char_name = "A"
        pet_id = generate_unique_pet_id()
        payload = create_valid_pet_payload(pet_id=pet_id, name=single_char_name)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for single char name, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == single_char_name

    def test_create_pet_with_very_long_name(self):
        """
        Test creating a pet with 'name' as a very long string (e.g., 255 characters).
        The Petstore API appears to accept very long names without truncation or error.
        """
        long_name = "A" * 255 # 255 characters
        pet_id = generate_unique_pet_id()
        payload = create_valid_pet_payload(pet_id=pet_id, name=long_name)
        response = requests.post(PET_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Expected status code 200 for 255-char name, got {response.status_code}. Response: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == long_name

        # Test with an even longer name (e.g., 1000 characters) to push limits
        long_name_excessive = "B" * 1000
        pet_id_excessive = generate_unique_pet_id()
        payload_excessive = create_valid_pet_payload(pet_id=pet_id_excessive, name=long_name_excessive)
        response_excessive = requests.post(PET_ENDPOINT, json=payload_excessive)

        assert response_excessive.status_code == 200, \
            f"Expected status code 200 for 1000-char name, got {response_excessive.status_code}. Response: {response_excessive.text}"
        
        response_data_excessive = response_excessive.json()
        assert response_data_excessive["id"] == pet_id_excessive
        assert response_data_excessive["name"] == long_name_excessive