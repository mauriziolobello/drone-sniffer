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
