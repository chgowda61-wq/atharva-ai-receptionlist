import database

database.init_db()

database.create_call("TEST001", "en")

database.save_turn(
    "TEST001",
    "caller",
    "I need an appointment"
)

database.save_turn(
    "TEST001",
    "agent",
    "Sure, I can help you."
)

database.save_request(
    "TEST001",
    "appointment",
    "Customer requested an appointment"
)

print("Calls:", database.get_calls())
print("Conversation:", database.get_transcripts("TEST001"))
print("Requests:", database.get_requests("TEST001"))

print("Database test completed!")