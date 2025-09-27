import httpx
import pytest
from fastapi.testclient import TestClient


class TestCreateItemIntegration:
    """Table-driven integration tests for POST /items"""
    
    def setup_method(self):
        # Clear DB before each test if needed
        # Assuming you have access to clear your DB
        pass
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "valid_basic_item",
            "payload": {"name": "test_item", "value": "test_value"},
            "auth_token": "user_token",  # Will be replaced with actual token in test
            "expected_status": 200,
            "expected_response": {
                "name": "test_item",
                "value": "test_value",
                "id": "generated"  # Special marker for generated fields
            },
            "should_have_id": True
        },
        {
            "name": "empty_strings",
            "payload": {"name": "", "value": ""},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "", "value": "", "id": "generated"},
            "should_have_id": True
        },
        {
            "name": "unicode_characters",
            "payload": {"name": "测试项目", "value": "тестовое значение 🚀"},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "测试项目", "value": "тестовое значение 🚀", "id": "generated"},
            "should_have_id": True
        },
        {
            "name": "special_characters",
            "payload": {"name": "item!@#$%^&*()", "value": "value<>?:\"{}|"},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "item!@#$%^&*()", "value": "value<>?:\"{}|", "id": "generated"},
            "should_have_id": True
        },
        {
            "name": "very_long_strings",
            "payload": {"name": "x" * 1000, "value": "y" * 1000},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "x" * 1000, "value": "y" * 1000, "id": "generated"},
            "should_have_id": True
        },
        {
            "name": "missing_name_field",
            "payload": {"value": "test_value"},
            "auth_token": "user_token",
            "expected_status": 422,  # Pydantic validation error
            "expected_response": None,
            "should_have_id": False
        },
        {
            "name": "missing_value_field",
            "payload": {"name": "test_item"},
            "auth_token": "user_token",
            "expected_status": 422,  # Pydantic validation error
            "expected_response": None,
            "should_have_id": False
        },
        {
            "name": "no_auth_token",
            "payload": {"name": "test_item", "value": "test_value"},
            "auth_token": None,
            "expected_status": 403,  # Unauthorized
            "expected_response": None,
            "should_have_id": False
        },
        {
            "name": "invalid_auth_token",
            "payload": {"name": "test_item", "value": "test_value"},
            "auth_token": "invalid_token",
            "expected_status": 401,  # Unauthorized
            "expected_response": None,
            "should_have_id": False
        }
    ])
    def test_create_item_scenarios(self, test_client: TestClient, user_token: str, test_case):
        """Test various create item scenarios"""
        headers = {}
        if test_case["auth_token"] == "user_token":
            headers["Authorization"] = f"Bearer {user_token}"
        elif test_case["auth_token"] == "invalid_token":
            headers["Authorization"] = "Bearer invalid_token_here"
        elif test_case["auth_token"]:
            headers["Authorization"] = f"Bearer {test_case['auth_token']}"
        
        response = test_client.post("/items", json=test_case["payload"], headers=headers)
        
        assert response.status_code == test_case["expected_status"]
        
        if test_case["expected_status"] == 200:
            response_data = response.json()
            expected = test_case["expected_response"]
            
            assert response_data["name"] == expected["name"]
            assert response_data["value"] == expected["value"]
            
            if test_case["should_have_id"]:
                assert "id" in response_data
                assert response_data["id"] is not None
                assert len(response_data["id"]) > 0


