#!/usr/bin/env python3
"""
Test script to validate docker-compose setup without actually running Docker.
This script checks configuration, dependencies, and port availability.
"""

import sys
import io
import os

# Fix Windows Unicode encoding issue
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import yaml
import json
from pathlib import Path

def load_compose_config(filepath):
    """Load and parse docker-compose.yml"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def load_env_file(filepath):
    """Load .env file variables"""
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def resolve_env_variables(value, env_vars):
    """Resolve ${VAR} and ${VAR:-default} patterns"""
    if not isinstance(value, str):
        return value
    
    import re
    pattern = r'\$\{([^}]+)\}'
    
    def replacer(match):
        var_spec = match.group(1)
        if ':-' in var_spec:
            var_name, default = var_spec.split(':-', 1)
            return env_vars.get(var_name.strip(), default)
        else:
            return env_vars.get(var_spec, match.group(0))
    
    return re.sub(pattern, replacer, value)

def validate_ports(config, env_vars):
    """Validate port mappings for conflicts"""
    ports_used = {}
    issues = []
    
    for service_name, service_config in config.get('services', {}).items():
        if 'ports' in service_config:
            for port_mapping in service_config['ports']:
                # Port mapping format: "host:container" or just "container"
                parts = str(port_mapping).split(':')
                if len(parts) == 2:
                    host_port = parts[0]
                else:
                    host_port = parts[0]
                
                # Resolve environment variables
                host_port = resolve_env_variables(host_port, env_vars)
                
                if host_port in ports_used:
                    issues.append(
                        f"Port conflict: {host_port} used by both "
                        f"{ports_used[host_port]} and {service_name}"
                    )
                else:
                    ports_used[host_port] = service_name
    
    return ports_used, issues

def validate_service_dependencies(config):
    """Validate service dependencies are resolvable"""
    services = set(config.get('services', {}).keys())
    issues = []
    
    for service_name, service_config in config.get('services', {}).items():
        depends_on = service_config.get('depends_on', {})
        
        if isinstance(depends_on, dict):
            for dep_service in depends_on.keys():
                if dep_service not in services:
                    issues.append(
                        f"Service '{service_name}' depends on non-existent "
                        f"service '{dep_service}'"
                    )
        elif isinstance(depends_on, list):
            for dep_service in depends_on:
                if dep_service not in services:
                    issues.append(
                        f"Service '{service_name}' depends on non-existent "
                        f"service '{dep_service}'"
                    )
    
    return issues

def validate_volumes(config):
    """Validate volume references"""
    defined_volumes = set(config.get('volumes', {}).keys())
    issues = []
    
    for service_name, service_config in config.get('services', {}).items():
        for volume in service_config.get('volumes', []):
            if isinstance(volume, str):
                # Named volume format: "volume_name:/path"
                # Bind mount format: "./path:/path" or "/path:/path"
                if ':' in volume:
                    vol_name = volume.split(':')[0].strip()
                    # Skip bind mounts (start with / or ./)
                    if not vol_name.startswith('/') and not vol_name.startswith('./') and vol_name not in defined_volumes:
                        issues.append(
                            f"Service '{service_name}' references undefined "
                            f"volume '{vol_name}'"
                        )
    
    return issues

def validate_networks(config):
    """Validate network references"""
    defined_networks = set(config.get('networks', {}).keys())
    # Also include default network
    defined_networks.add('default')
    
    issues = []
    
    for service_name, service_config in config.get('services', {}).items():
        service_networks = service_config.get('networks', [])
        if isinstance(service_networks, (list, dict)):
            if isinstance(service_networks, dict):
                service_networks = list(service_networks.keys())
            
            for network in service_networks:
                if network not in defined_networks:
                    issues.append(
                        f"Service '{service_name}' references undefined "
                        f"network '{network}'"
                    )
    
    return issues

def check_health_checks(config):
    """Report on health check coverage"""
    services = config.get('services', {})
    with_healthchecks = 0
    without_healthchecks = 0
    
    for service_name, service_config in services.items():
        if 'healthcheck' in service_config:
            with_healthchecks += 1
        else:
            without_healthchecks += 1
    
    return with_healthchecks, without_healthchecks

def check_resource_limits(config):
    """Report on resource limit coverage"""
    services = config.get('services', {})
    with_limits = 0
    without_limits = 0
    
    for service_name, service_config in services.items():
        if 'deploy' in service_config and 'resources' in service_config['deploy']:
            with_limits += 1
        else:
            without_limits += 1
    
    return with_limits, without_limits

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}")

def main():
    """Main validation routine"""
    compose_file = 'docker-compose.yml'
    env_file = '.env'
    
    if not os.path.exists(compose_file):
        print(f"✗ Error: {compose_file} not found")
        return False
    
    try:
        config = load_compose_config(compose_file)
        env_vars = load_env_file(env_file)
        
        print_section("Docker Compose Validation Report")
        
        # Basic structure
        print(f"\n✓ Configuration file: {compose_file}")
        print(f"✓ Environment file: {env_file} {'(found)' if env_vars else '(not found - using defaults)'}")
        print(f"✓ Compose version: {config.get('version', 'unknown')}")
        
        # Service summary
        services = config.get('services', {})
        print(f"\n✓ Services: {len(services)} total")
        for service_name in sorted(services.keys()):
            print(f"  - {service_name}")
        
        # Port validation
        print_section("Port Configuration")
        ports_used, port_issues = validate_ports(config, env_vars)
        print(f"\n✓ Ports used: {len(ports_used)}")
        # Sort ports, handling both numeric and string values
        sorted_ports = []
        for port, service in ports_used.items():
            try:
                sorted_ports.append((int(port), port, service))
            except ValueError:
                sorted_ports.append((9999, port, service))
        
        for _, port, service in sorted(sorted_ports):
            print(f"  {port:6} -> {service}")
        
        if port_issues:
            print("\n✗ Port conflicts detected:")
            for issue in port_issues:
                print(f"  - {issue}")
            return False
        
        # Dependency validation
        print_section("Service Dependencies")
        dep_issues = validate_service_dependencies(config)
        for service_name, service_config in sorted(services.items()):
            depends_on = service_config.get('depends_on', {})
            if depends_on:
                if isinstance(depends_on, dict):
                    deps = list(depends_on.keys())
                elif isinstance(depends_on, list):
                    deps = depends_on
                else:
                    deps = []
                print(f"\n✓ {service_name}")
                for dep in deps:
                    print(f"  → {dep}")
        
        if dep_issues:
            print("\n✗ Dependency issues found:")
            for issue in dep_issues:
                print(f"  - {issue}")
            return False
        
        # Volume validation
        print_section("Volume Configuration")
        vol_issues = validate_volumes(config)
        volumes = config.get('volumes', {})
        print(f"\n✓ Named volumes: {len(volumes)}")
        for volume_name in sorted(volumes.keys()):
            print(f"  - {volume_name}")
        
        if vol_issues:
            print("\n✗ Volume issues found:")
            for issue in vol_issues:
                print(f"  - {issue}")
            return False
        
        # Network validation
        print_section("Network Configuration")
        net_issues = validate_networks(config)
        networks = config.get('networks', {})
        print(f"\n✓ Networks: {len(networks)}")
        for network_name, network_config in sorted(networks.items()):
            if isinstance(network_config, dict):
                driver = network_config.get('driver', 'bridge')
            else:
                driver = 'bridge'
            print(f"  - {network_name} (driver: {driver})")
        
        if net_issues:
            print("\n✗ Network issues found:")
            for issue in net_issues:
                print(f"  - {issue}")
            return False
        
        # Health checks
        print_section("Health Checks")
        with_hc, without_hc = check_health_checks(config)
        print(f"\n✓ Services with health checks: {with_hc}/{len(services)}")
        print(f"⚠ Services without health checks: {without_hc}/{len(services)}")
        
        # Resource limits
        print_section("Resource Limits")
        with_limits, without_limits = check_resource_limits(config)
        print(f"\n✓ Services with resource limits: {with_limits}/{len(services)}")
        print(f"⚠ Services without resource limits: {without_limits}/{len(services)}")
        
        # Environment variables
        print_section("Environment Variables")
        env_vars_used = set()
        for service_name, service_config in services.items():
            env = service_config.get('environment', {})
            if isinstance(env, dict):
                for key, value in env.items():
                    if isinstance(value, str) and '${' in value:
                        import re
                        matches = re.findall(r'\$\{([^}:]+)', value)
                        env_vars_used.update(matches)
        
        if env_vars_used:
            print(f"\n✓ Environment variables referenced: {len(env_vars_used)}")
            for var in sorted(env_vars_used):
                value = env_vars.get(var, '<NOT SET>')
                print(f"  ${{{var}}} = {value}")
        
        # Final summary
        print_section("Validation Summary")
        print("\n✓ VALIDATION PASSED - All checks completed successfully")
        print("\nYou can now start the services with:")
        print("  docker-compose up -d")
        print("\nTo view logs:")
        print("  docker-compose logs -f")
        print("\nTo stop services:")
        print("  docker-compose stop")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"\n✗ YAML Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
