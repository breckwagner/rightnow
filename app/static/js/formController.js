rightnow.controller('formController', function($scope, $state) {
  $scope.formData = {};
  $scope.selectedTime = { name: 'None' };

  $scope.times = [
    { name: 'Right Now!' },
    { name: 'Later Tonight' },
    { name: 'Tomorrow' },
    { name: 'This Friday' },
    { name: 'This Saturday' }
  ];

  $scope.findEvent = function() {
    alert('FIND SOMETHING');
  }

  $scope.timeSelected = function() {
    //change here
    $state.transitionTo('form.what');
  }
});
