app.controller('ProductCtrl', ['$scope', 'ProductServ', function($scope, ProductServ){

  $scope.products_all  =  ProductServ.getProducts();
  console.log($scope.products_all);

}])
.service('ProductServ', function($http){
  
  this.getProducts = function(callback){
    return products; 
  }
});

