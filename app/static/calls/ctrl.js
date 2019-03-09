"use strict";
angular.module("calls")
    .controller('CallsCtrl', ['$scope', function($scope){
        $scope.payload = {};
        $scope.errors = [];
        $scope.handleErrors = function(error) {
            if(!$scope.errors.includes(error)){
                $scope.errors.push(error);
            }
        };
    }]);