---
source_filename: settings
---

### How to set the settings
To set DRF docs' settings just include the dictionary below in Django's `settings.py` file.

    REST_FRAMEWORK_DOCS = {
        'HIDE_DOCS': True,
        'HIDE_LIVE_ENDPOINTS': True,
        'HIDE_HIDDEN_FIELDS': True
    }


### Settings Description

##### HIDE_DOCS
You can use hidden to prevent your docs from showing up in different environments (ie. Show in development, hide in production). To do so you can use environment variables.

    REST_FRAMEWORK_DOCS = {
        'HIDE_DOCS': os.environ.get('HIDE_DRFDOCS', False)
    }

Then set the value of the environment variable `HIDE_DRFDOCS` for each environment (ie. Use `.env` files)

##### HIDE_LIVE_ENDPOINTS
You can use ```HIDE_LIVE_ENDPOINTS``` to hide the live endpoints feature on the documentation.

#### HIDE_HIDDEN_FIELDS
You can use ```HIDE_HIDDEN_FIELDS``` to hide hidden fields in Request and Response fields.

### List of Settings

|      Setting      | Type    | Options         | Default |
|-------------------|---------|-----------------|---------|
|HIDE_DOCS          | Boolean | `True`, `False` | `False` |
|HIDE_LIVE_ENDPOINTS| Boolean | `True`, `False` | `False` |
|HIDE_HIDDEN_FIELDS | Boolean | `True`, `False` | `False` |
|                   |         |                 |         |
