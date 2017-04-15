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
## Voting Integration render (default) - additonal arugments should be past at the end of the list.
```python
return render(request, template_path, {"title": page_title_name, "breadcrumb": [(breadcrumb_title, breadcrumb_url), ]})
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