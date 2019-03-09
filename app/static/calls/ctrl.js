"use strict";
angular.module("calls")
    .controller('CallsCtrl', ['$scope', function($scope){
        $scope.payload = {};
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
    }]);