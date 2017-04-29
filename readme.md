# Description
> An online secure election voting system. 
>
# Team Members
+ Adam Monagham
+ Christopher Atwood
+ Craig Winfield
+ Daniel Harborne
+ Giwrgos Kiliafas
+ Ioana Bob
+ Jordan Paskin
+ Matt Elcock
+ Sam Mantle
>
# Usage

python manage.py runsslserver --certificate server.crt --key server.key 

## Voting Integration render (default) - additonal arugments should be past at the end of the list.
```python
return render(request, template_path, {"title": page_title_name, "breadcrumb": [(breadcrumb_title, reverse(url_name)), ]})
``` 

## admin Integration render (default) - additonal arugments should be past at the end of the list.
```python
return render(request, template_path, {"title": page_title_name,'first_name': request.session.forename, "breadcrumb": [(breadcrumb_title, breadcrumb_url) ]})
```

## Displaying messages to admin or voters
### Success
```python
messages.success(request, message)
### Warning
```python
messages.warning(request, message)
### Info
```python
messages.info(request, message)
### Error
```python
messages.error(request, message)
```

## Templates
### New template
``` python
{% extends 'voter_interface/base.html' %}

{% block content %}
    # Template Content Goes Here
{% endblock %}
{% block js %}
    # Javascript files and inline javascript should be placed here
{% endblock %}
```
``` python
{% extends 'admin_interface/base.html' %}

{% block content %}
    # Template Content Goes Here
{% endblock %}
{% block js %}
    # Javascript files and inline javascript should be placed here
{% endblock %}
```
### Extend
> Extend the base.html in the chosen directory
```python
{% extends 'voter_interface/base.html' %}
```
```python
{% extends 'admin_interface/base.html' %}
```
### Container
> The main container (.container) is defined within base.html, therefore does not require to be repeated unless needed.

### Content
> All content of a template should be contained with the content block

```python
{% block content %}
    # Template Content Goes Here
{% endblock %}
```
