var fs = require('fs');

exports.__templatePath      = "";
exports.__templateData      = [];
exports.__templates         = [];
exports.__templatesUnbuild  = [];
exports.__templatesBuilt    = 0;
exports.__templatesCompiled = [];

exports.path = function (path) {
    exports.__templatePath = process.cwd() + '/' + path;
}

exports.getTemplate = function (template) {
    templateContent = fs.readFileSync(exports.__templatePath + '/templates/' + template + '.tp', 'utf-8');

    Array.prototype.shift.apply(arguments);

    var templateData = [];

    if (exports.__templateData.hasOwnProperty(template)) {

        for (var member in exports.__templateData[template]) {

            templateData[member] = exports.__templateData[template][member];
        }
    }

    buildArguments(templateData, '', arguments);

    exports.__templatesUnbuild[template] = templateContent;

    jQuery.each(Object.keys(templateData), function (i, e) {

        templateContent = templateContent.replace('{{ ' + e + ' }}', templateData[e]);
    });

    function buildArguments (templateData, start) {

        jQuery.each(arguments[2], function (i, e) {

            var key = ((start !== '') ? start + '.' + i : (isNaN(i) ? i : '') );

            if (typeof e === 'object') {

                start = buildArguments(templateData, key, e);
            } else {

                templateData[((start !== '') ? start + '.' + i : i)] = e;
            }
        });
    }

    function buildDependencies (templateContent) {
        templateContent = "<tpl>"+templateContent+"</tpl>";
        var deps = [];

        jQuery(templateContent).find('tpl').each(function (i, e) {
            deps.push(jQuery(this).attr('name'));
        });

        return deps;
    }

    exports.__templates[template] = { 
        content : templateContent,
        dependencies : buildDependencies(templateContent)
    };

    exports.__templatesBuilt++;

    if (exports.__templatesTotal == exports.__templatesBuilt) {
        exports.__templatesCompile();
    } 
}

exports.data = function (template, data) {
    var templateData = [];

    setData();

    function setData () {
        buildArguments(templateData, '', data);

        if (exports.__templateData.hasOwnProperty(template)) {
            for (var member in templateData) {
                exports.__templateData[template][member] = templateData[member];
            }
        } else {
            exports.__templateData[template] = templateData;
        }

        function buildArguments (templateData, start) {

            jQuery.each(arguments[2], function (i, e) {

                var key = ((start !== '') ? start + '.' + i : (isNaN(i) ? i : '') );

                if (typeof e === 'object') {

                    start = buildArguments(templateData, key, e);
                } else {

                    templateData[((start !== '') ? start + '.' + i : i)] = e;
                }
            });
        }
    }
}

exports.block = function (block) {
    return {
        block : block, 
        set : function (blockTeplate) {
            that = this;
            var blockContent = fs.readFileSync(exports.__templatePath + '/blocks/' + blockTeplate + '.bp', 'utf8');

            var blockContent = jQuery.parseHTML('<blk>'+blockContent+'</blk>');

            jQuery(blockContent).find('tpl').each(function (i, e) {
                jQuery(e).html(exports.__templates[jQuery(e).attr('name')].content);
            });

            jQuery('block[name='+that.block+']').html(jQuery(blockContent).html());
        }
    };
}

exports.build = function (template) {
    buildTemplate();

    function buildTemplate() {
        if(typeof template === 'undefined') {
            exports.__templatesBuilt = 0;
            filenames = fs.readdirSync(exports.__templatePath + '/templates');
            exports.__templatesTotal = filenames.length;

            filenames.forEach(function (filename) {
                file = filename.split('.'); file.splice(-1, 1); file = file.join('.');
                exports.getTemplate(file);
            });
        } else {
            exports.__templatesBuilt--;
            exports.getTemplate(template);
        }
    }

    return {
        template : template,
        reset : function () {
            template = this.template;

            jQuery('tpl[name='+template+']').html(exports.__templates[template].content);
        }
    }
}

exports.__templatesCompile = function () {
    for (var template in exports.__templates) {
        compileTemplate(template, exports.__templates[template]);
    }

    function compileTemplate (name, template) {
        if (exports.__templatesCompiled.indexOf(name) < 0) {
            if (typeof template.dependencies !== "undefined" && template.dependencies.length > 0) {
                for (var dep in template.dependencies) {
                    if (typeof exports.__templatesCompiled[template.dependencies[dep]] === 'undefined') {
                        compileTemplate(template.dependencies[dep], exports.__templates[template.dependencies[dep]]);
                    }
                }
            }

            templateContent = jQuery.parseHTML('<tpl>'+template.content+'</tpl>');

            jQuery(templateContent).find('tpl').each(function (i, e) {
                jQuery(e).html(exports.__templates[jQuery(e).attr('name')].content);
            });

            exports.__templates[name].content = jQuery(templateContent).html();

            exports.__templatesCompiled.push(name);
        }
    }
}