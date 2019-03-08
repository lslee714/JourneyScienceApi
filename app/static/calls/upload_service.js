"use strict";
(function(a, $){
    a.module("calls")
        .service('UploadApiService', ['$http', function($http){
            this.baseUrl = '/upload';
            this.post = function(postData, options){
                var options = options || {};
                return $http.post(this.baseUrl, postData, options);
            };
        }])
})(angular, jQuery)