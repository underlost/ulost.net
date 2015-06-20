/*!
 * UnderTasker
 * Copyright 2015 Tyler Rilling, some parts loosely based off of Bootstrap
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

module.exports = function (grunt) {
  'use strict';

  // Force use of Unix newlines
  grunt.util.linefeed = '\n';

  RegExp.quote = function (string) {
    return string.replace(/[-\\^$*+?.()|[\]{}]/g, '\\$&');
  };

  // Project configuration.
  grunt.initConfig({

    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*!\n' +
            ' * <%= pkg.name %> v<%= pkg.version %> (Built with UnderTasker)\n' +
            ' */\n',
    jqueryCheck: 'if (typeof jQuery === \'undefined\') { throw new Error(\'UnderTasker\\\'s JavaScript requires jQuery\') }\n\n',

    // Task configuration.
    clean: {
      dist: ['dist']
    },

    coffee: {
      compile: {
        files: {
          // 'ulost/static_precompile/js/result.js': 'ulost/static_precompile/coffee/source.coffee', // 1:1 compile
          'ulost/static/js/app.js': ['ulost/static_precompile/coffee/blip/*.coffee'] // compile and concat into single file
        }
      },
    },

    jshint: {
      options: {
        jshintrc: 'ulost/static_precompile/js/.jshintrc'
      },
      grunt: {
        options: {
          jshintrc: 'grunt/.jshintrc'
        },
        src: ['Gruntfile.js', 'grunt/*.js']
      },
      src: {
        src: 'ulost/static_precompile/js/*.js'
      },
      test: {
        src: 'ulost/static_precompile/js/tests/unit/*.js'
      }
    },

    jscs: {
      options: {
        config: 'ulost/static_precompile/js/.jscsrc'
      },
      grunt: {
        options: {
          requireCamelCaseOrUpperCaseIdentifiers: null,
          requireParenthesesAroundIIFE: true
        },
        src: '<%= jshint.grunt.src %>'
      },
      src: {
        src: '<%= jshint.src.src %>'
      },
      test: {
        src: '<%= jshint.test.src %>'
      },
      assets: {
        src: '<%= jshint.assets.src %>'
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>\n<%= jqueryCheck %>',
        stripBanners: false
      },
      undertask: {
          src: [
            'ulost/static_precompile/js/transition.js',
            'ulost/static_precompile/js/alert.js',
            'ulost/static_precompile/js/button.js',
            'ulost/static_precompile/js/carousel.js',
            'ulost/static_precompile/js/collapse.js',
            'ulost/static_precompile/js/dropdown.js',
            'ulost/static_precompile/js/modal.js',
            'ulost/static_precompile/js/tooltip.js',
            'ulost/static_precompile/js/popover.js',
            'ulost/static_precompile/js/scrollspy.js',
            'ulost/static_precompile/js/tab.js',
            'ulost/static_precompile/js/affix.js',
          ],
        dest: 'dist/js/<%= pkg.slug %>.js'
      }
    },

    uglify: {
      options: {
        report: 'min'
      },
      undertask: {
        options: {
          banner: '<%= banner %>'
        },
        src: '<%= concat.undertask.dest %>',
        dest: 'dist/js/<%= pkg.slug %>.min.js'
      }
    },

    qunit: {
      options: {
        inject: 'ulost/static_precompile/js/tests/unit/phantom.js'
      },
      files: 'ulost/static_precompile/js/tests/index.html'
    },

    less: {
      compileCore: {
        options: {
          strictMath: true,
          sourceMap: true,
          outputSourceFiles: true,
          sourceMapURL: '<%= pkg.slug %>.css.map',
          sourceMapFilename: 'dist/css/<%= pkg.slug %>.css.map'
        },
        files: {
          'dist/css/<%= pkg.slug %>.css': 'ulost/static_precompile/less/<%= pkg.slug %>.less'
        }
      },
      minify: {
        options: {
          cleancss: true,
          report: 'min'
        },
        files: {
          'dist/css/<%= pkg.slug %>.min.css': 'dist/css/<%= pkg.slug %>.css'
        }
      }
    },

    autoprefixer: {
      options: {
        browsers: [
            "Android 2.3",
            "Android >= 4",
            "Chrome >= 20",
            "Firefox >= 24",
            "Explorer >= 8",
            "iOS >= 6",
            "Opera >= 12",
            "Safari >= 6"
        ]
      },
      core: {
        options: {
          map: true
        },
        src: 'dist/css/<%= pkg.slug %>.css'
      }
    },

    csslint: {
      options: {
        csslintrc: 'ulost/static_precompile/less/.csslintrc'
      },
      src: [
        'dist/css/<%= pkg.slug %>.css'
      ]
    },

    cssmin: {
      options: {
        keepSpecialComments: '*',
        advanced: false,
        report: 'min',
        compatibility: 'ie8'
      }
    },

    usebanner: {
      options: {
        position: 'top',
        banner: '<%= banner %>'
      },
      files: {
        src: 'dist/css/*.css'
      }
    },

    csscomb: {
      options: {
        config: 'ulost/static_precompile/less/.csscomb.json'
      },
      dist: {
        expand: true,
        cwd: 'dist/css/',
        src: ['*.css', '!*.min.css'],
        dest: 'dist/css/'
      }
    },

    imagemin: {
      dynamic: {
        files: [{
        expand: true,
        cwd: 'ulost/static_precompile/img/',
        src: ['**/*.{png,jpg,gif}'],
        dest: 'dist/img/'
      }]
      }
    },

    copy: {
      fonts: {
        expand: true,
        cwd: './ulost/static_precompile',
        src: [
          'fonts/*'
        ],
        dest: 'dist'
      },
      dist: {
        expand: true,
        cwd: './dist',
        src: [
          '{css,js}/*.min.*',
          'css/*.map',
          'fonts/*',
          'img/*'
        ],
        dest: 'ulost/static'
      },
    },

    connect: {
      server: {
        options: {
          port: 3000,
          base: '.'
        }
      }
    },

    jekyll: {
      options : {
        bundleExec: true,
        src : 'ulost/static_precompile/site',
      },
      site: {}
    },

    validation: {
      options: {
        charset: 'utf-8',
        doctype: 'HTML5',
        failHard: true,
        reset: true,
        relaxerror: [
          'Bad value X-UA-Compatible for attribute http-equiv on element meta.',
          'Element img is missing required attribute src.'
        ]
      },
      files: {
        src: '_gh_pages/**/*.html'
      }
    },

    watch: {
      src: {
        files: '<%= jshint.src.src %>',
        tasks: ['jshint:src', 'qunit']
      },
      test: {
        files: '<%= jshint.test.src %>',
        tasks: ['jshint:test', 'qunit']
      },
      less: {
        files: 'ulost/static_precompile/less/*.less',
        tasks: 'less'
      }
    },

    git_deploy: {
      github: {
        options: {
          url: 'git@github.com:underlost/ulost.net.git',
          branch: 'gh-pages',
          message: 'Deployed with grunt' // Commit message
        },
        src: '_gh_pages'
      },
    }

  });

  // These plugins provide necessary tasks.
  require('load-grunt-tasks')(grunt, {scope: 'dependencies'});
  require('time-grunt')(grunt);

  // Coffee build task.
  grunt.registerTask('build-coffee', ['coffee']);

  // JS distribution task.
  grunt.registerTask('build-js', ['concat', 'uglify']);

  // IMG distribution task.
  grunt.registerTask('build-img', ['imagemin']);

  // CSS build task.
  grunt.registerTask('less-compile', ['less:compileCore']);
  grunt.registerTask('build-css', ['less-compile', 'autoprefixer', 'usebanner', 'csscomb', 'less:minify', 'cssmin']);

  // HTML build/validation site task
  grunt.registerTask('build-site', ['jekyll', 'validation']);

  // Git Deploy task
  grunt.registerTask('git-deploy', ['git_deploy:github']);

  // Test task.
  grunt.registerTask('test', ['build-css', 'csslint', 'jshint', 'jscs', 'qunit']);

  // Build static assets and HTML
  grunt.registerTask('build', ['clean', 'build-coffee', 'build-css', 'build-js', 'build-img', 'build-site', 'copy:fonts', 'copy:dist']);

  // Only build static assets, not html
  grunt.registerTask('dist', ['clean', 'build-coffee', 'build-css', 'build-js', 'build-img', 'copy:fonts', 'copy:dist']);

  // Full Deploy
  grunt.registerTask('deploy', ['git-deploy']);

};
