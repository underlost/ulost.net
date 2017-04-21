/*!
 * Based on UnderTasker
 * Copyright 2017 Tyler Rilling
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

// grab our packages
var gulp   = require('gulp'),
    child = require('child_process');
    jshint = require('gulp-jshint');
    sass = require('gulp-sass');
    sourcemaps = require('gulp-sourcemaps');
    concat = require('gulp-concat');
    autoprefixer = require('gulp-autoprefixer');
    cleanCSS = require('gulp-clean-css');
    rename = require('gulp-rename'); // to rename any file
    uglify = require('gulp-uglify');
    del = require('del');
    stylish = require('jshint-stylish');
    runSequence = require('run-sequence');
    coffee = require('gulp-coffee');
    gutil = require('gulp-util');
    bower = require('gulp-bower');
    imagemin = require('gulp-imagemin');
    git = require('gulp-deploy-git');
    browserSync = require('browser-sync');
    $ = require('gulp-load-plugins')();

// Cleans the web dist folder
gulp.task('clean', function () {
    return del([
        'dist/',
        'app/static/',
        'app/**/*.pyc'
    ]);
});

// Clear cache
gulp.task('clean-cache', function () {
    del(['app/**/*.pyc']);
});

gulp.task('copy-dist', function() {
    gulp.src('dist/**/*.*')
    .pipe(gulp.dest('app/static'));
});

// Copy fonts task
gulp.task('copy-fonts', function() {
    gulp.src('app/static_precompile/fonts/site/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/fonts'));
    gulp.src('bower_components/components-font-awesome/fonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/fonts'));
});

// Minify Images
gulp.task('imagemin', function() {
    return gulp.src('app/static_precompile/img/**/*.{jpg,png,gif,ico,json}')
	.pipe(imagemin())
	.pipe(gulp.dest('dist/img'))
});

// Copy Bower components
gulp.task('copy-bower', function() {
    gulp.src('bower_components/components-font-awesome/scss/**/*.*')
    .pipe(gulp.dest('app/static_precompile/sass/font-awesome'));

    gulp.src('bower_components/bootstrap-sass/assets/stylesheets/**/*.*')
    .pipe(gulp.dest('app/static_precompile/sass/bootstrap'));
});

// Runs Bower update
gulp.task('bower-update', function() {
    return bower({ cmd: 'update'});
});

// Bower tasks
gulp.task('bower', function(callback) {
    runSequence(
        'bower-update', 'copy-bower', callback
    );
});

// Compile coffeescript to JS
gulp.task('brew-coffee', function() {
    return gulp.src('app/static_precompile/coffee/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('app/static_precompile/js/coffee/'))
});

// CSS Build Task for main site/theme
gulp.task('build-css', function() {
  return gulp.src('app/static_precompile/sass/site.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
        browsers: ['last 2 versions'],
        cascade: false
    }))
    .pipe(gulp.dest('dist/css'))
    .pipe(cleanCSS())
    .pipe(rename('site.min.css'))
    .pipe(gulp.dest('dist/css'))
    .on('error', sass.logError)
});

// Concat All JS into unminified single file
gulp.task('concat-js', function() {
    return gulp.src([
        'bower_components/jquery/dist/jquery.js',
        'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
        'bower_components/fullpage.js/dist/jquery.fullpage.js',
        'bower_components/jquery.scrollbar/jquery.scrollbar.js',
        'bower_components/PACE/pace.js',
        'app/static_precompile/js/site.js',
        //'app/static_precompile/js/coffee/*.*',
    ])
    .pipe(sourcemaps.init())
        .pipe(concat('global.js'))
        .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest('dist/js'));
});

// configure the jshint task
gulp.task('jshint', function() {
    return gulp.src('app/static_precompile/js/site/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'));
});

// Shrinks all the site js
gulp.task('shrink-js', function() {
    return gulp.src('dist/js/global.js')
    .pipe(uglify())
    .pipe(rename('global.min.js'))
    .pipe(gulp.dest('dist/js'))
});

// Javascript build task for frontend
gulp.task('build-js', function(callback) {
    runSequence('concat-js', 'shrink-js', callback);
});

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
    gulp.watch('app/static_precompile/coffee/**/*.js', ['brew-coffee', 'copy-dist']);
    gulp.watch('app/static_precompile/js/**/*.js', ['build-js', 'copy-dist']);
    gulp.watch('app/static_precompile/sass/**/*.scss', ['build-css', 'copy-dist' ] );
});

// Default build task
gulp.task('build', function(callback) {
    runSequence(
        ['build-css', 'build-js'], 'copy-fonts', 'copy-dist', callback
    );
});

// Default build task
gulp.task('build-copy-img', function(callback) {
    runSequence(
        ['build-css', 'build-js'],
        'imagemin', 'copy-fonts', 'copy-dist', callback
    );
});

// Default task will build the assets then watch for any updates to files.
gulp.task('default', ['build', 'watch']);
