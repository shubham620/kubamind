#!/usr/bin/env python3
"""Validate docker-compose.yml configuration"""

import sys
import io
import os

# Fix Windows Unicode encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import yaml

def validate_compose_file(filepath):
    """Validate docker-compose.yml file"""
    try:
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
        
        if not config:
            print("✗ Error: Empty docker-compose.yml file")
            return False
        
        print("✓ YAML syntax is valid")
        
        # Validate version
        version = config.get('version')
        print(f"✓ Docker Compose version: {version}")
        
        # Validate services
        services = config.get('services', {})
        print(f"\n✓ Found {len(services)} services:")
        
        required_services = [
            'postgres', 'redis', 'qdrant', 'prometheus', 
            'grafana', 'loki', 'backend', 'node-exporter', 'ollama'
        ]
        
        found_services = list(services.keys())
        for service in required_services:
            if service in found_services:
                print(f"  ✓ {service}")
            else:
                print(f"  ✗ {service} - MISSING")
                return False
        
        # Validate service configurations
        print("\n✓ Service configurations:")
        for service_name, service_config in services.items():
            has_healthcheck = 'healthcheck' in service_config
            has_restart = 'restart' in service_config
            has_logging = 'logging' in service_config
            has_resources = 'deploy' in service_config and 'resources' in service_config.get('deploy', {})
            
            status = []
            if has_healthcheck:
                status.append("HC")
            if has_restart:
                status.append("RST")
            if has_logging:
                status.append("LOG")
            if has_resources:
                status.append("RES")
            
            status_str = "[" + ",".join(status) + "]" if status else "[-]"
            print(f"  {service_name:20} {status_str}")
        
        # Validate volumes
        volumes = config.get('volumes', {})
        print(f"\n✓ Found {len(volumes)} volumes:")
        for volume_name in sorted(volumes.keys()):
            print(f"  - {volume_name}")
        
        # Validate networks
        networks = config.get('networks', {})
        print(f"\n✓ Found {len(networks)} networks:")
        for network_name, network_config in networks.items():
            driver = network_config.get('driver', 'default') if isinstance(network_config, dict) else 'default'
            print(f"  - {network_name} (driver: {driver})")
        
        # Check environment variable references
        print("\n✓ Environment variable references detected:")
        env_vars_found = set()
        
        for service_name, service_config in services.items():
            env = service_config.get('environment', {})
            if isinstance(env, dict):
                for key, value in env.items():
                    if isinstance(value, str) and '${' in value:
                        env_var = value.split('${')[1].split('}')[0].split(':-')[0]
                        env_vars_found.add(env_var)
        
        for var in sorted(env_vars_found):
            print(f"  ${{{var}}}")
        
        # Check for proper dependencies
        print("\n✓ Service dependencies:")
        for service_name, service_config in services.items():
            depends_on = service_config.get('depends_on', {})
            if depends_on:
                if isinstance(depends_on, list):
                    print(f"  {service_name}: {', '.join(depends_on)}")
                elif isinstance(depends_on, dict):
                    deps = list(depends_on.keys())
                    print(f"  {service_name}: {', '.join(deps)}")
        
        print("\n" + "="*60)
        print("✓ Docker Compose configuration is VALID")
        print("="*60)
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: File not found: {filepath}")
        return False
    except yaml.YAMLError as e:
        print(f"✗ YAML Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    compose_file = 'docker-compose.yml'
    if not validate_compose_file(compose_file):
        sys.exit(1)
