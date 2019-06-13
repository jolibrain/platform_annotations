(function () {

  var opts = {
    os: 'ubuntu',
    source: 'docker',
    compute: 'gpu',
    gpu: 'gtx',
    backend: ['caffe', 'tsne', 'xgboost'],
    disabledLabels: []
  };

  opts.deepdetect = $("#deepdetect").val();

  var os =          $("#quickstart-selector .os a.btn");
  var source =      $("#quickstart-selector .source a.btn");
  var compute =     $("#quickstart-selector .compute a.btn");
  var gpu =         $("#quickstart-selector .gpu a.btn");
  var backend =     $("#quickstart-selector .backend a.btn");

  os.on("click", clickEvent.bind(this, 'os'));
  source.on("click", clickEvent.bind(this, 'source'));
  compute.on("click", clickEvent.bind(this, 'compute'));
  gpu.on("click", clickEvent.bind(this, 'gpu'));
  backend.on("click", function() {

    if(!$(this).hasClass('disabled')) {

      if(opts.backend.indexOf(this.id) !== -1) {
        opts.backend.splice(opts.backend.indexOf(this.id), 1);
      } else {
        opts.backend.push(this.id);
      }

      checkOptions();
      disableLabels();
      displayOpts();
      setUrlParams();

      hideSelectorSections();
      displayDockerPull();
      displayCmake();

    }

  });

  function clickEvent(optLabel, event) {
    if(!$(event.currentTarget).hasClass('disabled')) {

      opts[optLabel] = event.currentTarget.id;

      checkOptions();
      disableLabels();
      displayOpts();
      setUrlParams();
      displayDiv();

      hideSelectorSections();

    }
  }

  function displayOpts() {

    os.removeClass('selected');
    $('#' + opts.os).addClass('selected');

    source.removeClass('selected');
    $('#' + opts.source).addClass('selected');

    compute.removeClass('selected');
    $('#' + opts.compute).addClass('selected');

    gpu.removeClass('selected');
    $('#' + opts.gpu).addClass('selected');

    backend.removeClass('selected');
    for(var i = 0; i < opts.backend.length; i++) {
      var label = opts.backend[i];
      $('#' + label).addClass('selected');
    }

    $('.disabled.selected').removeClass('selected');
    //$(".option i").removeClass('fa-circle fa-check-circle');
    //$(".option.selected i").addClass('fa-check-circle');
    //$(".option:not(.selected) i").addClass('fa-circle');
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

    if(opts.deepdetect === 'platform') {
      opts.disabledLabels.push('ubuntu');
      opts.disabledLabels.push('other_linux');
      opts.disabledLabels.push('macos');
      opts.disabledLabels.push('windows');

      opts.disabledLabels.push('build_source');

      opts.disabledLabels.push('raspberry');

      opts.disabledLabels.push('p100');
      opts.disabledLabels.push('volta');
      opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');

      opts.disabledLabels.push('caffe2');
    }

    if(
      opts.deepdetect === 'server' &&
      opts.source === 'build_source' &&
      opts.compute === 'raspberry'
    ) {
      opts.backend.push('ncnn');
      opts.disabledLabels.push('tensorflow');
      opts.disabledLabels.push('tsne');
      opts.disabledLabels.push('xgboost');
    }

    if(opts.os !== 'ubuntu') {
      opts.source = 'docker';
      opts.disabledLabels.push('aws');
      opts.disabledLabels.push('build_source');
      opts.disabledLabels.push('raspberry');
      /*opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');*/
      opts.disabledLabels.push('gpu_aws');
    }

    if(
      opts.deepdetect === 'server' &&
      opts.os === 'windows'
    ) {
      opts.compute = 'cpu';
      opts.disabledLabels.push('gpu');

      opts.disabledLabels.push('gtx');
      opts.disabledLabels.push('p100');
      opts.disabledLabels.push('volta');
      opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');
      opts.disabledLabels.push('gpu_aws');
    }

    if(opts.source === 'docker') {

      // only ncnn build available for Docker on Raspberry Pi - #61
      if(opts.compute === 'raspberry') {
        opts.backend.push('ncnn');
        opts.disabledLabels.push('caffe');
        opts.disabledLabels.push('caffe2');
        opts.disabledLabels.push('tensorflow');
        opts.disabledLabels.push('tsne');
        opts.disabledLabels.push('xgboost');
      }

      opts.disabledLabels.push('gpu_aws');

      if(!opts.backend.includes('xgboost'))
          opts.backend.push('xgboost');

      if(!opts.backend.includes('tsne'))
          opts.backend.push('tsne');

      /*if(opts.compute === 'gpu') {
        opts.disabledLabels.push('tx1');
        opts.disabledLabels.push('tx2');
      }*/

      if (opts.gpu == 'p100') {
          opts.disabledLabels.push('caffe2');
          opts.disabledLabels.push('tensorflow');
      }

      if (opts.gpu == 'volta') {
          opts.disabledLabels.push('caffe2');
          opts.disabledLabels.push('tensorflow');
      }
    }

    if(opts.source === 'aws') {
      opts.disabledLabels.push('ncnn');
      opts.disabledLabels.push('tsne');

      opts.disabledLabels.push('gtx');
      opts.disabledLabels.push('p100');
      opts.disabledLabels.push('volta');
      opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');

      if(!opts.backend.includes('tensorflow'))
        opts.backend.push('tensorflow');

      if(!opts.backend.includes('xgboost'))
        opts.backend.push('xgboost');

      if(opts.compute === 'gpu') {
        opts.gpu = 'gpu_aws';
      }
    }

    if(opts.source === 'build_source') {
      opts.disabledLabels.push('gpu_aws');
    }

    if(opts.compute === 'cpu') {
      opts.disabledLabels.push('gtx');
      opts.disabledLabels.push('p100');
      opts.disabledLabels.push('volta');
      opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');
      opts.disabledLabels.push('gpu_aws');

      if(opts.source !== 'build_source') {
        opts.disabledLabels.push('caffe2');
      }
    }

    if(opts.compute === 'raspberry') {
      opts.disabledLabels.push('gtx');
      opts.disabledLabels.push('p100');
      opts.disabledLabels.push('volta');
      opts.disabledLabels.push('tx1');
      opts.disabledLabels.push('tx2');
      opts.disabledLabels.push('gpu_aws');
    }

    if(opts.backend.includes('tensorflow'))
      opts.disabledLabels.push('caffe2');

    if(opts.backend.includes('caffe2'))
      opts.disabledLabels.push('tensorflow');

    if(opts.source === 'aws' || opts.os !== 'ubuntu') {
      opts.disabledLabels.push('raspberry');
    }
  }

  function hideSelectorSections() {
    $("pre").show();
    $(".section_selector").nextUntil(".section_selector_end").hide();

    $(".section_selector#os_" + opts.os).nextUntil("#os_" + opts.os + "_end").show();
    $(".section_selector#source_" + opts.source).nextUntil("#source_" + opts.source + "_end").show();
    $(".section_selector#compute_" + opts.compute).nextUntil("#compute_" + opts.compute + "_end").show();
    $(".section_selector#gpu_" + opts.gpu).nextUntil("#gpu_" + opts.gpu + "_end").show();

    for(var i = 0; i < opts.backend.length; i++) {
      var label = opts.backend[i];
      $(".section_selector#backend_" + label).nextUntil("#backend_" + label + "_end").show();
    }
  }

  function displayDiv() {
    $('.quickstart-section').hide();

    if(opts.deepdetect === 'platform') {
      $('#from_dd_platform_' + opts.source).show();
    } else {
      $('#from_' + opts.source).show();
      displayDockerPull();
      displayCmake();
    }

    gtag('send', 'event', 'Quickstart Selector', 'click', JSON.stringify(opts));
  }

  function displayCmake() {
    var cmake_command = ['mkdir build\ncd build\ncmake .. -DUSE_SIMSEARCH=ON'];

    switch(opts.compute) {
      case 'cpu':
        cmake_command.push('-DUSE_CPU_ONLY=ON');
        break;
      case 'gpu':
        cmake_command.push("-DUSE_CUDNN=ON");

        switch(opts.gpu) {
          case 'gtx':
            break;
	  case 'p100':
            cmake_command.push('-DCUDA_ARCH="-gencode arch=compute_60,code=sm_60"');
	    break;
          case 'volta':
            cmake_command.push('-DCUDA_ARCH="-gencode arch=compute_70,code=sm_70"');
            break;
          case 'tx1':
            cmake_command.push('-DJETSON=ON -DCUDA_ARCH="-gencode arch=compute_53,code=sm_53" -DCUDA_USE_STATIC_CUDA_RUNTIME=OFF');
      break;
        case 'tx2':
      cmake_command.push('-DJETSON=ON -DCUDA_ARCH="-gencode arch=compute_62,code=sm_62" -DCUDA_USE_STATIC_CUDA_RUNTIME=OFF');
            break;
          default:
            break;
        }

        break;
    case 'raspberry':
        cmake_command.push('-DRPI3=ON -DUSE_HDF5=OFF')
        break;
      default:
        break;
    }

    for(var i = 0; i < opts.backend.length; i++) {
      var label = opts.backend[i];

      switch(label) {
        case 'caffe2':
          cmake_command.push('-DUSE_CAFFE2=ON');
          break;
        case 'ncnn':
          cmake_command.push('-DUSE_NCNN=ON');
          break;
        case 'xgboost':
          cmake_command.push('-DUSE_XGBOOST=ON');
          break;
        case 'tsne':
          cmake_command.push('-DUSE_TSNE=ON');
          break;
      case 'caffe':
	  break;
      case 'tensorflow':
	  cmake_command.push('-DUSE_TF=ON -DCUDA_USE_STATIC_CUDA_RUNTIME=OFF')
      default:
          break;
      }
    }

    // Possible to disable Caffe - issue #61
    if(!opts.backend.includes('caffe')) {
      cmake_command.push('-DUSE_CAFFE=OFF');
    }

    cmake_command.push('\nmake');

    $('#cmake').html(cmake_command.join(' '));
    Prism.highlightElement($('#cmake')[0]);
  }

  function displayDockerPull() {
    var docker_command = ['docker pull jolibrain/deepdetect'];
    var docker_run = ['docker run -d -p 8080:8080 jolibrain/deepdetect'];

    switch(opts.compute) {
      case 'cpu':
        docker_command.push('_cpu');
        docker_run.push('_cpu');
        break;
      case 'gpu':

        switch(opts.gpu) {
        case 'gtx':
      docker_command = ['docker pull jolibrain/deepdetect_gpu'];
      docker_run = ['nvidia-docker run -d -p 8080:8080 jolibrain/deepdetect_gpu'];
            break;
	case 'p100':
      docker_command = ['docker pull jolibrain/deepdetect_gpu_p100'];
      docker_run = ['nvidia-docker run -d -p 8080:8080 jolibrain/deepdetect_gpu_p100'];
            break;
        case 'volta':
      docker_command = ['docker pull jolibrain/deepdetect_gpu_volta'];
      docker_run = ['nvidia-docker run -d -p 8080:8080 jolibrain/deepdetect_gpu_volta'];
            break;
        case 'tx1':
	    docker_command = ['docker pull jolibrain/deepdetect_gpu'];
	    docker_run = ['nvidia-docker run -d -p 8080:8080 jolibrain/deepdetect_gpu'];
            break;
        case 'tx2':
	    docker_command = ['docker pull jolibrain/deepdetect_gpu'];
	    docker_run = ['nvidia-docker run -d -p 8080:8080 jolibrain/deepdetect_gpu'];
            break;
          default:
            docker_command.push('_gpu');
            break;
        }

        break;
    case 'raspberry':
        docker_command.push('_ncnn_pi3');
        docker_run.push('_ncnn_pi3');
        break;
      default:
        break;
    }

    for(var i = 0; i < opts.backend.length; i++) {
      var label = opts.backend[i];

      switch(label) {
        case 'caffe2':
          docker_command.push('_caffe2');
          break;
        case 'ncnn':
          break;
        case 'xgboost':
          break;
        case 'tsne':
          break;
      case 'caffe':
    break;
      case 'tensorflow':
	  docker_command.push('_tf')
	  docker_run.push('_tf')
    break;
        default:
          break;
      }
    }

      $('#docker_pull').html(docker_command.join(''));
      $('#docker_runc').html(docker_run.join(''));

    Prism.highlightElement($('#docker_pull')[0]);
    Prism.highlightElement($('#docker_runc')[0]);
  }

  function getUrlParams() {
    var query = location.search.substr(1);
    console.log(location)
    var result = {};
    query.split("&").forEach(function(part) {
      var item = part.split("=");
      result[item[0]] = decodeURIComponent(item[1]);
    });

    if(result.opts) {

      const deepdetectVersion = location.pathname === '/quickstart-server/' ?
        "server" : "platform";

      if(result.opts === "aws_cpu") {

        opts = {
          os: "ubuntu",
          source: "aws",
          compute: "cpu",
          gpu: "gpu_aws",
          backend: [
            "tsne",
            "tensorflow",
            "xgboost",
            "caffe"
          ],
          deepdetect: deepdetectVersion
        };

      } else if (result.opts === "aws_gpu") {

        opts = {
          os: "ubuntu",
          source: "aws",
          compute: "gpu",
          gpu: "gpu_aws",
          backend: [
            "tsne",
            "tensorflow",
            "xgboost",
            "caffe"
          ],
          deepdetect: deepdetectVersion
        };

      } else {

        var optsParams = JSON.parse(result.opts);

        if(optsParams.deepdetect &&
          ['platform', 'server'].includes(optsParams.deepdetect)) {
          opts.deepdetect = optsParams.deepdetect;
        }

        if(optsParams.os &&
          ['ubuntu', 'other_linux', 'macos', 'windows'].includes(optsParams.os)) {
          opts.os = optsParams.os;
        }

        if(optsParams.source &&
          ['docker', 'aws', 'build_source'].includes(optsParams.source)) {
          opts.source = optsParams.source;
        }

        if(optsParams.compute &&
          ['gpu', 'cpu', 'raspberry'].includes(optsParams.compute)) {
          opts.compute = optsParams.compute;
        }

        if(optsParams.gpu &&
          ['gtx', 'p100', 'volta', 'tx1', 'tx2', 'gpu_aws'].includes(optsParams.gpu)) {
          opts.gpu = optsParams.gpu;
        }

        if(optsParams.backend && Array.isArray(optsParams.backend)) {
          var isValid = true;
          var validBackends = ['caffe', 'caffe2', 'tensorflow', 'ncnn', 'tsne', 'xgboost'];
          for(var i = 0; i < optsParams.backend.length; i++) {
            isValid = isValid && validBackends.includes(optsParams.backend[i]);
          }

          if(isValid) {
            opts.backend = optsParams.backend;
          }
        }
      }
    }
  }

  function setUrlParams() {
    var params = JSON.parse(JSON.stringify(opts));
    delete params.disabledLabels;
    var url = '/quickstart-' + opts.deepdetect + '/?opts=' + JSON.stringify(params);
    window.history.pushState({urlPath:'/quickstart-' + opts.deepdetect},"",url);
  }

  if($('#quickstart-selector').length > 0) {
    getUrlParams();

    checkOptions();
    disableLabels();
    displayOpts();
    setUrlParams();
    displayDiv();

    hideSelectorSections();
    displayCmake();
    displayDockerPull();
  }

}());
