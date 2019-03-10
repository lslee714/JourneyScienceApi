angular.module('utils')
    .directive('tdCheckbox', function(){
        return {
            restrict: 'A',
            replace: true,
            transclude: true,
            scope: {
                ngModel: '=',
            },
            templateUrl: '/static/utils/td_checkbox.html',
            link: function(scope, elem, attrs){
                scope.setCheckbox = function(){
                    scope.ngModel = !scope.ngModel;
                };
            }
        };
    })