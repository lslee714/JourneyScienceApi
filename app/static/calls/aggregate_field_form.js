angular.module('calls')
    .directive('aggregateFieldForm', ['CallsApiService', function(CallsApiService){
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/calls/aggregate_field_form.html',
            link: function(scope, elem, attrs){
                scope.aggregateField = {};
                scope.getFieldAggregate = function(){
                    scope.getAggregatePromise = CallsApiService.getFieldAggregate(scope.aggregateField);
                    scope.getAggregatePromise.then(
                        function(response){
                        }, function(error){
                            console.log("Error")
                            scope.handleErrors(error.data);
                        }
                    );
                };
          }
        }

    }])