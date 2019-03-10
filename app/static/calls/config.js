
angular.module('calls')
    .config(['$qProvider', function($qProvider){
        $qProvider.errorOnUnhandledRejections(false);
    }]);