class TestReadItemIntegration:
    """Table-driven integration tests for GET /items/{item_id}"""
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "read_existing_item",
            "setup_items": [{"name": "test_item", "value": "test_value"}],
            "item_index_to_read": 0,  # Read the first created item
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "test_item", "value": "test_value"}
        },
        {
            "name": "read_with_unicode",
            "setup_items": [{"name": "测试", "value": "значение"}],
            "item_index_to_read": 0,
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "测试", "value": "значение"}
        },
        {
            "name": "read_nonexistent_item",
            "setup_items": [],
            "item_id_to_read": "non-existent-id",
            "auth_token": "user_token",
            "expected_status": 404,
            "expected_response": None
        },
        {
            "name": "read_without_auth",
            "setup_items": [{"name": "test", "value": "value"}],
            "item_index_to_read": 0,
            "auth_token": None,
            "expected_status": 403,
            "expected_response": None
        },
        {
            "name": "read_with_invalid_auth",
            "setup_items": [{"name": "test", "value": "value"}],
            "item_index_to_read": 0,
            "auth_token": "invalid_token",
            "expected_status": 401,
            "expected_response": None
        }
    ])
    def test_read_item_scenarios(self, test_client: httpx.Client, user_token: str, test_case):
        """Test various read item scenarios"""
        created_items = []
        
        # Setup: Create items if needed
        if test_case["setup_items"]:
            headers = {"Authorization": f"Bearer {user_token}"}
            for item_data in test_case["setup_items"]:
                response = test_client.post("/items", json=item_data, headers=headers)
                assert response.status_code == 200
                created_items.append(response.json())
        
        # Determine which item ID to read
        if "item_index_to_read" in test_case:
            item_id = created_items[test_case["item_index_to_read"]]["id"]
        elif "item_id_to_read" in test_case:
            item_id = test_case["item_id_to_read"]
        else:
            item_id = "default-id"
        
        # Setup headers
        headers = {}
        if test_case["auth_token"] == "user_token":
            headers["Authorization"] = f"Bearer {user_token}"
        elif test_case["auth_token"] == "invalid_token":
            headers["Authorization"] = "Bearer invalid_token_here"
        
        # Make the read request
        response = test_client.get(f"/items/{item_id}", headers=headers)
        
        assert response.status_code == test_case["expected_status"]
        
        if test_case["expected_status"] == 200:
            response_data = response.json()
            expected = test_case["expected_response"]
            assert response_data["name"] == expected["name"]
            assert response_data["value"] == expected["value"]
            assert response_data["id"] == item_id


class TestUpdateItemIntegration:
    """Table-driven integration tests for PUT /items/{item_id}"""
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "update_existing_item",
            "setup_items": [{"name": "original", "value": "original_value"}],
            "item_index_to_update": 0,
            "update_data": {"name": "updated", "value": "updated_value"},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "updated", "value": "updated_value"}
        },
        {
            "name": "update_with_unicode",
            "setup_items": [{"name": "test", "value": "test"}],
            "item_index_to_update": 0,
            "update_data": {"name": "更新的", "value": "обновленное"},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "更新的", "value": "обновленное"}
        },
        {
            "name": "update_with_same_values",
            "setup_items": [{"name": "same", "value": "same"}],
            "item_index_to_update": 0,
            "update_data": {"name": "same", "value": "same"},
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_response": {"name": "same", "value": "same"}
        },
        {
            "name": "update_nonexistent_item",
            "setup_items": [],
            "item_id_to_update": "non-existent-id",
            "update_data": {"name": "test", "value": "test"},
            "auth_token": "user_token",
            "expected_status": 404,
            "expected_response": None
        },
        {
            "name": "update_without_auth",
            "setup_items": [{"name": "test", "value": "test"}],
            "item_index_to_update": 0,
            "update_data": {"name": "updated", "value": "updated"},
            "auth_token": None,
            "expected_status": 403,
            "expected_response": None
        },
        {
            "name": "update_with_invalid_data",
            "setup_items": [{"name": "test", "value": "test"}],
            "item_index_to_update": 0,
            "update_data": {"name": "updated"},  # Missing value field
            "auth_token": "user_token",
            "expected_status": 422,  # Validation error
            "expected_response": None
        }
    ])
    def test_update_item_scenarios(self, test_client: httpx.Client, user_token: str, test_case):
        """Test various update item scenarios"""
        created_items = []
        
        # Setup: Create items if needed
        if test_case["setup_items"]:
            headers = {"Authorization": f"Bearer {user_token}"}
            for item_data in test_case["setup_items"]:
                response = test_client.post("/items", json=item_data, headers=headers)
                assert response.status_code == 200
                created_items.append(response.json())
        
        # Determine which item ID to update
        if "item_index_to_update" in test_case:
            item_id = created_items[test_case["item_index_to_update"]]["id"]
        elif "item_id_to_update" in test_case:
            item_id = test_case["item_id_to_update"]
        else:
            item_id = "default-id"
        
        # Setup headers
        headers = {}
        if test_case["auth_token"] == "user_token":
            headers["Authorization"] = f"Bearer {user_token}"
        elif test_case["auth_token"] == "invalid_token":
            headers["Authorization"] = "Bearer invalid_token_here"
        
        # Make the update request
        response = test_client.put(f"/items/{item_id}", json=test_case["update_data"], headers=headers)
        
        assert response.status_code == test_case["expected_status"]
        
        if test_case["expected_status"] == 200:
            response_data = response.json()
            expected = test_case["expected_response"]
            assert response_data["name"] == expected["name"]
            assert response_data["value"] == expected["value"]
            assert response_data["id"] == item_id


