angular.module('calls')
    .directive('uploadTr', [function(){
        return {
            restrict: 'A',
            replace: true,
            templateUrl: '/static/calls/upload_tr.html'
        }
    }]);