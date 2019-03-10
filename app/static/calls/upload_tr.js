angular.module('calls')
    .directive('uploadTr', [function(){
        return {
            restrict: 'A',
            replace: true,
            templateUrl: '/static/calls/upload_tr.html',
            link: function(scope, elem, attrs){
                scope.$watch('upload.include', function(newVal){
                    if(newVal===true){
                        scope.uploadsToAggregate.push(scope.upload.id);
                    }else if(scope.uploadsToAggregate.indexOf(scope.upload.id) > -1){
                        var index = scope.uploadsToAggregate.indexOf(scope.upload.id);
                        scope.uploadsToAggregate.splice(index, 1);
                    }
                });
            }
        }
    }]);