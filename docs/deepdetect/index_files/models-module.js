(function () {

  var opts = {
    media: 'image',
    type: 'type-all',
    backend: ['caffe', 'tensorflow', 'caffe2'],
    platform: 'desktop',
    disabledLabels: [],
    searchTerm: ""
  };

  var media = $("#models-selector .media > a");
  var type = $("#models-selector .type > a");
  var platform = $("#models-selector .platform > a");
  var backend = $("#models-selector .backend > a");

  media.on("click", clickEvent.bind(this, 'media'));
  type.on("click", clickEvent.bind(this, 'type'));
  platform.on("click", clickEvent.bind(this, 'platform'));
  backend.on("click", function() {
    if(!$(this).hasClass('disabled')) {

      if(
        opts.backend.indexOf(this.id) !== -1 &&
        opts.backend.length > 1
      ) {
        opts.backend.splice(opts.backend.indexOf(this.id), 1);
      } else {
        opts.backend.push(this.id);
      }

      checkOptions();
      disableLabels();
      displayOpts();
      setUrlParams();
      displayModels();

    }
  });

  function getUrlParams() {
    var query = location.search.substr(1);
    var result = {};
    query.split("&").forEach(function(part) {
      var item = part.split("=");
      result[item[0]] = decodeURIComponent(item[1]);
    });

    if(result.opts) {
      var optsParams = JSON.parse(result.opts);

      if(optsParams.media &&
        ['image', 'text', 'other'].includes(optsParams.media)) {
        opts.media = optsParams.media;
      }

      if(optsParams.type &&
        ['type-all', 'detection', 'classification', 'ocr', 'segmentation', 'image-net'].includes(optsParams.type)) {
        opts.type = optsParams.type;
      }

      if(optsParams.backend && Array.isArray(optsParams.backend)) {
        var isValid = true;
        var validBackends = ['caffe', 'caffe2', 'tensorflow', 'ncnn'];
        for(var i = 0; i < optsParams.backend.length; i++) {
          isValid = isValid && validBackends.includes(optsParams.backend[i]);
        }

        if(isValid) {
          opts.backend = optsParams.backend;
        }
      }

      if(optsParams.platform &&
        ['desktop', 'embedded'].includes(optsParams.platform)) {
        opts.platform = optsParams.platform;
      }

      if(optsParams.searchTerm && optsParams.searchTerm.length > 0) {
        opts.searchTerm = optsParams.searchTerm;
        $("#modelFilter").val(opts.searchTerm);
      }
    }
  }


  function setUrlParams() {
    var params = JSON.parse(JSON.stringify(opts));
    delete params.disabledLabels;
    var url = '/models/?opts=' + JSON.stringify(params);
    window.history.pushState({urlPath:'/models'},"",url);
  }

  function clickEvent(optLabel, event) {
    if(!$(event.currentTarget).hasClass('disabled')) {

      opts[optLabel] = event.currentTarget.id;

      if(opts[optLabel] === 'embedded') {
        if(opts.backend.indexOf('tensorflow') !== -1)
          opts.backend.splice(opts.backend.indexOf('tensorflow'), 1);
        if(opts.backend.indexOf('caffe2') !== -1)
          opts.backend.splice(opts.backend.indexOf('caffe2'), 1);
      }

      checkOptions();
      disableLabels();
      displayOpts();
      setUrlParams();
      displayModels();

    }
  }

  function displayModels() {
    var containers = $('.model-container');
    var displayedContainers = [];

    for(var i = 0; i < containers.length; i++) {
      var container = $(containers[i]);

      var includesBackend = false;
      var containerBackends = container.data('backend').split(',');
      for(var j = 0; j < containerBackends.length; j++) {
        var backend = containerBackends[j];
        includesBackend = includesBackend || opts.backend.includes(backend);
      }

      var isDisplayed =
        container.data('media').split(',').includes(opts.media) &&
        (opts.type === 'type-all' || container.data('type').split(',').includes(opts.type)) &&
        container.data('platform').split(',').includes(opts.platform) &&
        (opts.searchTerm.length > 0 ? container.data('name').includes(opts.searchTerm) : true) &&
        includesBackend;

      if(isDisplayed) {
        displayedContainers.push(container);
      }

    }

    containers.hide();
    displayedContainers.forEach(container => $(container).show());

    // Display models results message
    var containersLength = containers.siblings(':visible').length - 1;
    var message = [];
    if(containersLength === 0) {
      message.push("No models can be found using these parameters");
    } else {
      message.push(containersLength  +" results for: All ");
      message.push(opts.media);
      message.push(" models for ");
      message.push(opts.type === "type-all" ? "everything" : opts.type);
      message.push(" on ");
      message.push(opts.platform);

      if(opts.searchTerm.length > 0) {
        message.push(" containing term '");
        message.push(opts.searchTerm);
        message.push("'");
      }
    }
    $("#models-results").html(message.join(""));

  }

  function displayOpts() {

    media.removeClass('selected');
    $('#' + opts.media).addClass('selected');

    type.removeClass('selected');
    $('#' + opts.type).addClass('selected');

    platform.removeClass('selected');
    $('#' + opts.platform).addClass('selected');

    backend.removeClass('selected');
    for(var i = 0; i < opts.backend.length; i++) {
      var label = opts.backend[i];
      $('#' + label).addClass('selected');
    }

    $('.disabled.selected').removeClass('selected');
  }

  function disableLabels() {
    $('.disabled').removeClass('disabled');

    for(var i = 0; i < opts.disabledLabels.length; i++) {
      var label = opts.disabledLabels[i];
      $('#' + label).addClass('disabled');
    }
  }

  function checkOptions() {
    opts.disabledLabels = [];

    if(opts.media === "text") {
      opts.disabledLabels.push('detection');
      opts.disabledLabels.push('classification');
      opts.disabledLabels.push('ocr');
      opts.disabledLabels.push('segmentation');
      opts.disabledLabels.push('image-net');
    }

    if(
      opts.backend.length === 1 &&
      opts.backend.includes('ncnn')
    ) {
      opts.disabledLabels.push('desktop');
    }

    if(opts.platform === 'embedded') {
      opts.disabledLabels.push('tensorflow');
      opts.disabledLabels.push('caffe2');
    }

  }

  $('.install-configuration .btn').on("click", configurationChange);
  function configurationChange(evt) {
    var target = $(evt.currentTarget);
    var parent = target.parents('.install');

    parent.find('.install-configuration .btn').removeClass('btn-jolibrain').addClass('btn-secondary');
    target.addClass('btn-jolibrain').removeClass('btn-secondary');

    parent.find('pre').removeClass('d-block').addClass('d-none');
    parent.find('pre.install_' + target.text()).removeClass('d-none').addClass('d-block');
  }

  $('.usage-selector .btn').on("click", usageChange);
  function usageChange(evt) {
    var target = $(evt.currentTarget);
    var parent = target.parents('.usage');

    parent.find('.usage-selector .btn').removeClass('btn-jolibrain').addClass('btn-secondary');
    target.addClass('btn-jolibrain').removeClass('btn-secondary');

    parent.find('pre').removeClass('d-block').addClass('d-none');
    parent.find('pre.usage_' + target.text().toLowerCase().trim()).removeClass('d-none').addClass('d-block');
  }

  $('.output-selector .btn').on("click", outputChange);
  function outputChange(evt) {
    var target = $(evt.currentTarget);
    var parent = target.parents('.content');

    parent.find('.output-selector .btn').removeClass('btn-jolibrain').addClass('btn-secondary');
    target.addClass('btn-jolibrain').removeClass('btn-secondary');

    parent.find('.selectable-output').removeClass('d-block').addClass('d-none');
    parent.find('.output-' + target.data('selectable')).removeClass('d-none').addClass('d-block');
  }

  var copyInstall = new ClipboardJS('.btn.copy-install', {
    target: function(trigger) {
      return $(trigger).parents('.install').find('pre.d-block code')[0];
    }
  });
  copyInstall.on('success', function(e) {
    $(e.trigger).tooltip('show');
    e.clearSelection();
    setTimeout(function() {
      $('.btn.copy-install[data-toggle="tooltip"]').tooltip('hide');
    }, 800);
  });

  var copyUsage = new ClipboardJS('.btn.copy-usage', {
    target: function(trigger) {
      return $(trigger).parents('.usage').find('pre.d-block code')[0];
    }
  });
  copyUsage.on('success', function(e) {
    $(e.trigger).tooltip('show');
    e.clearSelection();
    setTimeout(function() {
      $('.btn.copy-usage[data-toggle="tooltip"]').tooltip('hide');
    }, 800);
  });

  if($('#models-selector').length > 0) {
    getUrlParams();

    checkOptions();
    disableLabels();
    displayOpts();
    setUrlParams();
    displayModels();
  }

  $(".model-single-wrapper .nav-link, .models-wrapper .nav-link").on("click", function(e) {

    var container = $(e.target).parents(".model-container");

    container.find(".nav-link").removeClass("active");
    $(e.target).addClass('active');

    container.find(".code > div").removeClass("d-block").addClass("d-none");
    container.find(".code > div." + e.target.dataset.target).removeClass("d-none").addClass("d-block");

  });

  $("#modelFilter").on('input', function(e) {
    opts.searchTerm = e.currentTarget.value;

    if(opts.searchTerm.length > 0) {
      $("#searchClean").show();
    } else {
      $("#searchClean").hide();
    }

    setUrlParams();
    displayModels();
  });

  $("#searchClean").click(function(e) {
    opts.searchTerm = "";
    $("#modelFilter").val("");
    $("#searchClean").hide();

    setUrlParams();
    displayModels();
  });

}());
