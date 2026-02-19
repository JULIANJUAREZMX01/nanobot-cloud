"""Backup service for S3 storage"""

import asyncio
from pathlib import Path
import zipfile
import tempfile
from datetime import datetime
from app.config import Settings
from app.utils import get_logger

logger = get_logger(__name__)


class BackupService:
    """Handle backups to S3"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.s3_client = None
        
        if settings.aws_access_key_id and settings.s3_bucket:
            self._init_s3()
    
    def _init_s3(self):
        """Initialize S3 client"""
        try:
            import boto3
            self.s3_client = boto3.client(
                "s3",
                region_name=self.settings.aws_region,
                aws_access_key_id=self.settings.aws_access_key_id,
                aws_secret_access_key=self.settings.aws_secret_access_key
            )
            logger.info("S3 client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize S3: {e}")
    
    async def backup_workspace(self) -> bool:
        """Backup workspace to S3"""
        if not self.s3_client:
            logger.warning("S3 not configured, skipping backup")
            return False
        
        try:
            workspace_path = Path("./workspace")
            if not workspace_path.exists():
                logger.warning("Workspace directory not found")
                return False
            
            # Create zip file
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
            
            self.s3_client.upload_file(
                str(tmp_path),
                self.settings.s3_bucket,
                s3_key
            )
            
            logger.info(f"Workspace backed up to S3: {s3_key}")
            tmp_path.unlink()
            return True
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    async def scheduled_backup(self, interval_hours: int = 6):
        """Run backups on schedule"""
        while True:
            try:
                await self.backup_workspace()
                await asyncio.sleep(interval_hours * 3600)
            except Exception as e:
                logger.error(f"Scheduled backup error: {e}")
                await asyncio.sleep(60)
