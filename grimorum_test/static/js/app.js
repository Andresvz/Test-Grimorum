angular.module('app', ['ui-notification'])
.config(['$interpolateProvider', 'NotificationProvider', function($interpolateProvider, NotificationProvider){
    $interpolateProvider.startSymbol('<%');
    $interpolateProvider.endSymbol('%>');
    NotificationProvider.setOptions({
      delay: 4000,
      startTop: 20,
      startRight: 10,
      verticalSpacing: 20,
      horizontalSpacing: 20,
      positionX: 'right',
      positionY: 'top'
    });
}])
.service('ProductServ', function($http){
  this.checkoutSend = function(data, callback){
    return $http.post('/checkout/', data)
    .then(callback, this.handleError) 
  }
})
.controller('ProductCtrl', ['$scope', '$timeout','ProductServ','$rootScope','Notification',function($scope,$timeout,ProductServ,
$rootScope,Notification){
 
  var cart = [];

  $scope.products_all = products;
  
  $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
  
  if(localStorage.getItem('order')){
    $rootScope.count = JSON.parse(localStorage.getItem('order')).length;
  }else{
    $rootScope.count = 0;
  }


  $scope.addToCar = function(product){
    var date = {};
    if(!localStorage.getItem('order')){
      data = {"item":product,"cantidad":1}
      cart.push(data)
      $rootScope.count = cart.length;
      console.log(cart)      
      localStorage.setItem('order', JSON.stringify(cart))
      $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
      Notification.success('Producto agregado al carrito');
    }else{
      cart = [];
      cart = JSON.parse(localStorage.getItem('order'))
      var Olditem = _.find(cart, function(item){ return item.item.pk == product.pk });
      if(Olditem){
        Olditem.cantidad++;
        angular.forEach(cart, function(value, key) {
          if(value.item.pk == Olditem.item.pk){
            value = Olditem;
          } 
        });
        console.log(cart)      
        $rootScope.count = cart.length;
        localStorage.setItem('order', JSON.stringify(cart))
        $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
        Notification.success('Producto agregado al carrito');
      }else{
        data = {"item":product,"cantidad":1}
        cart.push(data)
        console.log(cart)      
        $rootScope.count = cart.length;
        localStorage.setItem('order', JSON.stringify(cart))
        $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
        Notification.success('Producto agregado al carrito');
      }      
    }
  };

  $scope.max = function(order){
    var cart = [];
    cart = JSON.parse(localStorage.getItem('order'))
    var Olditem = _.find(cart, function(item){ return item.item.pk == order.item.pk });
    if(Olditem){
      Olditem.cantidad++;
      angular.forEach(cart, function(value, key) {
        if(value.item.pk == Olditem.item.pk){
          value = Olditem;
        } 
      });
      console.log(cart)      
      $rootScope.count = cart.length;
      localStorage.setItem('order', JSON.stringify(cart))
      $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
    }
  };

  $scope.minux = function(order){
    var cart = [];
    cart = JSON.parse(localStorage.getItem('order'))
    var Olditem = _.find(cart, function(item){ return item.item.pk == order.item.pk });
    if(Olditem){
      Olditem.cantidad--;
      angular.forEach(cart, function(value, key) {
        if(value.item.pk == Olditem.item.pk){
          value = Olditem;
        } 
      });
      console.log(cart)      
      $rootScope.count = cart.length;
      localStorage.setItem('order', JSON.stringify(cart))
      $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
    }
  };

  $scope.delete = function(order){


    var cart = [];
    cart = JSON.parse(localStorage.getItem('order'))
    var Olditem = _.find(cart, function(item){ return item.item.pk == order.item.pk });
    if(Olditem){
      angular.forEach(cart, function(value, key) {
        if(value.item.pk == Olditem.item.pk){
          cart.splice(key,1);
        } 
      });
      console.log(cart)      
      $rootScope.count = cart.length;
      localStorage.setItem('order', JSON.stringify(cart))
      $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
    }
  } 
  $scope.goDetail = function(product){
    $('#detail').modal('show');
    $rootScope.detail_product = product; 
  };
  $scope.addTOItemDetail = function(item,cant){
    var data = {};
    var cart = [];
  
    if(!localStorage.getItem('order')){
    data = {"item":item,"cantidad":cant}
      cart.push(data)
      $rootScope.count = cart.length;
      console.log(cart)      
      localStorage.setItem('order', JSON.stringify(cart))
      $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
      Notification.success('Producto agregado al carrito');
    }else{
      cart = [];
      cart = JSON.parse(localStorage.getItem('order'))
      var Olditem = _.find(cart, function(items){ return items.item.pk == item.pk });
      if(Olditem){
        Olditem.cantidad = Olditem.cantidad+cant;
        angular.forEach(cart, function(value, key) {
          if(value.item.pk == Olditem.item.pk){
            value = Olditem;
          } 
        });
        console.log(cart)      
        $rootScope.count = cart.length;
        localStorage.setItem('order', JSON.stringify(cart))
        $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
        Notification.success('Producto agregado al carrito');
      }else{
        data = {"item":item,"cantidad":cant}
        cart.push(data)
        console.log(cart)      
        $rootScope.count = cart.length;
        localStorage.setItem('order', JSON.stringify(cart))
        $rootScope.shopingCart = JSON.parse(localStorage.getItem('order'));
        Notification.success('Producto agregado al carrito');
      }      
    }
    $('#detail').modal('hide');
  }
  $scope.Total = function(){
    var total = 0; 
    angular.forEach(JSON.parse(localStorage.getItem('order')), function(item){
      total += parseInt(item.cantidad) * item.item.fields.price;
    });
    return total;
  };

  $scope.comprar =function(){
    var tmp = JSON.parse(localStorage.getItem('order'));
    var data ={};
    var aux =[]; 
    angular.forEach(tmp, function(item){
      item.item.fields.quantity = item.cantidad;
      item.item.fields.id = item.item.pk;
      data = item.item.fields;
      aux.push(data);
    });
    ProductServ.checkoutSend(aux, function(data){
      console.log(data)    
      if (data.data.status == 200) {
        localStorage.clear();
        Notification.info('Compra exitosa!');
        $timeout(function(){
          window.location.href='/';
        }, 3000);
      } else {
        console.error(data); 
        Notification.error('Intenta nuevamente!');
      }
    }); 
  }
}]);