class TestDeleteItemIntegration:
    """Table-driven integration tests for DELETE /items/{item_id}"""
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "admin_delete_existing_item",
            "setup_items": [{"name": "to_delete", "value": "delete_value"}],
            "item_index_to_delete": 0,
            "auth_token": "admin_token",
            "expected_status": 200,
            "expected_response": {"deleted": True},
            "should_be_deleted": True
        },
        {
            "name": "user_delete_existing_item_forbidden",
            "setup_items": [{"name": "to_delete", "value": "delete_value"}],
            "item_index_to_delete": 0,
            "auth_token": "user_token",
            "expected_status": 403,  # Forbidden
            "expected_response": None,
            "should_be_deleted": False
        },
        {
            "name": "admin_delete_nonexistent_item",
            "setup_items": [],
            "item_id_to_delete": "non-existent-id",
            "auth_token": "admin_token",
            "expected_status": 404,
            "expected_response": None,
            "should_be_deleted": False
        },
        {
            "name": "delete_without_auth",
            "setup_items": [{"name": "test", "value": "test"}],
            "item_index_to_delete": 0,
            "auth_token": None,
            "expected_status": 403,
            "expected_response": None,
            "should_be_deleted": False
        },
        {
            "name": "delete_with_invalid_auth",
            "setup_items": [{"name": "test", "value": "test"}],
            "item_index_to_delete": 0,
            "auth_token": "invalid_token",
            "expected_status": 401,
            "expected_response": None,
            "should_be_deleted": False
        }
    ])
    def test_delete_item_scenarios(self, test_client: httpx.Client, user_token: str, admin_token, test_case):
        """Test various delete item scenarios"""
        created_items = []
        
        # Setup: Create items if needed
        if test_case["setup_items"]:
            headers = {"Authorization": f"Bearer {user_token}"}
            for item_data in test_case["setup_items"]:
                response = test_client.post("/items", json=item_data, headers=headers)
                assert response.status_code == 200
                created_items.append(response.json())
        
        # Determine which item ID to delete
        if "item_index_to_delete" in test_case:
            item_id = created_items[test_case["item_index_to_delete"]]["id"]
        elif "item_id_to_delete" in test_case:
            item_id = test_case["item_id_to_delete"]
        else:
            item_id = "default-id"
        
        # Setup headers
        headers = {}
        if test_case["auth_token"] == "user_token":
            headers["Authorization"] = f"Bearer {user_token}"
        elif test_case["auth_token"] == "admin_token":
            headers["Authorization"] = f"Bearer {admin_token}"
        elif test_case["auth_token"] == "invalid_token":
            headers["Authorization"] = "Bearer invalid_token_here"
        
        # Make the delete request
        response = test_client.delete(f"/items/{item_id}", headers=headers)
        
        assert response.status_code == test_case["expected_status"]
        
        if test_case["expected_status"] == 200:
            response_data = response.json()
            expected = test_case["expected_response"]
            assert response_data == expected
        
        # Verify item deletion status by trying to read it
        if test_case["should_be_deleted"] and created_items:
            read_headers = {"Authorization": f"Bearer {user_token}"}
            read_response = test_client.get(f"/items/{item_id}", headers=read_headers)
            assert read_response.status_code == 404
        elif not test_case["should_be_deleted"] and created_items:
            read_headers = {"Authorization": f"Bearer {user_token}"}
            read_response = test_client.get(f"/items/{item_id}", headers=read_headers)
            if test_case["expected_status"] != 404:  # If original item existed
                assert read_response.status_code == 200


