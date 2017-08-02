var app = angular.module("myapp", ["ngRoute"]);
function fun_view_profile($scope, $http, $location, $timeout, $interval)
{
	 var url = '/app/view_profile';
	 $http.get(url).then( function(response) {
			 //alert('ohh')
			//alert(response.data);
			       $scope.user_details = response.data; 
				   $scope.list = [{'name': 'abc', 'country': 'india'}, {'name': 'def', 'country': 'india'}];
				   $scope.StateList = ['karnataka', 'kerala', 'mp', 'ap', 'tamilnadu', 'wb'];
				   $scope.names = [
    									{name:'Jani',country:'Norway'},
    									{name:'Carl',country:'Sweden'},
    									{name:'Margareth',country:'England'},
    									{name:'Hege',country:'Norway'},
    									{name:'Joe',country:'Denmark'},
    									{name:'Gustav',country:'Sweden'},
    									{name:'Birgit',country:'Denmark'},
    									{name:'Mary',country:'England'},
    									{name:'Kai',country:'Norway'}
  								  ]; 
					$scope.sort_array = function(parameter)
										{
											$scope.myOrderBy = parameter
										}


					$scope.current_location = $location.absUrl();
//					$scope.current_location = '/app/edit_profile';
					$timeout(function(){
					$scope.message = 'I am here';			
					}, 3000);
					$interval(function()
					{
						$scope.current_time = new Date().toLocaleTimeString();
					},3000);
					$scope.showMe = true 
					$scope.change_status = function()
									{
										$scope.showMe = !$scope.showMe;
									}
				
				      });
}
function fun_edit_profile($scope, $http)
{
	alert('inside edit profile');
	var url = '/app/edit_profile';
	$http.get(url).then(function(response){
			$scope.user_details = response.data;
			$scope.username = $scope.user_details['username'];
			$scope.first_name = $scope.user_details['first_name'];
			$scope.last_name = $scope.user_details['last_name'];
			$scope.email = $scope.user_details['email'];
	});
}
function fun_reg_conference($scope, $http)
{
	var url = '/app/state_list';
	$http.get(url).then(function(response)
		{
			$scope.state_list = response.data;
		}
	);	
}

function fun_request_details($scope, $http)
{
	var url = '/app/request_details';
	$http.get(url).then(function(response)
		{
			$scope.request_details = response.data;
		}
	);
}

function fun_not_adminUser($scope, $http)
{
	var url = '/app/admin';
	//alert('fun_not_adminUser');
	$http.get(url).then(function(response)
		{
			$scope.details = response.data;
			/*
			$scope.adminUser_details = response.data;
			if($scope.adminUser_details['authorized'])
			{
				

			}
			else
			{
				$scope.authorixed = false;
				$scope.username = scope.adminUser_details['username'];

			}
			*/
		}
		);
}

function fun_get_userDetail($scope, $http, $routeParams)
{
	var url = '/app/get_user_details/' + $routeParams.username;
	//alert('fun_get_userDetail');
	$http.get(url).then(function(response)
		{
			//alert(response.data);
			$scope.details = response.data;
			$scope.username = $scope.details.username;
		});
}

fucntion fun_get_requestStatus($scope, $http)
{
	var url = '/app/request_status';
	$http.get(url).then(function(response))
		{
			$scope.details = response.data;
		}
}		


app.controller('ctrl_view_profile', fun_view_profile);
app.controller('ctrl_edit_profile', fun_edit_profile);
app.controller('ctrl_reg_conference', fun_reg_conference);
app.controller('ctrl_request_details', fun_request_details);
app.controller('ctrl_not_adminUser', fun_not_adminUser);
app.controller('ctrl_get_userDetail', fun_get_userDetail);
app.controller('ctrl_get_requestStatus', fun_get_requestStatus);

app.config(function($routeProvider)
{
	$routeProvider
   .when("/app/view_profile", {
   		templateUrl : "/static/html/view_profile.html",
		controller: 'ctrl_view_profile'
   })
   .when("/app/edit_profile", {
      	templateUrl : "/static/html/edit_profile.html",
		controller: "ctrl_edit_profile"
   })
   .when("/app/post_request", {
		   templateUrl : '/static/html/reg_conference.html',
		   controller: 'ctrl_reg_conference'
   })
   .when("/app/request_details", {
		   templateUrl: '/static/html/request_details.html',
		   controller: 'ctrl_request_details'
	})
   .when("/app/admin", { 
		   templateUrl: '/static/html/not_adminUser.html',
   			controller: 'ctrl_not_adminUser'
   })
   .when("/app/get_user_details/:username", {
		   templateUrl: '/static/html/get_userDetail.html',
   		   controller: 'ctrl_get_userDetail'
	})
   .when("/app/request_status", {
		   templateUrl: '/static/html/request_status.html',
   			controller: 'ctrl_get_requestStatus'
		   )
});





