# electron-simple-templates
Simple templating system for electron.

## Instalation

```sh
$ npm install electron-simple-templates --save
```

## How to use

Initialize the module then set the path to the views folder:

```javascript
var template = require('electron-simple-templates');
template.path('app/views');
```

Views folder should have a `blocks` folder and a `templates` folder like in the picture:

![Folder structure](https://raw.githubusercontent.com/romeobalta/electron-simple-templates/master/folder-structure.png)

As you can see in the folder structure too, we have two types of elements:

### 1. Templates

Templates elements look like this in the html:

```html
<tpl name="template"></tpl>
<tpl name="template2"></tpl>
```

When you run

```javascript
template.build();
```
The content in `template.tp` will be compiled and set in `<tpl name="template"></tpl>` and `template2.tp` compiled then set in `<tpl name="template2"></tpl>`

Variables look like this:
```html
<!-- template.tp -->
<p>This is a {{ element.name }}</p>
```

And their data can be set by:
```javascript
template.data('template', { element : { name : 'paragraph' } } );
```
The first parameter is the template name, the second data in `JSON` format.
Data is compiled when the `build()` command is run. You can set data then call `build()` again to recompile.
You can also compile only one template using

```javascript
template.build('template');
```

### 2. Blocks

Blocks elements look like this in the html:

```html
<block name="container"></block>
```

These are not automatically compile.
If you want the set the content of a block, you do it like this:

```javascript
template.block('container').set('login');
```

This will take the content in `login.bp` and set it in `<block name="container"></block>`