import requests
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing FastAPI Todo Application...")
    print("=" * 50)

    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 2: Create a todo
    print("\n2. Creating a new todo...")
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos/", json=todo_data)
    print(f"Status: {response.status_code}")
    created_todo = response.json()
    print(f"Created: {created_todo}")
    todo_id = created_todo["id"]

    # Test 3: Get all todos
    print("\n3. Getting all todos...")
    response = requests.get(f"{BASE_URL}/todos/")
    print(f"Status: {response.status_code}")
    todos = response.json()
    print(f"Total todos: {len(todos)}")

    # Test 4: Get specific todo
    print(f"\n4. Getting todo with id {todo_id}...")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"Status: {response.status_code}")
    print(f"Todo: {response.json()}")

    # Test 5: Update todo
    print(f"\n5. Updating todo {todo_id}...")
    update_data = {"title": "Updated Test Todo"}
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Updated: {response.json()}")

    # Test 6: Mark as complete
    print(f"\n6. Marking todo {todo_id} as complete...")
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/complete")
    print(f"Status: {response.status_code}")
    print(f"Completed: {response.json()['completed']}")

    # Test 7: Mark as incomplete
    print(f"\n7. Marking todo {todo_id} as incomplete...")
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/incomplete")
    print(f"Status: {response.status_code}")
    print(f"Completed: {response.json()['completed']}")

    # Test 8: Delete todo
    print(f"\n8. Deleting todo {todo_id}...")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"Status: {response.status_code}")

    # Test 9: Verify deletion
    print(f"\n9. Verifying todo {todo_id} is deleted...")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print("Todo successfully deleted!")

    print("\n" + "=" * 50)
    print("All tests completed successfully!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"Error during testing: {e}")
