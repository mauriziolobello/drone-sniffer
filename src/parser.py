import importlib
from src.profiles import sanrock_u52

def get_profile(profile_name):
    """Dynamically load the profile module."""
    try:
        return importlib.import_module(f"src.profiles.{profile_name}")
    except ImportError:
        return None

def parse_payload(packet, profile_name="sanrock_u52"):
    """
    Isolate the raw payload from the packet and delegate parsing to the matching profile.
    Profile selection is dynamic via get_profile.
    """
    if packet.haslayer("Raw"):
        raw_data = packet.getlayer("Raw").load

        profile = get_profile(profile_name)
        if profile and hasattr(profile, 'parse'):
            return profile.parse(raw_data)

        return f"[Unmapped Raw Bytes]: {raw_data.hex(' ')}"
    return None
