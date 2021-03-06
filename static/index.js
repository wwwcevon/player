var app = angular.module('Player', [
  "ngRoute",
  "mobile-angular-ui",
]);

var songs;
var current_song;
var current_volume = 1;

app.config(function($routeProvider) {
  $routeProvider.when('/', {templateUrl: 'static/dir.html', reloadOnSearch: false});
  $routeProvider.when('/dir/:dir', {templateUrl: 'static/dir.html', controller: 'DirController', reloadOnSearch: false});
  $routeProvider.when('/all-songs', {templateUrl: 'static/dir.html', controller: 'DirController', reloadOnSearch: false});
  $routeProvider.otherwise({redirecTo: '/all-songs'});
});

app.controller('MainController', function($http, $scope) {
  var dirs = [];
  if (songs === undefined || songs === null) {
    console.log(songs);
    $http({
      method: 'POST',
      url: '/songs'
    }).then(function successCallback(response) {
      songs = response.data.songs;
      angular.forEach(songs, function(value, key) {
        dirs.push(value.dir);
        if ($scope.songs === undefined) {
          $scope.songs = [];
        }
        $scope.songs = $scope.songs.concat(value.files);
      });
      $scope.dirs = dirs;
    }, function errorCallback(response) {
    });
  }

  $scope.playSong = function(song) {
    current_song = song;
    $http({
      method: 'POST',
      data: {'song': current_song.file},
      url: '/play'
    }).then(function successCallback(response) {
    }, function errorCallback(response) {
    });
  };
});

app.controller('DirController', function($scope, $routeParams, $http, $rootScope) {
  var dir = $routeParams.dir;
  angular.forEach(songs, function(value, key) {
    if (value.dir == dir) {
      $scope.songs = value.files;
    }
  });

  $scope.playSong = function(song) {
    current_song = song;
    $http({
      method: 'POST',
      data: {'song': current_song.file},
      url: '/play'
    }).then(function successCallback(response) {
    }, function errorCallback(response) {
    });
  };
});

app.controller('SongController', function($scope, $http) {
  $scope.nextSong = function() {
    $http({
      method: 'POST',
      url: '/next'
    }).then(function successCallback(response) {
      current_song = '';
    }, function errorCallback(response) {
    });
  };
  $scope.stopPlay = function() {
    $http({
      method: 'POST',
      url: '/stop'
    }).then(function successCallback(response) {
      current_song = '';
    }, function errorCallback(response) {
    });
  };
  $scope.increaseVol = function() {
    $http({
      method: 'POST',
      url: '/set_volume',
      data: {'volume': 0.05}
    }).then(function successCallback(response) {
      current_volume = response.data.current_volume;
    }, function errorCallback(response) {
    });
  };
  $scope.decreaseVol = function() {
    $http({
      method: 'POST',
      url: '/set_volume',
      data: {'volume': -0.05}
    }).then(function successCallback(response) {
      current_volume = response.data.current_volume;
    }, function errorCallback(response) {
    });
  };
});

