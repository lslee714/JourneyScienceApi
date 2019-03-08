"use strict";
(function(a, $){
    a.module("calls")
        .directive('uploadForm', ['UploadApiService', function(UploadApiService){
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/calls/upload_form.html',
                link: function(scope, elem, attrs){
                    scope.upload = function(){
                        var formData = new FormData();
                        formData.append('file', scope.payload.file);
                        UploadApiService.post(formData, {
                            //angularjs is bad at file data for some reason, override angularjs serialization
                            transformRequest: a.identity,
                            headers: {'Content-Type': undefined}
                        }).then(function(response){
                            console.log(response);
                        });
                    };
                }
            }
        }])
})(angular, jQuery)