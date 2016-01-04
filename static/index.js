var app = angular.module('Player', [
  "ngRoute",
  "mobile-angular-ui",
]);

var songs;

app.config(function($routeProvider) {
  $routeProvider.when('/', {templateUrl: 'static/home.html'});
  $routeProvider.when('/dir/:dir', {templateUrl: 'static/dir.html', controller: 'DirController'});
});

app.controller('MainController', function($http, $scope) {
  var dirs = [];
  $http({
    method: 'POST',
    url: '/songs'
  }).then(function successCallback(response) {
    songs = response.data.songs;
    angular.forEach(songs, function(value, key) {
        dirs.push(value.dir);
    });
    $scope.dirs = dirs;
  }, function errorCallback(response) {
  });

});

app.controller('DirController', function($scope, $routeParams) {
  var dir = $routeParams.dir;
  angular.forEach(songs, function(value, key) {
      if (value.dir == dir) {
          $scope.songs = value.files;
      }
  });
});
