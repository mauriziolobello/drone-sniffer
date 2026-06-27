import pytest
from scapy.all import IP, UDP, Raw
from src.parser import parse_payload

def test_parse_payload_sanrock_valid_cmd():
    """Test parsing a valid 14-byte takeoff command for Sanrock U52."""
    raw_bytes = bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 00")
    packet = IP(dst="192.168.1.1") / UDP(dport=7080) / Raw(load=raw_bytes)
    
    result = parse_payload(packet, profile_name="sanrock_u52")
    
    assert "CMD" in result
    assert "Header=cc00" in result
    assert "Checksum=00" in result

def test_parse_payload_sanrock_unknown():
    """Test parsing an unknown length payload for Sanrock U52."""
    raw_bytes = bytes.fromhex("cc 00 40")
    packet = IP(dst="192.168.1.1") / UDP(dport=7080) / Raw(load=raw_bytes)
    
    result = parse_payload(packet, profile_name="sanrock_u52")
    
    assert "UKN (3 bytes)" in result

def test_parse_payload_unknown_profile():
    """Test parsing with a missing or unmapped profile."""
    raw_bytes = bytes.fromhex("ff ff")
    packet = IP(dst="192.168.1.1") / UDP(dport=7080) / Raw(load=raw_bytes)
    
    result = parse_payload(packet, profile_name="missing_profile")
    
    assert "Unmapped Raw Bytes" in result
    assert "ff ff" in result

def test_sanrock_u52_calculate_checksum():
    # Test typical XOR checksum calculation
    # Using a dummy payload for now since the real one's checksum algorithm is TBD
    payload = bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00")
    # Expected XOR of cc ^ 40 ^ 68 = e4
    from src.profiles import sanrock_u52
    assert sanrock_u52.calculate_checksum(payload) == 0xe4

def test_sanrock_u52_validate_checksum():
    from src.profiles import sanrock_u52
    # Valid packet with checksum 0xe4
    valid_payload = bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 e4")
    assert sanrock_u52.validate_checksum(valid_payload) is True

    # Invalid packet with checksum 0x00
    invalid_payload = bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 00")
    assert sanrock_u52.validate_checksum(invalid_payload) is False

def test_parse_payload_sanrock_checksum_validation():
    """Test parsing a command with checksum validation."""
    from src.parser import parse_payload
    from scapy.all import IP, UDP, Raw

    # This payload has 00 as checksum, but XOR gives e4. It should show CRC FAIL.
    raw_bytes = bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 00")
    packet = IP(dst="192.168.1.1") / UDP(dport=7080) / Raw(load=raw_bytes)
    result = parse_payload(packet, profile_name="sanrock_u52")
    
    assert "INVALID (CRC FAIL)" in result
