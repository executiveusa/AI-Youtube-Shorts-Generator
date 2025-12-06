#!/usr/bin/env python3
"""
Deployment Configuration Validator

Validates all deployment-related configuration files and settings
to ensure the repository is ready for Railway zero-secrets deployment.

Usage:
    python validate_deployment.py
"""

import os
import sys
import json

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False

def validate_json_file(filepath, description):
    """Validate JSON file syntax"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"✓ {description} is valid JSON")
        return True, data
    except json.JSONDecodeError as e:
        print(f"✗ {description} has invalid JSON: {e}")
        return False, None
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False, None

def validate_toml_file(filepath, description):
    """Validate TOML file syntax"""
    try:
        import toml
        with open(filepath, 'r') as f:
            data = toml.load(f)
        print(f"✓ {description} is valid TOML")
        return True, data
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False, None

def validate_gitignore():
    """Validate .gitignore includes secret protection"""
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required_entries = ['.env', 'master.secrets.json', '*.key', '*.pem']
    all_present = all(entry in content for entry in required_entries)
    
    if all_present:
        print("✓ .gitignore includes secret protection")
        return True
    else:
        print("✗ .gitignore missing some secret protection entries")
        return False

def validate_agents_schema(agents_data):
    """Validate .agents file structure"""
    required_keys = ['project', 'core', 'optional', 'required_secrets', 'schema']
    
    for key in required_keys:
        if key not in agents_data:
            print(f"✗ .agents missing required key: {key}")
            return False
    
    print(f"✓ .agents schema is complete")
    print(f"  - Project: {agents_data['project']}")
    print(f"  - Core variables: {len(agents_data['core'])}")
    print(f"  - Optional variables: {len(agents_data['optional'])}")
    print(f"  - Required secrets: {len(agents_data['required_secrets'])}")
    return True

def validate_railway_config(railway_data):
    """Validate railway.toml configuration"""
    try:
        assert railway_data['build']['builder'] == 'nixpacks'
        assert 'startCommand' in railway_data['deploy']
        assert 'memoryLimit' in railway_data['deploy']['resources']
        assert 'cpuLimit' in railway_data['deploy']['resources']
        
        print("✓ railway.toml configuration is valid")
        print(f"  - Builder: {railway_data['build']['builder']}")
        print(f"  - Start command: {railway_data['deploy']['startCommand']}")
        print(f"  - Memory limit: {railway_data['deploy']['resources']['memoryLimit']}")
        print(f"  - CPU limit: {railway_data['deploy']['resources']['cpuLimit']}")
        return True
    except (KeyError, AssertionError) as e:
        print(f"✗ railway.toml configuration error: {e}")
        return False

def validate_nixpacks_config(nixpacks_data):
    """Validate nixpacks.toml configuration"""
    try:
        assert 'phases' in nixpacks_data
        assert 'start' in nixpacks_data
        assert 'cmd' in nixpacks_data['start']
        
        print("✓ nixpacks.toml configuration is valid")
        print(f"  - Start command: {nixpacks_data['start']['cmd']}")
        return True
    except (KeyError, AssertionError) as e:
        print(f"✗ nixpacks.toml configuration error: {e}")
        return False

def validate_python_fallback():
    """Validate Python code has proper fallback logic"""
    try:
        # Set test environment
        os.environ['OPENAI_API'] = 'DISABLED'
        
        # Test import
        from Components.LanguageTasks import STUB_MODE
        
        if STUB_MODE:
            print("✓ LanguageTasks.py zero-secrets mode working")
            return True
        else:
            print("✗ LanguageTasks.py zero-secrets mode not activated")
            return False
    except Exception as e:
        print(f"✗ LanguageTasks.py import error: {e}")
        return False

def main():
    """Run all validations"""
    print("=" * 60)
    print("Railway Zero-Secrets Deployment Validator")
    print("=" * 60)
    print()
    
    results = []
    
    # Check required files exist
    print("Checking required files...")
    results.append(check_file_exists('.agents', '.agents file'))
    results.append(check_file_exists('railway.toml', 'railway.toml'))
    results.append(check_file_exists('nixpacks.toml', 'nixpacks.toml'))
    results.append(check_file_exists('Procfile', 'Procfile'))
    results.append(check_file_exists('maintenance.html', 'maintenance.html'))
    results.append(check_file_exists('cost_monitor.py', 'cost_monitor.py'))
    results.append(check_file_exists('.env.example', '.env.example'))
    results.append(check_file_exists('master.secrets.json.template', 'master.secrets.json.template'))
    results.append(check_file_exists('RAILWAY_DEPLOYMENT.md', 'RAILWAY_DEPLOYMENT.md'))
    results.append(check_file_exists('COOLIFY_SUPPORT.md', 'COOLIFY_SUPPORT.md'))
    results.append(check_file_exists('COOLIFY_MIGRATION.md', 'COOLIFY_MIGRATION.md'))
    print()
    
    # Validate JSON files
    print("Validating JSON configurations...")
    valid, agents_data = validate_json_file('.agents', '.agents file')
    results.append(valid)
    if valid:
        results.append(validate_agents_schema(agents_data))
    
    valid, secrets_data = validate_json_file('master.secrets.json.template', 'master.secrets.json.template')
    results.append(valid)
    print()
    
    # Validate TOML files
    print("Validating TOML configurations...")
    valid, railway_data = validate_toml_file('railway.toml', 'railway.toml')
    results.append(valid)
    if valid:
        results.append(validate_railway_config(railway_data))
    
    valid, nixpacks_data = validate_toml_file('nixpacks.toml', 'nixpacks.toml')
    results.append(valid)
    if valid:
        results.append(validate_nixpacks_config(nixpacks_data))
    print()
    
    # Validate .gitignore
    print("Validating security configurations...")
    results.append(validate_gitignore())
    print()
    
    # Validate Python fallback
    print("Validating zero-secrets mode...")
    results.append(validate_python_fallback())
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Validation Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All validations passed! Repository is ready for deployment.")
        return 0
    else:
        print("⚠️  Some validations failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
