"use strict";
angular.module("calls")
    .directive('uploadForm', ['$parse', 'UploadApiService', function($parse, UploadApiService){
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/calls/upload_form.html',
            link: function(scope, elem, attrs){
                scope.hasFile = false;
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;
                var fileInput = elem.find('#file-input');
                fileInput.bind('change', function(){
                    scope.$apply(function(){
                        var files = fileInput[0].files[0];
                        if(files){
                            modelSetter(scope, fileInput[0].files[0]);
                            scope.hasFile = true;
                        }else{
                            scope.hasFile = false;
                        }
                    });
                });
                scope.uploadPromise = null;
                scope.upload = function(){
                    var formData = new FormData();
                    formData.append('file', scope.uploadFile);
                    scope.uploadPromise = UploadApiService.createUpload(formData, {
                        //angularjs is bad at file data for some reason, override angularjs serialization
                        transformRequest: angular.identity,
                        headers: {'Content-Type': undefined}
                    }).then(
                    function(response){
                        scope.uploadPromise = null;
                    }, function(error){
                        scope.handleErrors(error.data);
                    });
                };
            }
        }
    }]);
