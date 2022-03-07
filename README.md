# Carnegie_POM_setup


Purpose: 

The setup uses the Page Object Model design pattern to allow for improved test case maintenance.

With the configuration.yaml file and config_verification.py file the setup allows testers to easily specify browsers/window sizes/verify browser version being tested against.


Project tree 

<pre>
.
├── base_file.py
├── config_verification.py
├── configuration.yaml
├── conftest.py
├── pages
│   ├── __init__.py
│   ├── base_page.py
│   └── homepage.py
└── tests
    ├── __init__.py
    └── test_scripts
        ├── __init__.py
        └── test_Carnegie_HP.py
</pre>



<pre>

configuration.yaml

Accepted values :

BROWSER_PARAMS: List [] or string 
BROWSER_VERSION: Any
HEADLESS: Bool
SCREEN_SIZE: CUSTOM or FULLSCREEN
SCREEN_WIDTH: > 0 
SCREEN_HEIGHT: > 0 

1) If a value does not match the specified type or value an error will be thrown and the test will fail to run.
2) If the entered Browser version does not match the actual browser version for the browser installed the test will fail to run.
The installed browser version is specified in the values for the different browsers specified in the BROWSER_EXE_PATHS. 
</pre>

