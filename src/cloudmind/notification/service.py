"""Notification service for managing followers and sending messages."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..core.models import Follower, Message, MessageDelivery
from ..core.logger import logger


class NotificationService:
    """Service for managing followers and sending messages."""

    def __init__(self, data_dir: str = ".cloudmind_data"):
        """Initialize notification service.
        
        Args:
            data_dir: Directory to store followers and messages data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.followers_file = self.data_dir / "followers.json"
        self.messages_file = self.data_dir / "messages.json"
        self.deliveries_file = self.data_dir / "deliveries.json"
        
        # Initialize data files if they don't exist
        for file in [self.followers_file, self.messages_file, self.deliveries_file]:
            if not file.exists():
                file.write_text("[]")
        
        logger.info(f"NotificationService initialized with data_dir: {data_dir}")

    def _load_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_json(self, file_path: Path, data: List[Dict[str, Any]]) -> None:
        """Save JSON data to file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def add_follower(self, email: str, name: Optional[str] = None, 
                     tags: Optional[List[str]] = None, 
                     metadata: Optional[Dict[str, Any]] = None) -> Follower:
        """Add a new follower.
        
        Args:
            email: Follower email address
            name: Follower name
            tags: List of tags for categorization
            metadata: Additional metadata
            
        Returns:
            Created follower object
        """
        followers = self._load_json(self.followers_file)
        
        # Check if follower already exists
        for f in followers:
            if f.get("email") == email:
                logger.warning(f"Follower with email {email} already exists")
                return Follower(**f)
        
        follower = Follower(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            subscribed=True,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        followers.append(follower.model_dump())
        self._save_json(self.followers_file, followers)
        
        logger.info(f"Added follower: {email}")
        return follower

    def get_followers(self, subscribed_only: bool = True, 
                     tags: Optional[List[str]] = None) -> List[Follower]:
        """Get all followers.
        
        Args:
            subscribed_only: Only return subscribed followers
            tags: Filter by tags
            
        Returns:
            List of followers
        """
        followers_data = self._load_json(self.followers_file)
        followers = [Follower(**f) for f in followers_data]
        
        if subscribed_only:
            followers = [f for f in followers if f.subscribed]
        
        if tags:
            followers = [f for f in followers if any(tag in f.tags for tag in tags)]
        
        return followers

    def get_follower(self, follower_id: str) -> Optional[Follower]:
        """Get a specific follower by ID.
        
        Args:
            follower_id: Follower ID
            
        Returns:
            Follower object or None
        """
        followers = self._load_json(self.followers_file)
        for f in followers:
            if f.get("id") == follower_id:
                return Follower(**f)
        return None

    def unsubscribe_follower(self, follower_id: str) -> bool:
        """Unsubscribe a follower.
        
        Args:
            follower_id: Follower ID
            
        Returns:
            True if successful, False otherwise
        """
        followers = self._load_json(self.followers_file)
        
        for f in followers:
            if f.get("id") == follower_id:
                f["subscribed"] = False
                self._save_json(self.followers_file, followers)
                logger.info(f"Unsubscribed follower: {follower_id}")
                return True
        
        return False

    def create_message(self, subject: str, content: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Create a new message.
        
        Args:
            subject: Message subject
            content: Message content
            metadata: Additional metadata
            
        Returns:
            Created message object
        """
        messages = self._load_json(self.messages_file)
        
        message = Message(
            id=str(uuid.uuid4()),
            subject=subject,
            content=content,
            metadata=metadata or {}
        )
        
        messages.append(message.model_dump())
        self._save_json(self.messages_file, messages)
        
        logger.info(f"Created message: {message.id}")
        return message

    def send_message_to_followers(self, message_id: str, 
                                  tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """Send a message to all followers.
        
        Args:
            message_id: Message ID to send
            tags: Only send to followers with these tags
            
        Returns:
            Dictionary with sending results
        """
        messages = self._load_json(self.messages_file)
        message_data = None
        
        for m in messages:
            if m.get("id") == message_id:
                message_data = m
                break
        
        if not message_data:
            logger.error(f"Message not found: {message_id}")
            return {"success": False, "error": "Message not found"}
        
        message = Message(**message_data)
        followers = self.get_followers(subscribed_only=True, tags=tags)
        
        if not followers:
            logger.warning("No followers to send message to")
            return {"success": True, "sent_count": 0, "message": "No followers found"}
        
        # Load existing deliveries
        deliveries = self._load_json(self.deliveries_file)
        
        # Send to each follower (simulated - in real implementation would use email service)
        sent_count = 0
        failed_count = 0
        
        for follower in followers:
            try:
                # Simulate sending (in real implementation, would use SMTP or email service)
                delivery = MessageDelivery(
                    message_id=message_id,
                    follower_id=follower.id,
                    status="sent"
                )
                
                deliveries.append(delivery.model_dump())
                sent_count += 1
                
                logger.info(f"Message sent to follower: {follower.email}")
                
            except Exception as e:
                logger.error(f"Failed to send message to {follower.email}: {e}")
                delivery = MessageDelivery(
                    message_id=message_id,
                    follower_id=follower.id,
                    status="failed",
                    error_message=str(e)
                )
                deliveries.append(delivery.model_dump())
                failed_count += 1
        
        # Update message with sent info
        message_data["sent_at"] = datetime.utcnow().isoformat()
        message_data["recipient_count"] = sent_count
        self._save_json(self.messages_file, messages)
        
        # Save deliveries
        self._save_json(self.deliveries_file, deliveries)
        
        result = {
            "success": True,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "total_followers": len(followers)
        }
        
        logger.info(f"Message broadcast complete: {result}")
        return result

    def get_messages(self) -> List[Message]:
        """Get all messages.
        
        Returns:
            List of messages
        """
        messages_data = self._load_json(self.messages_file)
        return [Message(**m) for m in messages_data]

    def get_message_deliveries(self, message_id: str) -> List[MessageDelivery]:
        """Get delivery status for a message.
        
        Args:
            message_id: Message ID
            
        Returns:
            List of deliveries
        """
        deliveries_data = self._load_json(self.deliveries_file)
        deliveries = [MessageDelivery(**d) for d in deliveries_data]
        return [d for d in deliveries if d.message_id == message_id]
