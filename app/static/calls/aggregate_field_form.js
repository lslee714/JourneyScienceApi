angular.module('calls')
    .directive('aggregateFieldForm', ['CallsApiService', function(CallsApiService){
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/calls/aggregate_field_form.html',
            link: function(scope, elem, attrs){
                scope.getFieldAggregate = function(){
//                    CallsApiService.getFieldAggregate().then(function(){
//                    });
                    console.log("HI")
                };
          }
        }

    }])