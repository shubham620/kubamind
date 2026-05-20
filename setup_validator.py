#!/usr/bin/env python3
"""
KubeMind AI End-to-End Setup Validator
Verifies all components are properly configured and functional
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Tuple, List
import requests
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    
def print_status(message: str, status: str = "INFO"):
    colors = {
        "SUCCESS": Colors.GREEN,
        "ERROR": Colors.RED,
        "WARNING": Colors.YELLOW,
        "INFO": Colors.BLUE,
    }
    color = colors.get(status, Colors.BLUE)
    symbol = {
        "SUCCESS": "✓",
        "ERROR": "✗",
        "WARNING": "⚠",
        "INFO": "ℹ",
    }[status]
    print(f"{color}[{symbol}] {message}{Colors.END}")

def check_docker_installed() -> bool:
    """Check if Docker is installed"""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print_status("Docker is installed", "SUCCESS")
        return True
    except:
        print_status("Docker is not installed", "ERROR")
        return False

def check_docker_compose_installed() -> bool:
    """Check if Docker Compose is installed"""
    try:
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print_status("Docker Compose is installed", "SUCCESS")
        return True
    except:
        print_status("Docker Compose is not installed", "ERROR")
        return False

def check_python_version() -> bool:
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} is compatible", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor} requires >= 3.10", "ERROR")
        return False

def check_node_installed() -> bool:
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, check=True, text=True)
        print_status(f"Node.js {result.stdout.strip()} is installed", "SUCCESS")
        return True
    except:
        print_status("Node.js is not installed", "ERROR")
        return False

def check_project_structure() -> bool:
    """Check if project structure is complete"""
    required_dirs = [
        "backend",
        "frontend",
        "kubernetes",
        "docker",
        "monitoring",
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists():
            print_status(f"Directory '{dir_name}' exists", "SUCCESS")
        else:
            print_status(f"Directory '{dir_name}' is missing", "ERROR")
            all_exist = False
    
    return all_exist

def check_required_files() -> bool:
    """Check if required files exist"""
    required_files = [
        "docker-compose.yml",
        "backend/requirements.txt",
        "frontend/package.json",
        "kubernetes/base-services.yaml",
        "kubernetes/backend-deployment.yaml",
        ".github/workflows/build-and-deploy.yaml",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print_status(f"File '{file_path}' exists", "SUCCESS")
        else:
            print_status(f"File '{file_path}' is missing", "ERROR")
            all_exist = False
    
    return all_exist

def check_docker_compose_syntax() -> bool:
    """Validate docker-compose.yml syntax"""
    try:
        result = subprocess.run(
            ["docker-compose", "config"],
            capture_output=True,
            check=True,
            text=True
        )
        print_status("docker-compose.yml syntax is valid", "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"docker-compose.yml syntax error: {e.stderr}", "ERROR")
        return False

def check_kubernetes_manifests() -> bool:
    """Validate Kubernetes manifest syntax"""
    manifests = [
        "kubernetes/base-services.yaml",
        "kubernetes/backend-deployment.yaml",
        "kubernetes/frontend-ingress.yaml",
    ]
    
    all_valid = True
    for manifest_path in manifests:
        path = Path(manifest_path)
        if not path.exists():
            print_status(f"Kubernetes manifest '{manifest_path}' not found", "ERROR")
            all_valid = False
            continue
        
        try:
            with open(path) as f:
                import yaml
                yaml.safe_load_all(f)
            print_status(f"Kubernetes manifest '{manifest_path}' is valid", "SUCCESS")
        except Exception as e:
            print_status(f"Kubernetes manifest '{manifest_path}' is invalid: {e}", "ERROR")
            all_valid = False
    
    return all_valid

def check_backend_requirements() -> bool:
    """Check if all backend requirements can be read"""
    try:
        with open("backend/requirements.txt") as f:
            requirements = f.readlines()
            print_status(f"Backend requirements file contains {len(requirements)} packages", "SUCCESS")
            return True
    except Exception as e:
        print_status(f"Cannot read backend requirements: {e}", "ERROR")
        return False

def check_frontend_dependencies() -> bool:
    """Check if frontend package.json is valid"""
    try:
        with open("frontend/package.json") as f:
            data = json.load(f)
            print_status(f"Frontend has {len(data.get('dependencies', {}))} dependencies", "SUCCESS")
            return True
    except Exception as e:
        print_status(f"Frontend package.json is invalid: {e}", "ERROR")
        return False

def check_api_endpoints() -> bool:
    """Check if API endpoints are responding"""
    endpoints = [
        ("http://localhost:8000/health", "Health Check"),
        ("http://localhost:8000/docs", "API Documentation"),
    ]
    
    all_healthy = True
    for url, name in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print_status(f"{name} endpoint is responding", "SUCCESS")
            else:
                print_status(f"{name} endpoint returned {response.status_code}", "WARNING")
        except requests.exceptions.ConnectionError:
            print_status(f"{name} endpoint is not reachable (API not running)", "WARNING")
        except Exception as e:
            print_status(f"{name} endpoint error: {e}", "WARNING")
    
    return True

def check_frontend_startup() -> bool:
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print_status("Frontend is responding on port 3000", "SUCCESS")
            return True
    except requests.exceptions.ConnectionError:
        print_status("Frontend is not running on port 3000", "WARNING")
        return False
    except Exception as e:
        print_status(f"Frontend check error: {e}", "WARNING")
        return False

def run_diagnostics():
    """Run all diagnostics"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("KubeMind AI - End-to-End Setup Validator")
    print(f"{'='*60}{Colors.END}\n")
    
    checks = []
    
    print(f"{Colors.BLUE}[1/5] Checking Prerequisites...{Colors.END}")
    checks.append(check_docker_installed())
    checks.append(check_docker_compose_installed())
    checks.append(check_python_version())
    checks.append(check_node_installed())
    
    print(f"\n{Colors.BLUE}[2/5] Checking Project Structure...{Colors.END}")
    checks.append(check_project_structure())
    checks.append(check_required_files())
    
    print(f"\n{Colors.BLUE}[3/5] Validating Configuration Files...{Colors.END}")
    checks.append(check_docker_compose_syntax())
    checks.append(check_kubernetes_manifests())
    
    print(f"\n{Colors.BLUE}[4/5] Validating Dependencies...{Colors.END}")
    checks.append(check_backend_requirements())
    checks.append(check_frontend_dependencies())
    
    print(f"\n{Colors.BLUE}[5/5] Checking Running Services...{Colors.END}")
    check_api_endpoints()
    check_frontend_startup()
    
    print(f"\n{Colors.BLUE}{'='*60}")
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print_status(f"All {total} checks passed! Ready for deployment.", "SUCCESS")
        print(f"{'='*60}{Colors.END}\n")
        return 0
    else:
        print_status(f"{passed}/{total} checks passed. Please fix errors above.", "WARNING")
        print(f"{'='*60}{Colors.END}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(run_diagnostics())
    except KeyboardInterrupt:
        print_status("\nValidator interrupted", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
        sys.exit(1)
