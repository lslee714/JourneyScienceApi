"use strict";
angular.module("calls")
    .service('CallsApiService', ['$http', function($http){
        this.getUploads = function(){
            var uploadUrl = 'uploads';
            return $http.get(uploadUrl);
        };

        this.createUpload = function(uploadData, options){
            var options = options || {};
            return $http.post('', uploadData, options);
        };
        this.getFieldAggregate = function(aggregateData){
            var aggregateUrl = 'fields';
            return $http.get(aggregateUrl, aggregateData);
        };
    }]);