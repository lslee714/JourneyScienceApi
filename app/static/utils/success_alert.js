angular.module('utils')
    .directive('successAlert', [function(errorAlert){
        return {
            restrict: 'E',
            replace: true,
            scope: {
                messages: '='
            },
            templateUrl: '/static/utils/success_alert.html'
        }
    }]);