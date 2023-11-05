# tests/core/test_config.py
import os
from src.core.config import Settings

def test_environment_variables_are_loaded(mocker):
    # Mocking the environment variables using mocker.patch.dict
    # This temporarily sets the SUPABASE_URL and SUPABASE_KEY environment variables for this test.
    mocker.patch.dict(os.environ, {"SUPABASE_URL": "mock_url", "SUPABASE_KEY": "mock_key", "CORS_ORIGINS": "mock_origins"})
    
    # Initialize the Settings object which should now load the mocked environment variables.
    settings = Settings()
    
    assert settings.SUPABASE_URL == "mock_url"
    assert settings.SUPABASE_KEY == "mock_key"
    assert settings.CORS_ORIGINS == "mock_origins"

def test_default_values_are_used(mocker):
    # Clearing the environment variables for this test to check default handling.
    mocker.patch.dict(os.environ, {}, clear=True)
    
    # Initialize Settings, it should now use the default values specified in its definition.
    settings = Settings()
    
    # Assert that the defaults are used.
    assert settings.SUPABASE_URL == None
    assert settings.SUPABASE_KEY == None
    assert settings.CORS_ORIGINS == "http://localhost:3000"
