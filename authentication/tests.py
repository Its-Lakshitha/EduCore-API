from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from teacher.models.Teacher import Teacher
from student.models import Student

from .utils import generate_password_reset_token

User = get_user_model()

class BaseAuthTestCase(APITestCase):
    """Base test class with common helper methods for authentication tests."""

    def create_user(self, username='testuser', email='test@mail.com',
                    password='StrongPass123!', role='student'):
        """Helper to create a user with sensible defaults."""
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

    def get_tokens_for_user(self, user):
        """Helper to generate JWT tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def authenticate_user(self, user):
        """Helper to authenticate a user via force_authenticate."""
        self.client.force_authenticate(user=user)

    def authenticate_with_token(self, user):
        """Helper to authenticate a user via JWT access token."""
        tokens = self.get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return tokens


# ---------------------------------------------------------------------------
# Registration Tests  (POST /api/auth/register/)
# ---------------------------------------------------------------------------
class RegisterViewTests(BaseAuthTestCase):
    """Tests for the user registration endpoint."""

    def setUp(self):
        self.url = reverse('register')
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password': 'StrongPass123!',
            'role': 'student',
        }

    # --- Success cases ---

    def test_register_student_success(self):
        """A new student can register with valid data."""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.role, 'student')

    def test_register_teacher_success(self):
        """A new teacher can register with valid data."""
        data = {**self.valid_data, 'username': 'teacher1',
                'email': 'teacher1@mail.com', 'role': 'teacher'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='teacher1')
        self.assertEqual(user.role, 'teacher')

    def test_register_admin_success(self):
        """A new admin can register with valid data."""
        data = {**self.valid_data, 'username': 'admin1',
                'email': 'admin1@mail.com', 'role': 'admin'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='admin1')
        self.assertEqual(user.role, 'admin')

    def test_register_password_is_hashed(self):
        """The stored password should be hashed, not plain text."""
        self.client.post(self.url, self.valid_data, format='json')
        user = User.objects.first()
        self.assertNotEqual(user.password, self.valid_data['password'])
        self.assertTrue(user.check_password(self.valid_data['password']))

    # --- Failure cases ---

    def test_register_missing_username(self):
        """Registration fails when username is missing."""
        data = {**self.valid_data}
        del data['username']
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_missing_password(self):
        """Registration fails when password is missing."""
        data = {**self.valid_data}
        del data['password']
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_duplicate_username(self):
        """Registration fails when the username already exists."""
        self.create_user(username='newuser')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_weak_password(self):
        """Registration fails when the password is too short or too common."""
        data = {**self.valid_data, 'password': '123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_empty_body(self):
        """Registration fails with an empty request body."""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Login Tests  (POST /api/auth/login/)
# ---------------------------------------------------------------------------
class LoginViewTests(BaseAuthTestCase):
    """Tests for the user login endpoint."""

    def setUp(self):
        self.url = reverse('login')
        self.password = 'StrongPass123!'
        self.user = self.create_user(password=self.password)

    # --- Success cases ---

    def test_login_success(self):
        """A user can log in with valid credentials."""
        data = {'username': self.user.username, 'password': self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_tokens_are_non_empty_strings(self):
        """Login response tokens should be non-empty strings."""
        data = {'username': self.user.username, 'password': self.password}
        response = self.client.post(self.url, data, format='json')
        print("RESPONSE DATA:", response.data)  # Debug print to inspect the response
        print("STATUS CODE:", response.status_code)  # Debug print to check status code
        self.assertIsInstance(response.data['access'], str)
        self.assertIsInstance(response.data['refresh'], str)
        self.assertTrue(len(response.data['access']) > 0)
        self.assertTrue(len(response.data['refresh']) > 0)

    # --- Failure cases ---

    def test_login_wrong_password(self):
        """Login fails with an incorrect password."""
        data = {'username': self.user.username, 'password': 'WrongPass999!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_nonexistent_user(self):
        """Login fails for a username that does not exist."""
        data = {'username': 'ghost', 'password': 'SomePass123!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_username(self):
        """Login fails when username is not provided."""
        data = {'password': self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        """Login fails when password is not provided."""
        data = {'username': self.user.username}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_body(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Logout Tests  (POST /api/auth/logout/)
# ---------------------------------------------------------------------------
class LogoutViewTests(BaseAuthTestCase):
    """Tests for the user logout endpoint."""

    def setUp(self):
        self.url = reverse('logout')
        self.user = self.create_user()

    # --- Success cases ---

    def test_logout_success(self):
        """An authenticated user can log out with a valid refresh token."""
        tokens = self.authenticate_with_token(self.user)
        data = {'refresh': tokens['refresh']}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_blacklists_refresh_token(self):
        """After logout, the refresh token should be blacklisted and unusable."""
        tokens = self.authenticate_with_token(self.user)
        self.client.post(self.url, {'refresh': tokens['refresh']}, format='json')

        # Attempting to use the blacklisted refresh token should fail
        token_refresh_url = reverse('login')  # We'll just verify the token object
        with self.assertRaises(Exception):
            RefreshToken(tokens['refresh']).check_blacklist()

    # --- Failure cases ---

    def test_logout_unauthenticated(self):
        """Logout fails when the user is not authenticated."""
        tokens = self.get_tokens_for_user(self.user)
        response = self.client.post(self.url, {'refresh': tokens['refresh']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalid_refresh_token(self):
        """Logout fails when an invalid refresh token is provided."""
        self.authenticate_with_token(self.user)
        data = {'refresh': 'invalid-token-string'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_logout_missing_refresh_token(self):
        """Logout fails when no refresh token is provided."""
        self.authenticate_with_token(self.user)
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Forget Password Tests  (POST /api/auth/forget-password/)
# ---------------------------------------------------------------------------
class ForgetPasswordViewTests(BaseAuthTestCase):
    """Tests for the forget password endpoint."""

    def setUp(self):
        self.url = reverse('forget-password')
        self.user = self.create_user(email='forgotme@mail.com')

    # --- Success cases ---

    def test_forget_password_success(self):
        """A valid email triggers a password reset response with uid and token."""
        data = {'email': 'forgotme@mail.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('uid', response.data)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)

    def test_forget_password_sends_email(self):
        """A valid request sends a password reset email."""
        data = {'email': 'forgotme@mail.com'}
        self.client.post(self.url, data, format='json')
        # Django test runner uses locmem email backend
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset', mail.outbox[0].subject)
        self.assertIn('forgotme@mail.com', mail.outbox[0].to)

    # --- Failure cases ---

    def test_forget_password_nonexistent_email(self):
        """Forget password fails for an email that doesn't exist."""
        data = {'email': 'nobody@mail.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_forget_password_missing_email(self):
        """Forget password fails when email is not provided."""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Reset Password Tests  (POST /api/auth/reset-password/)
# ---------------------------------------------------------------------------
class ResetPasswordViewTests(BaseAuthTestCase):
    """Tests for the reset password endpoint."""

    def setUp(self):
        self.url = reverse('reset-password')
        self.user = self.create_user()
        self.uid, self.token = generate_password_reset_token(self.user)

    # --- Success cases ---

    def test_reset_password_success(self):
        """A user can reset their password with a valid uid and token."""
        new_password = 'NewStrongPass456!'
        data = {
            'uid': self.uid,
            'token': self.token,
            'new_password': new_password,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_reset_password_updates_password(self):
        """After a successful reset, the user can log in with the new password."""
        new_password = 'NewStrongPass456!'
        data = {
            'uid': self.uid,
            'token': self.token,
            'new_password': new_password,
        }
        self.client.post(self.url, data, format='json')

        # Old password should no longer work
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('StrongPass123!'))
        self.assertTrue(self.user.check_password(new_password))

    # --- Failure cases ---

    def test_reset_password_invalid_token(self):
        """Reset fails with an invalid token."""
        data = {
            'uid': self.uid,
            'token': 'invalid-token',
            'new_password': 'NewStrongPass456!',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_invalid_uid(self):
        """Reset fails with an invalid uid."""
        data = {
            'uid': 'invalid-uid',
            'token': self.token,
            'new_password': 'NewStrongPass456!',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_expired_token(self):
        """A token cannot be reused after a successful reset."""
        new_password = 'NewStrongPass456!'
        data = {
            'uid': self.uid,
            'token': self.token,
            'new_password': new_password,
        }
        # First reset — should succeed
        self.client.post(self.url, data, format='json')

        # Second reset with same token — should fail (token is consumed)
        data['new_password'] = 'AnotherPass789!'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_missing_fields(self):
        """Reset fails when required fields are missing."""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Authorization & Permission Tests
# ---------------------------------------------------------------------------
class UnauthorizedAccessTests(BaseAuthTestCase):
    """Tests verifying that unauthenticated requests are rejected on protected endpoints."""

    def test_unauthenticated_access_to_student_list(self):
        """An unauthenticated user cannot access the students list endpoint."""
        url = reverse('students-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_access_to_logout(self):
        """An unauthenticated user cannot access the logout endpoint."""
        url = reverse('logout')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoleBasedAccessTests(BaseAuthTestCase):
    """Tests verifying role-based permission enforcement."""

    def test_student_cannot_access_admin_student_create(self):
        """A student user should be forbidden from creating students (admin action)."""
        student = self.create_user(
            username='student1', email='student1@mail.com',
            password='StrongPass123!', role='student',
        )
        self.authenticate_with_token(student)
        url = reverse('student-create')
        data = {
            'name': 'New Student',
            'email': 'new@mail.com',
            'registration_number': 'REG999',
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
        ])

    def test_admin_can_access_student_list(self):
        """An admin user should be able to access the students list."""
        admin = self.create_user(
            username='admin1', email='admin1@mail.com',
            password='StrongPass123!', role='admin',
        )
        self.authenticate_with_token(admin)
        url = reverse('students-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Signal Tests  (Profile auto-creation on registration)
# ---------------------------------------------------------------------------
class SignalTests(BaseAuthTestCase):
    """Tests verifying that signals create the correct profile on user registration."""

    def test_student_profile_created_on_registration(self):
        """Registering a student user auto-creates a Student profile via signal."""
        from student.models import Student

        url = reverse('register')
        data = {
            'username': 'signalstudent',
            'email': 'signalstudent@mail.com',
            'password': 'StrongPass123!',
            'role': 'student',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='signalstudent')
        self.assertTrue(Student.objects.filter(user=user).exists())
        student = Student.objects.get(user=user)
        self.assertEqual(student.email, 'signalstudent@mail.com')

    def test_teacher_profile_created_on_registration(self):
        """Registering a teacher user auto-creates a Teacher profile via signal."""
        from teacher.models import Teacher

        url = reverse('register')
        data = {
            'username': 'signalteacher',
            'email': 'signalteacher@mail.com',
            'password': 'StrongPass123!',
            'role': 'teacher',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='signalteacher')
        self.assertTrue(Teacher.objects.filter(user=user).exists())
        teacher = Teacher.objects.get(user=user)
        self.assertEqual(teacher.email, 'signalteacher@mail.com')
