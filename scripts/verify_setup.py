#!/usr/bin/env python3
"""
Nanobot Setup Verification Script
Checks if the local environment is correctly configured for Cloud/Telegram deployment.
"""

import os
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check_file(path, description):
    if path.exists():
        print(f"{GREEN}✅ Found {description}: {path}{RESET}")
        return True
    else:
        print(f"{RED}❌ Missing {description}: {path}{RESET}")
        return False

def check_env_var(file_path, var_name):
    if not file_path.exists():
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if f"{var_name}=" in content and not f"{var_name}=your_" in content:
            print(f"{GREEN}✅ {var_name} is set in .env{RESET}")
            return True
        else:
            print(f"{YELLOW}⚠️ {var_name} might be missing or default in .env{RESET}")
            return False

def main():
    print(f"\n{GREEN}=== Nanobot Environment Verification ==={RESET}\n")
    
    base_dir = Path(os.getcwd())
    
    # 1. Critical Files
    print(f"{YELLOW}Checking Critical Files...{RESET}")
    files_to_check = [
        ("app/main.py", "Main Application"),
        ("pyproject.toml", "Dependencies File"),
        ("infrastructure/Dockerfile", "Dockerfile"),
        ("workspace/SOUL.md", "Soul (Identity)"),
        ("workspace/USER.md", "User Profile"),
        ("workspace/MEMORY.md", "Long-term Memory"),
    ]
    
    all_files_exist = True
    for rel_path, desc in files_to_check:
        if not check_file(base_dir / rel_path, desc):
            all_files_exist = False
            
    # 2. Environment Variables (.env)
    print(f"\n{YELLOW}Checking Environment Configuration...{RESET}")
    env_file = base_dir / ".env"
    if env_file.exists():
        print(f"{GREEN}✅ Found .env file{RESET}")
        check_env_var(env_file, "TELEGRAM_TOKEN")
        check_env_var(env_file, "GROQ_API_KEY")
        check_env_var(env_file, "ANTHROPIC_API_KEY")
    else:
        print(f"{RED}❌ Missing .env file (Copy .env.example to .env and configure it){RESET}")
        
    # 3. Workspace Validity
    print(f"\n{YELLOW}Checking Workspace...{RESET}")
    user_md = base_dir / "workspace/USER.md"
    if user_md.exists():
        with open(user_md, 'r', encoding='utf-8') as f:
            content = f.read()
            if "QUINTANA" in content:
                print(f"{GREEN}✅ USER.md is personalized for QUINTANA{RESET}")
            else:
                print(f"{YELLOW}⚠️ USER.md might be generic (Update with your details){RESET}")

    # Summary
    print(f"\n{GREEN}=== Verification Complete ==={RESET}")
    if all_files_exist:
        print(f"{GREEN}Result: Ready for Deployment! 🚀{RESET}")
    else:
        print(f"{RED}Result: Fix missing files before deploying.{RESET}")

if __name__ == "__main__":
    main()
