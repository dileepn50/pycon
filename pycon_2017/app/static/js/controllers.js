var app = angular.module("myapp", ["ngRoute"]);
/*
function fun_view_profile($scope, $https)
{
	 url = '/app/view_profile';
	 $https.get(url).success( function(response) {
			 alert('ohh')
			       $scope.user_details = response; 
				      });
}
*/
app.controller('ctrl_view_profile', function($scope, $http)
				{
					var url = '/app/view_profile'
					$http.get(url).then( function(response) {
      				$scope.user_details = response.data; 
   					}); 
				}
				);

app.config(function($routeProvider)
{
	$routeProvider
   .when("/app/view_profile", {
   		templateUrl : "/static/view_profile.html",
		controller: 'ctrl_view_profile'
   })
   .when("/red", {
      	templateUrl : "/static/red.html"
   })
   .when("/sample_view", {
        templateUrl : "/static/sample_view.html"
   })
});
