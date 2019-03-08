"use strict";
(function(a, $){
    a.module("calls")
        .controller('CallsCtrl', ['$scope', function($scope){
            $scope.payload = {};
        }]);
})(angular, jQuery)