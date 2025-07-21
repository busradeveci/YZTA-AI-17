#!/usr/bin/env python3
"""
YZTA-AI-17 Deployment Script
===========================

This script helps deploy the medical prediction system to production environments.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class DeploymentManager:
    """Handles deployment tasks for YZTA-AI-17."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "yzta-ai-17"
    
    def check_production_requirements(self):
        """Check if production requirements are met."""
        print("🔍 Checking production requirements...")
        
        checks = []
        
        # Check Python version
        if sys.version_info >= (3, 8):
            checks.append(("✅", "Python version >= 3.8"))
        else:
            checks.append(("❌", f"Python version {sys.version} < 3.8"))
        
        # Check if in virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            checks.append(("✅", "Virtual environment active"))
        else:
            checks.append(("⚠️", "Virtual environment not detected"))
        
        # Check required files
        required_files = [
            "app/__init__.py",
            "config.py",
            "requirements.txt",
            "run.py"
        ]
        
        for file_path in required_files:
            if (self.project_root / file_path).exists():
                checks.append(("✅", f"Required file: {file_path}"))
            else:
                checks.append(("❌", f"Missing file: {file_path}"))
        
        # Print results
        for status, message in checks:
            print(f"  {status} {message}")
        
        # Return success status
        failed_checks = [c for c in checks if c[0] == "❌"]
        return len(failed_checks) == 0
    
    def install_production_dependencies(self):
        """Install production dependencies."""
        print("📦 Installing production dependencies...")
        
        try:
            # Install gunicorn for production
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "gunicorn"
            ])
            
            # Install requirements
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            
            print("✅ Production dependencies installed successfully.")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def create_gunicorn_config(self):
        """Create Gunicorn configuration file."""
        print("⚙️ Creating Gunicorn configuration...")
        
        config_content = '''
# Gunicorn configuration for YZTA-AI-17
# =====================================

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "yzta-ai-17"

# Server mechanics
daemon = False
pidfile = "yzta-ai-17.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment and configure for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Application
pythonpath = "."
'''
        
        try:
            with open(self.project_root / "gunicorn.conf.py", "w") as f:
                f.write(config_content.strip())
            
            # Create logs directory
            logs_dir = self.project_root / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            print("✅ Gunicorn configuration created.")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Gunicorn config: {e}")
            return False
    
    def create_systemd_service(self):
        """Create systemd service file for Linux deployment."""
        print("🔧 Creating systemd service file...")
        
        service_content = f'''[Unit]
Description=YZTA-AI-17 Medical Prediction System
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory={self.project_root}
Environment=PATH={sys.executable}
ExecStart={sys.executable} -m gunicorn --config gunicorn.conf.py "app:create_app()"
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
'''
        
        try:
            service_file = self.project_root / f"{self.app_name}.service"
            with open(service_file, "w") as f:
                f.write(service_content)
            
            print(f"✅ Systemd service file created: {service_file}")
            print("   To install:")
            print(f"   sudo cp {service_file} /etc/systemd/system/")
            print(f"   sudo systemctl enable {self.app_name}")
            print(f"   sudo systemctl start {self.app_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating systemd service: {e}")
            return False
    
    def create_nginx_config(self):
        """Create Nginx configuration for reverse proxy."""
        print("🌐 Creating Nginx configuration...")
        
        nginx_content = f'''# Nginx configuration for YZTA-AI-17
server {{
    listen 80;
    server_name your-domain.com;  # Change this to your domain
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Static files
    location /static/ {{
        alias {self.project_root}/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
    
    # Main application
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }}
    
    # Health check endpoint
    location /health {{
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }}
}}

# HTTPS configuration (uncomment and configure SSL certificates)
# server {{
#     listen 443 ssl http2;
#     server_name your-domain.com;
#     
#     ssl_certificate /path/to/certificate.crt;
#     ssl_certificate_key /path/to/private.key;
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
#     ssl_prefer_server_ciphers off;
#     
#     # Include the same location blocks as above
# }}
'''
        
        try:
            nginx_file = self.project_root / f"{self.app_name}.nginx"
            with open(nginx_file, "w") as f:
                f.write(nginx_content)
            
            print(f"✅ Nginx configuration created: {nginx_file}")
            print("   To install:")
            print(f"   sudo cp {nginx_file} /etc/nginx/sites-available/{self.app_name}")
            print(f"   sudo ln -s /etc/nginx/sites-available/{self.app_name} /etc/nginx/sites-enabled/")
            print("   sudo nginx -t && sudo systemctl reload nginx")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Nginx config: {e}")
            return False
    
    def create_docker_files(self):
        """Create Docker configuration files."""
        print("🐳 Creating Docker configuration...")
        
        # Dockerfile
        dockerfile_content = '''FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app()"]
'''
        
        # Docker Compose
        docker_compose_content = '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FASTAPI_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./yzta-ai-17.nginx:/etc/nginx/conf.d/default.conf
      - ./static:/app/static
    depends_on:
      - web
    restart: unless-stopped
