"use strict";
(function(a, $){
    a.module("calls")
        .service('UploadApiService', ['$http', function($http){
            this.post = function(postData, options){
                var options = options || {};
                return $http.post('', postData, options);
            };
        }])
})(angular, jQuery)