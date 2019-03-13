"use strict";
angular.module("calls")
    .controller('CallsCtrl', ['$scope', '$window', 'CallsApiService', function($scope, $window, CallsApiService){

        $scope.errors = [];
        $scope.handleErrors = function(error) {
            var errorMsg = error.error;
            //handle unhandled errors
            if(!errorMsg) {
                var $error = $(error);
                errorMsg = $error.find('.errormsg').text();
            }
            if(!$scope.errors.includes(errorMsg)){
                $scope.errors.push(errorMsg);
            }
            $window.scrollTo(0,0);
        };

        $scope.messages = []
        $scope.handleResponse = function(response){
            $scope.messages.push(response.data);
        };

        $scope.payload = {};
        $scope.uploads = [];
        $scope.uploadsToAggregate = [];

        $scope.load = function(){
            CallsApiService.getUploads().then(
                function(response){
                   var responseData = response.data;
                   $scope.uploads = responseData.data;
                }).catch(function(error){
                    $scope.handleErrors(error.data)
                });
        };

        $scope.load();

        $scope.statusUrls = [];
        $scope.pollPromise = null;
        $scope.pollStatuses = function(){
            angular.forEach($scope.statusUrls, function(url){
                $scope.pollPromise = CallsApiService.getTaskStatus(url).then(function(response){
                    console.log(response);
                    if(response.data && response.data.state=='SUCCESS'){
                        $scope.messages.push(response.data.result.message);
                    }else if(response.data.state=='FAILURE'){
                        $scope.errors.push(response.data.result.status + ' ' + response.data.result.result);
                    };
                });
            });
        };
    }]);