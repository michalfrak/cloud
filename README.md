# Cloud
This covers any code that is specific to a cloud providers components such
as file systems, lambda functions, key management systems etc.

## File structure
- `__init__.py` -> initialize singleton object for specific provider defined as environmental variable
- `const.py` -> defines enum with possible cloud provider options
- `cloud_api.py` -> class with all services functionality
- `<component_name>` -> folder with all implementations for single component (like file storage etc.)
    - `basic.py` -> abstract class with all defined functions for single service
    - `local.py` -> implementation for local/developer environment
    - `<provider_name>.py` -> implementation of component for particular cloud provider

### Setting cloud provider
Type of cloud provider used in code is defined by `CLOUD_PROVIDER` env var based on `CloudProviderType` enum
inside `const.py`. Local enviroment is set as default value.

### Adding new cloud provider code
To add another cloud provider specific code you need to:
- define new enum value in `const.py`
- add file with implementation for every component
- update `CloudApi` class in `cloud_api.py` to include new provider

### Adding new component
To add new component for providers you need to:
- create new folder with same structure as in other components
- update `CloudApi` class in `cloud_api.py` to initialize new component on creation

## Usage
It is designed to be used as singleton class within code, so importing should be done like that:
```python
from cloud import cloud_api

```

Initializing all components are done in object creation, all functionality for single component is accesed
by public member of class which is object for specific component with implementation. For example storing
data on aws s3 file storage in code can be achieved like:

```python
cloud_api.storage.save_file(filename)
```


## Future development
Adding new component/cloud provider should be done in agile manner, step by step. Classes defined
in `basic.py` are interfaces with public methods that all implementation should follow. Code will differ
for each provider, but calling them should be done the same way.

Right now new components were implemented based on aws functions/clients, already existing code should be refactored
to be more generic when implementing new providers.
