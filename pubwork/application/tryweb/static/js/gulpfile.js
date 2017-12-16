const gulp = require('gulp');
const babel = require('gulp-babel');

gulp.task('default', function() {
// browser source
    gulp.src("js/source/**/*.js")
        .pipe(babel())
        .pipe(gulp.dest("js/build"));
});