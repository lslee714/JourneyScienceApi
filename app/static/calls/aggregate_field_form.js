angular.module('calls')
    .directive('aggregateFieldForm', ['CallsApiService', function(CallsApiService){
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/calls/aggregate_field_form.html',
            link: function(scope, elem, attrs){
                scope.aggregateData = {};
                scope.getFieldAggregate = function(){
                    scope.getAggregatePromise = CallsApiService.getFieldAggregate(scope.aggregateData);
                    scope.getAggregatePromise.then(
                        function(response){
                        }, function(error){
                            scope.handleErrors(error.data);
                        }
                    );
                };
          }
        }

    }])