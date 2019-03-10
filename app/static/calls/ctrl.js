"use strict";
angular.module("calls")
    .controller('CallsCtrl', ['$scope', 'CallsApiService', function($scope, CallsApiService){
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
        };

        $scope.payload = {};
        $scope.uploads = [];

        $scope.load = function(){
            CallsApiService.getUploads().then(
                function(response){
                   var responseData = response.data;
                   $scope.uploads = responseData.data;
                },function(error){
                    $scope.handleErrors(error.data)
                }
            )
        };
        $scope.load();

    }]);