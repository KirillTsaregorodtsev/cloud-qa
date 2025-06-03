from dataclasses import dataclass

@dataclass
class ServerInfo:
    server_id: int
    instance_id: str
    ip_address: str