class TestListItemsIntegration:
    """Table-driven integration tests for GET /items"""
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "list_empty_items",
            "setup_items": [],
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_count": 0,
            "expected_names": []
        },
        {
            "name": "list_single_item",
            "setup_items": [{"name": "single", "value": "single_value"}],
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_count": 1,
            "expected_names": ["single"]
        },
        {
            "name": "list_multiple_items",
            "setup_items": [
                {"name": "first", "value": "first_value"},
                {"name": "second", "value": "second_value"},
                {"name": "third", "value": "third_value"}
            ],
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_count": 3,
            "expected_names": ["first", "second", "third"]
        },
        {
            "name": "list_items_unicode",
            "setup_items": [
                {"name": "测试1", "value": "值1"},
                {"name": "тест2", "value": "значение2"}
            ],
            "auth_token": "user_token",
            "expected_status": 200,
            "expected_count": 2,
            "expected_names": ["测试1", "тест2"]
        },
        {
            "name": "list_without_auth",
            "setup_items": [{"name": "test", "value": "test"}],
            "auth_token": None,
            "expected_status": 403,
            "expected_count": None,
            "expected_names": None
        },
        {
            "name": "list_with_invalid_auth",
            "setup_items": [{"name": "test", "value": "test"}],
            "auth_token": "invalid_token",
            "expected_status": 401,
            "expected_count": None,
            "expected_names": None
        }
    ])
    def test_list_items_scenarios(self, test_client: httpx.Client, user_token: str, test_case):
        """Test various list items scenarios"""
        # Setup: Create items if needed
        if test_case["setup_items"]:
            headers = {"Authorization": f"Bearer {user_token}"}
            for item_data in test_case["setup_items"]:
                response = test_client.post("/items", json=item_data, headers=headers)
                assert response.status_code == 200
        
        # Setup headers for list request
        headers = {}
        if test_case["auth_token"] == "user_token":
            headers["Authorization"] = f"Bearer {user_token}"
        elif test_case["auth_token"] == "invalid_token":
            headers["Authorization"] = "Bearer invalid_token_here"
        
        # Make the list request
        response = test_client.get("/items", headers=headers)
        
        assert response.status_code == test_case["expected_status"]
        
        if test_case["expected_status"] == 200:
            response_data = response.json()
            assert len(response_data) >= test_case["expected_count"]  # >= because other tests might create items
            
            if test_case["expected_count"] > 0:
                # Find items that match our expected names
                found_names = [item["name"] for item in response_data if item["name"] in test_case["expected_names"]]
                assert set(found_names) == set(test_case["expected_names"])
                
                # Verify structure of returned items
                for item in response_data:
                    assert "id" in item
                    assert "name" in item
                    assert "value" in item


