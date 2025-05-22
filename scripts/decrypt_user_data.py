"""
This script decodes a base64-encoded string containing configuration data,
converts it to a human-readable UTF-8 string, and prints the result.
"""

import base64


user_data = "I2Nsb3VkLWNvbmZpZwogcGFja2FnZXM6CiAgLSBuZ2lueAogcnVuY21kOgogIC0gc3lzdGVtY3RsIGVuYWJsZSBuZ2lueAogIC0gc3lzdGVtY3RsIHN0YXJ0IG5naW54"

decoded_bytes = base64.b64decode(user_data)
decoded_str = decoded_bytes.decode('utf-8')

print(decoded_str)