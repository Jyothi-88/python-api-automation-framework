import pytest
import responses
from tests.api_client import OrderApiClient
from unittest.mock import MagicMock

BASE_URL = "https://api.example.test/v1"

@responses.activate
def test_create_order_success(order_api_client):
    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
            "country": "India",
        },
        "weight_kg": 25.5,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",        
        json={
            "order_id": "123e4567-e89b-12d3-a456-426614174000",
            "status": "CREATED",
            "price_usd": 125.50,
            "eta": "2026-09-10T10:00:00Z",
        },
        status=201,
    )

    response = order_api_client.create_order(order_data)

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["order_id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert response_data["status"] == "CREATED"
    assert response_data["price_usd"] == 125.50
    assert "eta" in response_data

    request_data = responses.calls[-1].request.body
    assert b'"customer_id": "customer-123"' in request_data
    assert b'"weight_kg": 25.5' in request_data
    assert b'"service_level": "STANDARD"' in request_data

@responses.activate
def test_create_order_rejects_zero_weight(order_api_client):
    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
            "country": "India",
        },
        "weight_kg": 0,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "weight_kg must be greater than 0"},
        status=400,
    )

    response = order_api_client.create_order(order_data)

    assert response.status_code == 400

@responses.activate
def test_create_order_rejects_weight_above_maximum(order_api_client):
    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
            "country": "India",
        },
        "weight_kg": 5000.1,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "weight_kg must not exceed 5000"},
        status=400,
    )

    response = order_api_client.create_order(order_data)

    assert response.status_code == 400

@responses.activate
def test_create_order_rejects_incomplete_pickup_address(order_api_client):
    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            # postal_code intentionally missing
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
            "country": "India",
        },
        "weight_kg": 25.5,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "Incomplete pickup address"},
        status=422,
    )

    response = order_api_client.create_order(order_data)

    assert response.status_code == 422

@responses.activate
def test_create_order_rejects_incomplete_dropoff_address(order_api_client):
    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            # postal_code intentionally missing
            "country": "India",
        },
        "weight_kg": 25.5,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "Incomplete dropoff address"},
        status=422,
    )

    response = order_api_client.create_order(order_data)

    assert response.status_code == 422

@responses.activate
def test_create_order_rejects_missing_authentication():
    client = OrderApiClient(
        BASE_URL,
        token="",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "Authentication required"},
        status=401,
    )

    response = client.create_order({
        "customer_id": "customer-001",
        "weight_kg": 10,
    })

    assert response.status_code == 401
    assert "Authorization" not in responses.calls[-1].request.headers

@responses.activate
def test_create_order_rejects_invalid_authentication():
    client = OrderApiClient(
        BASE_URL,
        token="invalid-token",
    )

    order_data = {
        "customer_id": "customer-123",
        "pickup": {
            "address_line1": "123 Main Street",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        "dropoff": {
            "address_line1": "456 Park Road",
            "city": "Hyderabad",
            "state": "Telangana",
            "postal_code": "500001",
            "country": "India",
        },
        "weight_kg": 25.5,
        "service_level": "STANDARD",
    }

    responses.add(
        responses.POST,
        f"{BASE_URL}/orders",
        json={"detail": "Invalid authentication token"},
        status=401,
    )

    response = client.create_order(order_data)

    assert response.status_code == 401
    assert responses.calls[-1].request.headers["Authorization"] == "Bearer invalid-token"
    
@responses.activate
def test_get_order_success(order_api_client):
    order_id = "123e4567-e89b-12d3-a456-426614174000"

    responses.add(
        responses.GET,
        f"{BASE_URL}/orders/{order_id}",
        json={
            "order_id": order_id,
            "status": "CREATED",
            "price_usd": 125.50,
            "eta": "2026-09-10T10:00:00Z",
            "history": [
                {
                    "status": "CREATED",
                    "timestamp": "2026-09-07T10:00:00Z"
                }
            ],
        },
        status=200,
    )

    response = order_api_client.get_order(order_id)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["order_id"] == order_id
    assert response_data["status"] == "CREATED"
    assert response_data["price_usd"] == 125.50
    assert "eta" in response_data
    assert isinstance(response_data["history"], list)

@responses.activate
def test_get_order_not_found(order_api_client):
    order_id = "00000000-0000-0000-0000-000000000000"

    responses.add(
        responses.GET,
        f"{BASE_URL}/orders/{order_id}",
        json={"detail": "Order not found"},
        status=404,
    )

    response = order_api_client.get_order(order_id)

    assert response.status_code == 404

@pytest.mark.parametrize(
    "current_status, expected_status_code",
    [
        ("CREATED", 204),
        ("PICKED_UP", 204),
        ("IN_TRANSIT", 409),
        ("DELIVERED", 409),
    ],
)
@responses.activate
def test_delete_order_state_rules(
    order_api_client,
    current_status,
    expected_status_code,
):
    order_id = "123e4567-e89b-12d3-a456-426614174000"

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/orders/{order_id}",
        status=expected_status_code,
    )

    response = order_api_client.delete_order(order_id)

    assert response.status_code == expected_status_code

@responses.activate
def test_update_order_status_success(order_api_client):
    order_id = "123e4567-e89b-12d3-a456-426614174000"

    responses.add(
        responses.PATCH,
        f"{BASE_URL}/orders/{order_id}",
        json={
            "order_id": order_id,
            "status": "PICKED_UP",
            "price_usd": 125.50,
            "eta": "2026-09-10T10:00:00Z",
        },
        status=200,
    )

    response = order_api_client.update_order_status(
        order_id,
        "PICKED_UP",
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["order_id"] == order_id
    assert response_data["status"] == "PICKED_UP"

@responses.activate
def test_update_order_status_rejects_illegal_transition(order_api_client):
    order_id = "123e4567-e89b-12d3-a456-426614174000"

    responses.add(
        responses.PATCH,
        f"{BASE_URL}/orders/{order_id}",
        json={"detail": "Illegal state transition"},
        status=409,
    )

    response = order_api_client.update_order_status(
        order_id,
        "IN_TRANSIT",
    )

    assert response.status_code == 409

def test_order_status_change_publishes_sqs_event():
    from tests.order_events import OrderEventPublisher

    publisher = OrderEventPublisher(
        queue_url="https://sqs.ap-south-1.amazonaws.com/123456789012/order-events"
    )

    publisher.sqs = MagicMock()

    publisher.publish_status_change(
        order_id="123e4567-e89b-12d3-a456-426614174000",
        old_status="CREATED",
        new_status="PICKED_UP",
    )

    publisher.sqs.send_message.assert_called_once()

    call_kwargs = publisher.sqs.send_message.call_args.kwargs

    assert call_kwargs["QueueUrl"] == (
        "https://sqs.ap-south-1.amazonaws.com/123456789012/order-events"
    )

    message_body = call_kwargs["MessageBody"]

    assert "ORDER_STATUS_CHANGED" in message_body
    assert "123e4567-e89b-12d3-a456-426614174000" in message_body
    assert "CREATED" in message_body
    assert "PICKED_UP" in message_body