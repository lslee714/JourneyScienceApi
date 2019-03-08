"use strict";
(function(a, $){
    a.module("calls")
        .directive('uploadForm', ['$parse', 'UploadApiService', function($parse, UploadApiService){
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/calls/upload_form.html',
                link: function(scope, elem, attrs){
                    var model = $parse(attrs.fileModel);
                    var modelSetter = model.assign;
                    var fileInput = $('#file-input');
                    fileInput.bind('change', function(){
                        scope.$apply(function(){
                            modelSetter(scope, fileInput[0].files[0]);
                        });
                    });

                    scope.upload = function(){
                        var formData = new FormData();
                        formData.append('file', scope.uploadFile);
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