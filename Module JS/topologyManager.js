// Second app to create new topology
// Use $http service and ngDialog service
var manager = angular.module('manager', ['ngDialog']);

// Main controller of manager app
// Use Utilities server
manager.controller('MainCtrl', ['$scope','Utilities',
  function($scope,Utilities) {

    // Show existing topologies 
    Utilities.getTopologies().then(function(topos) {
      $scope.topos = topos;
    });

    // Add new topology
    $scope.add = Utilities.addTopology();
  }
])

// Utilities service 
// Contains functions to use in app 
manager.service('Utilities',['$http','ngDialog', 
  function($http,ngDialog) {
    var baseServerAddr = 'http://localhost:5000/topology/';

    var getObjLength = function() {
      return function(obj) {
        return Object.keys(obj).length;
      }
    }

    // Add new rack to an existing racks list
    var addRack = function() {
      return function(racks) {
        var index = Object.keys(racks).length;
        var newRack = {
          ip     : '',
          name   : 'New rack controller',
          devices: {}
        }
        racks[index+1]=newRack;
      }
    }

    // Delete specific rack from racks list
    var deleteRack = function() {
      return function(racks, rack) {
        for (var key in racks) {
          if (racks[key] == rack) {
            delete racks[key];
            return;
          }
        }
      }
    }

    // Add new device to an existing rack
    var addDevice = function() {
      return function(devices) {
        var index = Object.keys(devices).length;
        var newDevice = {
          ip        : '',
          comString : '',
          comConfirm: '',
          check     : '',
          checkColor: '',
          confirm   : confirmComString()
        }
        devices[index+1] = newDevice;
      }
    }

    // Delete specific from a rack 
    var deleteDevice = function() {
      return function(devices, device) {
        for (var key in devices) {
          if (devices[key] == device) {
            
            return;
          }
        }
      }
    }

    // Check user input in each form
    var checkInput = function(racks) {
      for (var rackKey in racks) {
        var rack = racks[rackKey];
        if (!rack.name || !rack.ip || Object.keys(rack.devices).length == 0) return false;
        for (var deviceKey in rack.devices) {
          var device = rack.devices[deviceKey];
          if (!device.ip || !device.comString || ( device.check != undefined && device.check != 'OK')) return false;
        }
      }
      return true;
    }

    // Confirm community string and notice user
    var confirmComString = function() {
      return function(device) {
        if (!device.comString || !device.comConfirm) {
          device.check = '';
        }
        else if (device.comString == device.comConfirm) {
          device.check      = 'OK';
          device.checkColor = 'green';
        }
        else {
          device.check      = 'Not match';
          device.checkColor = 'red';
        }
      }
    }

    // Get topology detail from Webserver API to show
    var getTopologyDetail = function() {
      return function(id) {
        ngDialog.open({
          template:'map/template/detail_topo.html',
          cache: false,
          width: '42%',
          controller: ['$scope', function($scope) {
            $http.get(baseServerAddr+'detail/',{params:{'topoId':id}}).then(function(res) {
              if (res.data.status == 'error') {
                alert("Cannot get this topology detail");
                $scope.closeThisDialog();
              }
              else {
                $scope.topo         = res.data;
                $scope.getObjLength = getObjLength();
              }
            })
          }]
        })
      }
    }

    // Modify rack name, rack IP, device IP and device community string of a topology
    var modifyTopology = function() {
      return function(id) {
        ngDialog.open({
          template: 'map/template/edit_topo.html',
          cache: false,
          width: '42%',
          controller: ['$scope', function($scope) {

            // Get topology detail and duplicate this data
            var origin = {};

            $http.get(baseServerAddr+'detail/',{params:{'topoId':id}}).then(function(res) {
              if (res.data.status == 'error') {
                alert("Cannot get this topology detail");
                $scope.closeThisDialog();
              }
              else {
                $scope.topo         = res.data;
                $scope.getObjLength = getObjLength();

                angular.copy($scope.topo,origin);
              }
            },function(error) {
              console.log(error);
            })

            // Check difference between origin data and modified data
            // Post to server if somethings different
            $scope.confirm = function() {
              if (checkInput($scope.topo.racks)) {
                if (!angular.equals($scope.topo,origin)) {
                  if (confirm('Do you want to change?')) {
                    $http.post(baseServerAddr+'edit/', JSON.stringify($scope.topo)).then(function(res) {
                      if (res.data.status == 'error') alert("Cannot modify this topology");
                    },function(error) {
                      console.log(error);
                    })
                  }
                }
                $scope.closeThisDialog();
              }
            }
          }]
        })
      }
    }

    // Delete an existing topology from topo lists
    var deleteTopology = function() {
      return function(id) {
        var check = confirm('Are you want to delete this topology?');

        if (!check) return;
        
        var promise = $http.post(baseServerAddr+'delete/',JSON.stringify({'topoId':id})).then(function(res) {
          if (res.data.status != 'success') alert("Cannot delete this topology");
          else location.reload();
        },function(error) {
          console.log(error);
        })
        return promise;
      }
    }

    // Get topology list and assign function to properties of each topo
    this.getTopologies = function() {
      var promise = $http.get(baseServerAddr+'list/').then(function(res) {
        var topos = [];

        for (var i=0;i<res.data.length;i++) {
          var topo = res.data[i];
          var newTopo = {
            'id'    : topo.id,
            'name'  : topo.name,
            'detail': getTopologyDetail(topo.id),
            'modify': modifyTopology(topo.id),
            'delete': deleteTopology(topo.id)
          }
          topos.push(newTopo);
        }
        return topos;
      },function(error) {
        console.log(error);
      })
      return promise;
    }

    // Generate a dialog to add new topology
    this.addTopology = function() {
      return function() {
        ngDialog.open({
          template: 'map/template/add_topo.html',
          controller: ['$scope',function($scope) {

            // Add new rack controller to topology
            $scope.name  = 'New Topology';
            $scope.racks = {};

            $scope.addRack      = addRack();
            $scope.deleteRack   = deleteRack();
            $scope.addDevice    = addDevice();
            $scope.deleteDevice = deleteDevice();
            
            // Submit function
            $scope.submit = function() {

              if (!checkInput($scope.racks)) return;

              // Reform data so server can read
              data = {
                name : $scope.name,
                racks: $scope.racks
              }

              console.log(data);

              // Send reformed data to server
              $http.post(baseServerAddr+'add/',JSON.stringify(data)).then(function(res) {
                if (res.data.status != 'success') alert('Cannot add topology!');
                else location.reload();
              },function(error) {
                console.log(error);
              })
              $scope.closeThisDialog();
            }
          }]
        })
      }
    }
  }
])