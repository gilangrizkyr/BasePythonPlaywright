"""Utilities untuk Playwright automation"""
import asyncio
from datetime import datetime
from typing import Callable, Any
import json


class WaitUtils:
    """Utility class untuk wait operations"""
    
    @staticmethod
    async def wait_for_condition(
        condition: Callable,
        timeout: int = 30000,
        poll_interval: int = 500
    ) -> bool:
        """Wait sampai condition terpenuhi"""
        start_time = datetime.now()
        timeout_seconds = timeout / 1000
        
        while True:
            try:
                if await condition():
                    return True
            except Exception as e:
                print(f"Condition check failed: {e}")
            
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout_seconds:
                return False
            
            await asyncio.sleep(poll_interval / 1000)


class FileUtils:
    """Utility class untuk file operations"""
    
    @staticmethod
    def save_json(data: dict, filepath: str):
        """Save dictionary ke JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def load_json(filepath: str) -> dict:
        """Load JSON file ke dictionary"""
        with open(filepath, 'r') as f:
            return json.load(f)


class StringUtils:
    """Utility class untuk string operations"""
    
    @staticmethod
    def remove_whitespace(text: str) -> str:
        """Remove semua whitespace dari string"""
        return ''.join(text.split())
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text - lowercase dan remove extra spaces"""
        return ' '.join(text.lower().split())
