# Followers Messaging System

CloudMind AI includes a built-in messaging system to communicate with followers and subscribers. This feature allows you to manage a list of followers and send them updates about your CloudMind AI project.

## Features

- 📧 Manage followers/subscribers with email and metadata
- 💬 Create and send messages to all followers or filtered groups
- 🏷️ Tag-based filtering for targeted messaging
- 📊 Track message delivery status
- 🌐 Pre-built templates for CloudMind AI announcements (Russian and English)
- 💾 Persistent storage using JSON files
- 🔌 REST API and CLI interfaces

## Usage

### CLI Commands

#### Add a Follower

```bash
python cloudmind_cli.py add-follower --email user@example.com --name "John Doe"
```

#### List All Followers

```bash
python cloudmind_cli.py list-followers
```

List all followers including unsubscribed:
```bash
python cloudmind_cli.py list-followers --no-subscribed-only
```

#### Create a Custom Message

```bash
python cloudmind_cli.py create-message \
  --subject "Update: New Feature Released" \
  --content "We're excited to announce a new feature..."
```

#### Create a CloudMind AI Introduction Message

Pre-built template highlighting the project's strengths:

```bash
# Russian version
python cloudmind_cli.py create-cloudmind-message --language ru

# English version
python cloudmind_cli.py create-cloudmind-message --language en
```

#### Send a Message to Followers

```bash
python cloudmind_cli.py send-message --message-id <message-id>
```

#### List All Messages

```bash
python cloudmind_cli.py list-messages
```

### REST API Endpoints

#### Follower Management

**Add a Follower**
```http
POST /followers?email=user@example.com&name=John+Doe
```

**List Followers**
```http
GET /followers?subscribed_only=true
```

**Get a Specific Follower**
```http
GET /followers/{follower_id}
```

**Unsubscribe a Follower**
```http
POST /followers/{follower_id}/unsubscribe
```

#### Message Management

**Create a Message**
```http
POST /messages?subject=Test&content=Hello+World
```

**List Messages**
```http
GET /messages
```

**Send a Message**
```http
POST /messages/{message_id}/send
```

**Get Message Deliveries**
```http
GET /messages/{message_id}/deliveries
```

### Python SDK

```python
from cloudmind.notification import NotificationService

# Initialize service
service = NotificationService()

# Add followers
follower = service.add_follower(
    email="user@example.com",
    name="John Doe",
    tags=["developers"]
)

# Create a message
message = service.create_message(
    subject="Project Update",
    content="We've released a new version..."
)

# Send to all followers
result = service.send_message_to_followers(message.id)
print(f"Sent to {result['sent_count']} followers")

# Send to specific tags only
result = service.send_message_to_followers(
    message.id,
    tags=["developers"]
)
```

## Complete Workflow Example

Here's a complete example of adding followers and sending them an introduction message:

```bash
# 1. Add followers
python cloudmind_cli.py add-follower --email user1@example.com --name "Alice"
python cloudmind_cli.py add-follower --email user2@example.com --name "Bob"
python cloudmind_cli.py add-follower --email user3@example.com --name "Charlie"

# 2. Create the CloudMind AI introduction message
python cloudmind_cli.py create-cloudmind-message --language ru
# Note the message ID from the output, e.g., abc123...

# 3. Send the message to all followers
python cloudmind_cli.py send-message --message-id abc123...

# 4. Verify the message was sent
python cloudmind_cli.py list-messages
```

## Data Storage

All data is stored in JSON files in the `.cloudmind_data` directory:

- `followers.json` - Follower information
- `messages.json` - Created messages
- `deliveries.json` - Message delivery status

This directory is excluded from version control via `.gitignore`.

## Message Templates

The system includes pre-built message templates that highlight CloudMind AI's key features:

### Russian Template (ru)
A comprehensive message in Russian covering:
- Multi-cloud support (AWS, Azure, GCP, on-prem)
- AI-powered optimization
- Comprehensive monitoring
- Cost control
- Flexible interfaces
- Extensible architecture
- Project roadmap

### English Template (en)
The same content translated to English.

## Advanced Features

### Tag-Based Filtering

Add followers with tags for targeted messaging:

```python
service.add_follower(
    email="dev@example.com",
    tags=["developers", "contributors"]
)

service.add_follower(
    email="user@example.com",
    tags=["users"]
)

# Send only to developers
service.send_message_to_followers(message_id, tags=["developers"])
```

### Metadata

Both followers and messages support custom metadata:

```python
# Follower metadata
service.add_follower(
    email="user@example.com",
    metadata={"company": "Acme Corp", "role": "DevOps"}
)

# Message metadata
service.create_message(
    subject="Update",
    content="...",
    metadata={"priority": "high", "category": "announcement"}
)
```

### Unsubscribe Handling

Followers can be unsubscribed:

```python
service.unsubscribe_follower(follower_id)
```

Unsubscribed followers won't receive future messages when using `subscribed_only=True` (default).

## Security Considerations

**Note:** The current implementation simulates sending messages without actually sending emails. For production use, you should:

1. Integrate with an actual email service (SMTP, SendGrid, AWS SES, etc.)
2. Implement proper authentication and authorization
3. Add rate limiting to prevent abuse
4. Implement unsubscribe links in emails
5. Comply with email regulations (CAN-SPAM, GDPR, etc.)
6. Validate email addresses
7. Use secure storage for follower data

## Future Enhancements

Potential improvements for the messaging system:

- Email service integration (SMTP, SendGrid, AWS SES)
- Email templates with HTML formatting
- Scheduled message sending
- A/B testing for messages
- Analytics and engagement tracking
- Webhook notifications for deliveries
- Import/export follower lists
- Unsubscribe link generation
- Email verification
- Bounce handling

## API Documentation

When running the API server, visit http://localhost:8000/docs for interactive API documentation including the notification endpoints.

```bash
python cloudmind_cli.py start-api
```

Then open http://localhost:8000/docs in your browser.