'''
        
        try:
            # Write Dockerfile
            with open(self.project_root / "Dockerfile", "w") as f:
                f.write(dockerfile_content)
            
            # Write docker-compose.yml
            with open(self.project_root / "docker-compose.yml", "w") as f:
                f.write(docker_compose_content)
            
            # Create .dockerignore
            dockerignore_content = '''__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.swp
*.swo
node_modules
'''
            
            with open(self.project_root / ".dockerignore", "w") as f:
                f.write(dockerignore_content)
            
            print("✅ Docker configuration created.")
            print("   To build and run:")
            print("   docker-compose up --build")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Docker files: {e}")
            return False
    
    def run_production_tests(self):
        """Run tests in production mode."""
        print("🧪 Running production tests...")
        
        try:
            # Set production environment
            os.environ['FASTAPI_ENV'] = 'production'
            
            # Run tests
            result = subprocess.run([
                sys.executable, "tests/test_system.py", "--all"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All production tests passed.")
                return True
            else:
                print("❌ Some production tests failed.")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False
    
    def deploy(self, deployment_type="gunicorn"):
        """Deploy the application."""
        print(f"🚀 Deploying YZTA-AI-17 with {deployment_type}...")
        
        # Check requirements
        if not self.check_production_requirements():
            print("❌ Production requirements not met. Aborting deployment.")
            return False
        
        # Install dependencies
        if not self.install_production_dependencies():
            print("❌ Failed to install dependencies. Aborting deployment.")
            return False
        
        # Run tests
        if not self.run_production_tests():
            print("⚠️ Tests failed. Continue anyway? (y/N)")
            response = input().lower()
            if response != 'y':
                print("❌ Deployment aborted.")
                return False
        
        # Create configuration files
        success = True
        
        if deployment_type in ["gunicorn", "all"]:
            success &= self.create_gunicorn_config()
        
        if deployment_type in ["systemd", "all"]:
            success &= self.create_systemd_service()
        
        if deployment_type in ["nginx", "all"]:
            success &= self.create_nginx_config()
        
        if deployment_type in ["docker", "all"]:
            success &= self.create_docker_files()
        
        if success:
            print("✅ Deployment configuration completed successfully!")
            print("\n📋 Next steps:")
            print("1. Review and customize configuration files")
            print("2. Set up SSL certificates for HTTPS")
            print("3. Configure firewall and security settings")
            print("4. Set up monitoring and logging")
            print("5. Create backup procedures")
            print("\n⚠️ Remember to:")
            print("- Change default passwords and secrets")
            print("- Configure proper file permissions")
            print("- Set up log rotation")
            print("- Test the deployment thoroughly")
        else:
            print("❌ Deployment configuration failed.")
        
        return success


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="YZTA-AI-17 Deployment Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('action', choices=[
        'check', 'gunicorn', 'systemd', 'nginx', 'docker', 'all'
    ], help='Deployment action to perform')
    
    args = parser.parse_args()
    
    deployment_manager = DeploymentManager()
    
    if args.action == 'check':
        success = deployment_manager.check_production_requirements()
    else:
        success = deployment_manager.deploy(args.action)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
