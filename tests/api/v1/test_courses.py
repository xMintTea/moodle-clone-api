# from fastapi.testclient import TestClient

# from app.api.v1.courses import get_course_service
# from app.main import app
# from app.service.course_service import CourseService
# from tests.test_db import TestingSessionLocal

# # Setup test client
# client = TestClient(app)


# def override_get_user_service():
#     session = TestingSessionLocal()
#     yield CourseService(session)


# app.dependency_overrides[get_course_service] = override_get_user_service

# def test_create_and_get_user():
#     # Create a new user
#     response = client.get("/v1/courses", )

#     assert response.status_code == 200