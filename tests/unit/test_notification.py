"""Unit tests for notification service."""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudmind.notification import NotificationService
from cloudmind.core.models import Follower, Message, MessageDelivery


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def notification_service(temp_data_dir):
    """Create a notification service with temporary data directory."""
    return NotificationService(data_dir=temp_data_dir)


def test_add_follower(notification_service):
    """Test adding a new follower."""
    follower = notification_service.add_follower(
        email="test@example.com",
        name="Test User"
    )
    
    assert follower.email == "test@example.com"
    assert follower.name == "Test User"
    assert follower.subscribed is True
    assert len(follower.id) > 0


def test_add_duplicate_follower(notification_service):
    """Test adding a duplicate follower."""
    # Add first follower
    follower1 = notification_service.add_follower(email="test@example.com")
    
    # Try to add same email again
    follower2 = notification_service.add_follower(email="test@example.com")
    
    # Should return the existing follower
    assert follower1.id == follower2.id


def test_get_followers(notification_service):
    """Test getting all followers."""
    # Add multiple followers
    notification_service.add_follower(email="user1@example.com", name="User 1")
    notification_service.add_follower(email="user2@example.com", name="User 2")
    notification_service.add_follower(email="user3@example.com", name="User 3")
    
    followers = notification_service.get_followers(subscribed_only=True)
    
    assert len(followers) == 3
    assert all(isinstance(f, Follower) for f in followers)
    assert all(f.subscribed for f in followers)


def test_get_follower_by_id(notification_service):
    """Test getting a specific follower by ID."""
    follower = notification_service.add_follower(email="test@example.com")
    
    retrieved = notification_service.get_follower(follower.id)
    
    assert retrieved is not None
    assert retrieved.id == follower.id
    assert retrieved.email == follower.email


def test_get_nonexistent_follower(notification_service):
    """Test getting a follower that doesn't exist."""
    result = notification_service.get_follower("nonexistent-id")
    assert result is None


def test_unsubscribe_follower(notification_service):
    """Test unsubscribing a follower."""
    follower = notification_service.add_follower(email="test@example.com")
    
    success = notification_service.unsubscribe_follower(follower.id)
    assert success is True
    
    # Verify follower is unsubscribed
    updated = notification_service.get_follower(follower.id)
    assert updated.subscribed is False
    
    # Should not appear in subscribed_only list
    subscribed = notification_service.get_followers(subscribed_only=True)
    assert len(subscribed) == 0


def test_unsubscribe_nonexistent_follower(notification_service):
    """Test unsubscribing a follower that doesn't exist."""
    success = notification_service.unsubscribe_follower("nonexistent-id")
    assert success is False


def test_create_message(notification_service):
    """Test creating a message."""
    message = notification_service.create_message(
        subject="Test Subject",
        content="Test content"
    )
    
    assert message.subject == "Test Subject"
    assert message.content == "Test content"
    assert len(message.id) > 0
    assert message.sent_at is None
    assert message.recipient_count == 0


def test_create_message_with_metadata(notification_service):
    """Test creating a message with metadata."""
    metadata = {"language": "en", "type": "announcement"}
    message = notification_service.create_message(
        subject="Test",
        content="Content",
        metadata=metadata
    )
    
    assert message.metadata == metadata


def test_get_messages(notification_service):
    """Test getting all messages."""
    # Create multiple messages
    notification_service.create_message(subject="Message 1", content="Content 1")
    notification_service.create_message(subject="Message 2", content="Content 2")
    
    messages = notification_service.get_messages()
    
    assert len(messages) == 2
    assert all(isinstance(m, Message) for m in messages)


def test_send_message_to_followers(notification_service):
    """Test sending a message to followers."""
    # Add followers
    notification_service.add_follower(email="user1@example.com")
    notification_service.add_follower(email="user2@example.com")
    notification_service.add_follower(email="user3@example.com")
    
    # Create message
    message = notification_service.create_message(
        subject="Test Broadcast",
        content="This is a test"
    )
    
    # Send to followers
    result = notification_service.send_message_to_followers(message.id)
    
    assert result["success"] is True
    assert result["sent_count"] == 3
    assert result["failed_count"] == 0
    assert result["total_followers"] == 3


def test_send_message_to_no_followers(notification_service):
    """Test sending a message when there are no followers."""
    message = notification_service.create_message(subject="Test", content="Content")
    
    result = notification_service.send_message_to_followers(message.id)
    
    assert result["success"] is True
    assert result["sent_count"] == 0


def test_send_nonexistent_message(notification_service):
    """Test sending a message that doesn't exist."""
    result = notification_service.send_message_to_followers("nonexistent-id")
    
    assert result["success"] is False
    assert "error" in result


def test_send_message_to_tagged_followers(notification_service):
    """Test sending a message to followers with specific tags."""
    # Add followers with tags
    notification_service.add_follower(email="user1@example.com", tags=["developers"])
    notification_service.add_follower(email="user2@example.com", tags=["developers", "admins"])
    notification_service.add_follower(email="user3@example.com", tags=["users"])
    
    # Create message
    message = notification_service.create_message(subject="Dev Update", content="Content")
    
    # Send only to developers
    result = notification_service.send_message_to_followers(message.id, tags=["developers"])
    
    assert result["success"] is True
    assert result["sent_count"] == 2  # Only 2 followers have "developers" tag


def test_get_message_deliveries(notification_service):
    """Test getting message delivery status."""
    # Add followers and send message
    notification_service.add_follower(email="user1@example.com")
    notification_service.add_follower(email="user2@example.com")
    
    message = notification_service.create_message(subject="Test", content="Content")
    notification_service.send_message_to_followers(message.id)
    
    # Get deliveries
    deliveries = notification_service.get_message_deliveries(message.id)
    
    assert len(deliveries) == 2
    assert all(isinstance(d, MessageDelivery) for d in deliveries)
    assert all(d.status == "sent" for d in deliveries)


def test_persistence_across_instances(temp_data_dir):
    """Test that data persists across service instances."""
    # Create first instance and add data
    service1 = NotificationService(data_dir=temp_data_dir)
    follower = service1.add_follower(email="test@example.com")
    message = service1.create_message(subject="Test", content="Content")
    
    # Create new instance with same data directory
    service2 = NotificationService(data_dir=temp_data_dir)
    
    # Verify data persists
    followers = service2.get_followers()
    messages = service2.get_messages()
    
    assert len(followers) == 1
    assert followers[0].email == "test@example.com"
    assert len(messages) == 1
    assert messages[0].subject == "Test"
