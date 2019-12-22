'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
const del = require('del');
var imageDataURI = require('gulp-image-data-uri');

 
sass.compiler = require('node-sass');

//makes ./css/main.css out of the scss file(s) in ./{{ template_name }}-bootstrap-theme
gulp.task('sass', function () {
  return gulp.src('./scss/main.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest('./css'));
});

//use this if changing css 
//watches the scss file(s) in ./scss and updates ./css/main.css 
gulp.task('sass:watch', function () {
  sass.compiler.watch('./scss/main.scss', gulp.series('sass'));
});

gulp.task('clean', () => {
    return del([
        './css/main.css',
    ]);
});

gulp.task('watch', () => {
    gulp.series(['sass']);
    gulp.watch('./scss/**/*.scss', (done) => {
        gulp.series(['clean', 'sass'])(done);
    });

});


//copies the bootstrap default scss for a first time use or in case you update the bootstrap version
//for use before compiling the scss into main.css (aka gulp process 'sass')
gulp.task('copyscss', function () {
  return gulp.src(['./node_modules/bootstrap/scss/**/*'])
    .pipe(gulp.dest('./scss/bootstrap-scss/.'));
});

//copies the bootstrap default js for a first time use or in case you update the bootstrap version
gulp.task('copyjs', function () {
  return gulp.src(['./node_modules/bootstrap/dist/js/**/*.js'])
    .pipe(gulp.dest('./js/bootstrap/'));
});

gulp.task('setup', gulp.series('copyscss', 'copyjs', 'sass'));

gulp.task('prepare-data-uri', function() {
    return gulp.src('./img/*.png')
        .pipe(imageDataURI()) 
        .pipe(gulp.dest('./dist'));
});
