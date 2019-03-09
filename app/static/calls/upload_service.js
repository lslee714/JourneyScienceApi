"use strict";
angular.module("calls")
    .service('UploadApiService', ['$http', function($http){
        this.getUploads = function(){
            var uploadUrl = 'uploads';
            return $http.get(uploadUrl);
        };

        this.createUpload = function(uploadData, options){
            var options = options || {};
            return $http.post('', uploadData, options);
        };
    }]);