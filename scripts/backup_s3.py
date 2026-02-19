#!/usr/bin/env python3
"""Backup workspace to S3"""

import os
import sys
import boto3
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime

def backup_to_s3():
    """Backup workspace directory to S3"""
    
    # Configuration
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket = os.getenv("S3_BUCKET")
    region = os.getenv("AWS_REGION", "us-east-1")
    
    if not all([aws_key, aws_secret, bucket]):
        print("⚠️  S3 credentials not configured, skipping backup")
        return True
    
    try:
        # Initialize S3
        s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret
        )
        
        # Find workspace
        workspace_path = Path("./workspace")
        if not workspace_path.exists():
            print("⚠️  Workspace not found, skipping backup")
            return True
        
        # Create zip
        print("📦 Creating backup...")
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in workspace_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(workspace_path.parent)
                    zf.write(file_path, arcname)
        
        # Upload to S3
        timestamp = datetime.utcnow().isoformat()
        s3_key = f"backups/workspace_{timestamp}.zip"
        
        print(f"📤 Uploading to S3: {s3_key}")
        s3.upload_file(str(tmp_path), bucket, s3_key)
        
        tmp_path.unlink()
        print("✅ Backup complete")
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    success = backup_to_s3()
    sys.exit(0 if success else 1)
