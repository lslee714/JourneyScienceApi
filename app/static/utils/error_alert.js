angular.module('utils')
    .directive('errorAlert', [function(errorAlert){
        return {
            restrict: 'E',
            replace: true,
            scope: {
                errors: '='
            },
            templateUrl: '/static/utils/error_alert.html'
        }
    }]);