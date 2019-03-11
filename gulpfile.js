
var gulp = require('gulp');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var minify = require('gulp-minify');
 
gulp.task('concat', function(done) {
  return gulp.src([
            'app/static/utils/**/*.js',
            'app/static/calls/**/*.js'
        ])
    .pipe(sourcemaps.init())
    .pipe(concat('dist.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('app/static/dist'));
    done()
});


gulp.task('minify', function(done) {
  gulp.src(['app/static/dist/dist.js'])
    .pipe(minify())
    .pipe(gulp.dest('app/static/dist'))
     done()
});

gulp.task('default', gulp.series('concat', 'minify'))