class TestCompleteWorkflowIntegration:
    """Test complete CRUD workflows with table-driven approach"""
    
    @pytest.mark.parametrize("workflow_case", [
        {
            "name": "complete_crud_workflow_success",
            "create_data": {"name": "workflow_item", "value": "workflow_value"},
            "update_data": {"name": "updated_workflow", "value": "updated_value"},
            "user_role": "user",
            "admin_role": "admin",
            "expected_create_status": 200,
            "expected_read_status": 200,
            "expected_update_status": 200,
            "expected_delete_by_user_status": 403,
            "expected_delete_by_admin_status": 200
        },
        {
            "name": "workflow_with_unicode",
            "create_data": {"name": "流程项目", "value": "流程值"},
            "update_data": {"name": "更新流程", "value": "更新值"},
            "user_role": "user",
            "admin_role": "admin",
            "expected_create_status": 200,
            "expected_read_status": 200,
            "expected_update_status": 200,
            "expected_delete_by_user_status": 403,
            "expected_delete_by_admin_status": 200
        }
    ])
    def test_complete_crud_workflow(self, test_client: httpx.Client, user_token: str, admin_token, workflow_case):
        """Test complete CRUD workflow scenarios"""
        user_headers = {"Authorization": f"Bearer {user_token}"}
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        # 1. Create item
        create_response = test_client.post("/items", json=workflow_case["create_data"], headers=user_headers)
        assert create_response.status_code == workflow_case["expected_create_status"]
        
        if create_response.status_code == 200:
            created_item = create_response.json()
            item_id = created_item["id"]
            
            # 2. Read item
            read_response = test_client.get(f"/items/{item_id}", headers=user_headers)
            assert read_response.status_code == workflow_case["expected_read_status"]
            assert read_response.json()["name"] == workflow_case["create_data"]["name"]
            
            # 3. Update item
            update_response = test_client.put(f"/items/{item_id}", json=workflow_case["update_data"], headers=user_headers)
            assert update_response.status_code == workflow_case["expected_update_status"]
            if update_response.status_code == 200:
                assert update_response.json()["name"] == workflow_case["update_data"]["name"]
            
            # 4. Try delete as user (should fail)
            delete_user_response = test_client.delete(f"/items/{item_id}", headers=user_headers)
            assert delete_user_response.status_code == workflow_case["expected_delete_by_user_status"]
            
            # 5. Delete as admin (should succeed)
            delete_admin_response = test_client.delete(f"/items/{item_id}", headers=admin_headers)
            assert delete_admin_response.status_code == workflow_case["expected_delete_by_admin_status"]
            
            # 6. Verify item is deleted
            if delete_admin_response.status_code == 200:
                final_read_response = test_client.get(f"/items/{item_id}", headers=user_headers)
                assert final_read_response.status_code == 404


# Performance and stress test scenarios
class TestPerformanceIntegration:
    """Table-driven performance and stress tests"""
    
    @pytest.mark.parametrize("perf_case", [
        {
            "name": "create_many_items",
            "item_count": 100,
            "auth_token": "user_token",
            "expected_status": 200
        },
        {
            "name": "create_items_with_large_data",
            "item_count": 5,
            "auth_token": "user_token",
            "name_size": 1000,
            "value_size": 1000,
            "expected_status": 200
        }
    ])
    @pytest.mark.slow  # Mark as slow test
    def test_performance_scenarios(self, test_client: httpx.Client, user_token: str, perf_case):
        """Test performance scenarios"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        created_items = []
        
        for i in range(perf_case["item_count"]):
            if "name_size" in perf_case:
                item_data = {
                    "name": f"item_{i}_" + "x" * perf_case["name_size"],
                    "value": f"value_{i}_" + "y" * perf_case["value_size"]
                }
            else:
                item_data = {"name": f"item_{i}", "value": f"value_{i}"}
            
            response = test_client.post("/items", json=item_data, headers=headers)
            assert response.status_code == perf_case["expected_status"]
            
            if response.status_code == 200:
                created_items.append(response.json())
        
        # Verify we can list all created items
        list_response = test_client.get("/items", headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json()) >= len(created_items)
