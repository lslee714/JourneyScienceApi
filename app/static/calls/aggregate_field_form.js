angular.module('calls')
    .directive('aggregateFieldForm', ['CallsApiService', '$interval', function(CallsApiService, $interval){
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/calls/aggregate_field_form.html',
            link: function(scope, elem, attrs){
                scope.aggregateData = {};
                scope.setUploadsToAggregate = function(){
                    scope.aggregateData.uploads = scope.uploadsToAggregate;
                };

                var startPolling = function(url){
                    var pollPromise = $interval(function(){
                        CallsApiService.getTaskStatus(url).then(
                            function(response){
                                console.log(response)
                                if(response.data && response.data.state=='SUCCESS'){
                                    scope.handleResponse(response.data);
                                    $interval.cancel(pollPromise);
                                }
                            }).catch(function(error){
                                if(error.data){
                                    scope.handleErrors(error.data);
                                    $interval.cancel(pollPromise);
                                }
                            });
                        }, 5000);
                };

                scope.getFieldAggregate = function(){
                    scope.setUploadsToAggregate();
                    scope.getAggregatePromise = CallsApiService.getFieldAggregate(scope.aggregateData);
                    scope.getAggregatePromise.then(
                        function(response){
                            startPolling(response.data.statusUrl);
                        }).catch(function(error){
                            scope.handleErrors(error.data);
                        });
                };
            }
        }
    }])