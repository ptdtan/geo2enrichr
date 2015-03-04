App.View.InputForm = Backbone.View.extend({

    tagName: 'form',
    
    mode: 'geo',

    mockUsed: false,
    
    initialize: function(options) {
        this.index = options.index;

        var $table = $('<table></table>');
        this.$el.append($table);
        this.collection.each(function(f) {
            var field;
            if (f instanceof App.Model.Input) {
                field = new App.View.Input({ model: f });
            } else if (f instanceof App.Model.Option) {
                field = new App.View.Option({ model: f });
            } else if (f instanceof App.Model.TextArea) {
                field = new App.View.TextArea({ model: f });
            } else if (f instanceof App.Model.File) {
                field = new App.View.File({ model: f });
            }
            $table.append(field.el);
        }, this);

        App.EventAggregator.on('clear:form', this.clear, this);
        App.EventAggregator.on('change:mode', this.change, this);
        App.EventAggregator.on('mock:input', this.mock, this);
        
        this.secure()
        //this.render();
    },

    render: function(url) {
        this.collection.each(function(model) {
            model.set('value', '');
        });
        _.each(url.queryString, function(value, field) {
            var model = this.collection.get(field);
            model.set('value', value.replace(/\+/g, ' '));
        }, this);
        this.secure();
    },
   
    secure: function() {
        var hash = Backbone.history.location.hash.split('?');
        if (hash.length) {
            this.mode = hash[0].slice(1);
        }
        console.log('securing under mode ' + this.mode);
        this.collection.each(function(model) {
            var triFlag = model.get(this.mode);
            if (triFlag === 1) {
                model.set('hide', false);
                model.set('disabled', false);
            } else if (triFlag === -1) {
                model.set('hide', true);
            } else {
                model.set('hide', false);
                model.set('disabled', true);
            }
        }, this);
    },

    change: function(mode) {
        this.mode = mode;
        App.EventAggregator.trigger('clear:form');
        App.EventAggregator.trigger('clear:results');
        this.secure();
        if (this.mockUsed) {
            this.mock();
        }
    }/*,

    clear: function() {
        this.mockUsed = false;
        this.collection.each(function(model) {
            if (model.get('options')) {
                model.set('value', model.get('value'));
            } else {
                model.set('value', '');
            }
        });
    },

    mock: function() {
        this.mockUsed = true;
        this.collection.each(function(model) {
            var prop = model.get(this.mode + 'Mock');
            if (_.isUndefined(prop)) {
                model.set('value', '');
            } else {
                model.set('value', prop);
            }
        }, this);
    }*/
});