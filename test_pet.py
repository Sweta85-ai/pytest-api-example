from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''

@pytest.fixture
def setup_pet_with_status():
    def _create(status):
        pet_id = int(uuid.uuid4().int % 10000)
        pet_data = {
            "id": pet_id,
            "name": f"pet_{pet_id}",
            "type": "cat",
            "status": status
        }
        response = api_helpers.post_api_data("/pets/", pet_data)
        assert response.status_code == 201
        return pet_id, pet_data
    return _create



@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status, setup_pet_with_status):
    pet_id, pet_data = setup_pet_with_status(status)
    test_endpoint = "/pets/findByStatus"
    params = {"status": status}

    response = api_helpers.get_api_data(test_endpoint, params)
    
    assert response.status_code == 200

    pets = response.json()
    assert any(p["id"] == pet_id for p in pets)
    for pet in pets:
        assert pet["status"] == status
        validate(instance=pet, schema=schemas.pet)    

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("invalid_id", [-1, 1000, 9999])
def test_get_by_id_404(invalid_id):
    test_endpoint = f"/pets/{invalid_id}"
    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404
    assert_that(response.text, contains_string("not found"))
