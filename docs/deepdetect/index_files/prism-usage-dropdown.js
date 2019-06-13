(function(){
  if (typeof self === 'undefined' || !self.Prism || !self.document) {
    return;
  }

  if (!Prism.plugins.toolbar) {
    console.warn('Usage Dropdown plugin loaded before Toolbar plugin.');

    return;
  }

  var callbacks = [];

  Prism.hooks.add('complete', function(env) {

    if(!env.element.className.includes('usage-dropdown'))
      return false;

    $(env.element).parents('.usage').find('pre').removeClass('d-block').removeClass('d-none');
    $(env.element).parents('.usage').find('.code-toolbar').removeClass('d-block').addClass('d-none');
    $(env.element).parents('.usage').find('pre.usage_curl').parents('.code-toolbar').removeClass('d-none').addClass('d-block');
  });

  Prism.plugins.toolbar.registerButton('usage-dropdown', function (env) {

    var className = env.element.className;
    var mainLang = env.element.dataset.lang;

    if(!env.element.className.includes('usage-dropdown'))
      return false;

    var dropdown = document.createElement('div');
    dropdown.setAttribute('class', 'toolbar-dropdown');
    dropdown.innerHTML = '<button class="btn btn-outline-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' + mainLang + '</button><div class="dropdown-menu"><a class="dropdown-item" data-target="curl">Curl</a><a class="dropdown-item" data-target="python">Python</a><a class="dropdown-item" data-target="javascript">Javascript</a></div>';
    var items = dropdown.getElementsByClassName('dropdown-item');
    for(i = 0; i < items.length; i++) {
      items[i].addEventListener('click', function() {
        var target = this.dataset.target;
        $(this).parents('.usage').find('pre').removeClass('d-block').removeClass('d-none');
        $(this).parents('.usage').find('.code-toolbar').removeClass('d-block').addClass('d-none');
        $(this).parents('.usage').find('pre.usage_' + target).parents('.code-toolbar').removeClass('d-none').addClass('d-block');
      });
    }
    return dropdown;
  });

})();

