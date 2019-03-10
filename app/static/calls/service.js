"use strict";
angular.module("calls")
    .service('CallsApiService', ['$http', '$httpParamSerializer', function($http, $httpParamSerializer){
        this.getUploads = function(){
            var uploadUrl = 'uploads';
            return $http.get(uploadUrl);
        };

        this.createUpload = function(uploadData, options){
            var options = options || {};
            return $http.post('', uploadData, options);
        };
        this.getFieldAggregate = function(aggregateData){
            var query = $httpParamSerializer(aggregateData);
            var aggregateUrl = 'fields' + '?' + query;
            return $http.get(aggregateUrl);
        };
    }]);