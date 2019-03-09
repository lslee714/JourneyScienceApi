angular.module('utils')
    .directive('loadingButton', ['$parse', function($parse){
        return {
            restrict: 'A',
            replace: true,
            link: function(scope, elem, attrs){
                var parser = $parse(attrs.loadingButton);
                scope.$watch(function() {return parser(scope);}, function() {
                    var promise = parser(scope);
                    if (promise) {
                        var loadingDom = $("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
                        elem.append(loadingDom)
                        promise.finally(function() {
                            loadingDom.remove();
                        });
                    }
                });
            }
        }
    }]);