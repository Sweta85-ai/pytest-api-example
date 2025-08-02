from jsonschema import validate
import pytest
import schemas
import api_helpers
import uuid
from hamcrest import assert_that, contains_string, is_


@pytest.fixture
def create_pet_and_order():
    """
    Creates a new pet and places an order for it.
    Returns:
        (order_id, pet_id)
    """
    pet_id = int(uuid.uuid4().int % 10000)
    pet_data = {
        "id": pet_id,
        "name": f"pet_{pet_id}",
        "type": "dog",
        "status": "available"
    }

    # Create pet
    post_pet = api_helpers.post_api_data("/pets/", pet_data)
    assert post_pet.status_code == 201

    # Create order
    order_data = {
        "pet_id": pet_id
    }
    post_order = api_helpers.post_api_data("/store/order", order_data)
    assert post_order.status_code == 201

    order_json = post_order.json()
    validate(instance=order_json, schema=schemas.order)

    return order_json["id"], pet_id

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
def test_patch_order_by_id(create_pet_and_order):
    """
    Tests PATCH endpoint for updating an order's status.
    """
    order_id, pet_id = create_pet_and_order

    # Update the order status to 'sold'
    update_data = {
        "status": "sold"
    }

    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", update_data)
    assert patch_response.status_code == 200

    json_response = patch_response.json()
    assert json_response["message"] == "Order and pet status updated successfully"

    # Validate PATCH response schema
    validate(instance=json_response, schema=schemas.success_message)

    # Verify pet status has changed to 'sold'
    pet_response = api_helpers.get_api_data(f"/pets/{pet_id}")
    assert pet_response.status_code == 200
    pet_json = pet_response.json()

    validate(instance=pet_json, schema=schemas.pet)
    assert pet_json["status"] == "sold"
