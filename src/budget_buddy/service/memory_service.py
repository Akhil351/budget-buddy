# 📁 service/memory_service.py

import json
import os
from typing import List
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

# ✅ Memory file configuration
memory_file = "memory.txt"

def save_conversation(messages: List) -> None:
    """Save conversation messages to memory.txt file."""
    try:
        # Convert messages to serializable format
        serialized_messages = []
        for message in messages:
            message_dict = {
                "type": message.__class__.__name__,
                "content": message.content,
                "id": getattr(message, 'id', ''),
            }

            # Add tool-specific fields
            if hasattr(message, 'tool_call_id') and message.tool_call_id:
                message_dict["tool_call_id"] = message.tool_call_id
            
            # Add tool-specific fields
            if hasattr(message, 'tool_calls') and message.tool_calls:
                message_dict["tool_calls"] = message.tool_calls
            
            # Add additional_kwargs if present
            if hasattr(message, 'additional_kwargs') and message.additional_kwargs:
                message_dict["additional_kwargs"] = message.additional_kwargs
            
                
            serialized_messages.append(message_dict)
        
        # Save to file
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(serialized_messages, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Conversation saved to {memory_file}")
        
    except Exception as e:
        print(f"❌ Error saving conversation: {e}")

def load_conversation() -> List:
    """Load conversation messages from memory.txt file."""
    try:
        if not os.path.exists(memory_file):
            print(f"📝 No existing memory file found. Starting fresh conversation.")
            return []
        
        with open(memory_file, 'r', encoding='utf-8') as f:
            serialized_messages = json.load(f)
        
        # Convert back to message objects
        messages = []
        for msg_dict in serialized_messages:
            msg_type = msg_dict["type"]
            content = msg_dict["content"]
            
            if msg_type == "HumanMessage":
                message = HumanMessage(content=content)
            elif msg_type == "AIMessage":
                message = AIMessage(content=content)
            elif msg_type == "ToolMessage":
                # For ToolMessage, we need to handle missing tool_call_id
                tool_call_id = msg_dict.get("tool_call_id", "")
                name = msg_dict.get("name", "")
                
                # Only create ToolMessage if we have valid tool_call_id
                if tool_call_id and tool_call_id.strip():
                    message = ToolMessage(
                        content=content,
                        name=name,
                        tool_call_id=tool_call_id
                    )
                else:
                    # If no valid tool_call_id, create a simple AIMessage instead
                    print(f"⚠️ Converting invalid ToolMessage to AIMessage (missing tool_call_id)")
                    message = AIMessage(content=content)
            elif msg_type == "SystemMessage":
                message = SystemMessage(content=content)
            else:
                # Create a generic message for unknown types
                message = HumanMessage(content=content)
            
            # Restore additional attributes
            if "id" in msg_dict:
                message.id = msg_dict["id"]
            if "tool_calls" in msg_dict:
                message.tool_calls = msg_dict["tool_calls"]
            if "additional_kwargs" in msg_dict:
                message.additional_kwargs = msg_dict["additional_kwargs"]
            
            messages.append(message)
        
        print(f"📖 Loaded {len(messages)} messages from {memory_file}")
        return messages
        
    except Exception as e:
        print(f"❌ Error loading conversation: {e}")
        return []

def clear_memory() -> None:
    """Clear the memory file."""
    try:
        if os.path.exists(memory_file):
            os.remove(memory_file)
            print(f"🗑️ Memory file {memory_file} cleared")
        else:
            print(f"📝 No memory file to clear")
    except Exception as e:
        print(f"❌ Error clearing memory: {e}")

def print_memory_status() -> None:
    """Print the current status of memory file."""
    if os.path.exists(memory_file):
        size = os.path.getsize(memory_file)
        print(f"💾 Memory file exists: {memory_file} ({size} bytes)")
    else:
        print(f"📝 No memory file found: {memory_file}") 