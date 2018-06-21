// Main app to display topology using information provided by server API
// Use ngVis, ngDraggable, ngDialog module
var viewer = angular.module('viewer', ['ngVis','ngDraggable','ngDialog']);

// Main controller of topology
// Use contextMenu factory of main app and Data service of ngVis module
viewer.controller('MainCtrl', ['$scope','contextMenu','Data',

  function($scope,contextMenu,Data) {


    // Get network information and draw topology first time
    Data.getNetwork($scope);

    // Objects draggable and addable to topology
    // Locate in left side of topology
    $scope.addableObjects = [
      {
        name : 'Computer',
        image: '/map/img/Computer.ico'
      },
      {
        name : 'Router',
        image: '/map/img/Router.ico'
      },
      {
        name : 'Switch',
        image: 'map/img/Switch.ico'
      },
      {
        name : 'Unknown',
        image: 'map/img/Unknown.ico'
      },
      {
        name : 'edge',
        image: '/map/img/Edge.jpg'
      }
    ]

    // Fire when drag an object from previous list to topology
    // If object is an edge, switch to addEdgeMode of vis network and select all node availabel
    // If object is a node, call addNode function from contextMenu factory
    $scope.onDropComplete=function(obj,event) {
      if(obj.name != 'edge') {
        contextMenu.addNode($scope,obj,event);
      } else {
        $scope.network.addEdgeMode();
        $scope.network.selectNodes($scope.network.body.nodeIndices,false);
      }
    }

    // General option of vis network
    // Just copy somewhere, almost nonsense
    $scope.options = {
      autoResize: false,
      physics:{
        enabled: true,
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity       : 0.3,
          springLength         : 95,
          springConstant       : 0.04,
          damping              : 0.09,
          avoidOverlap         : 0
        }
      },
      layout:{
        randomSeed    :5,
        improvedLayout:true,
      },
      edges: {
        arrows: {
          to:{
            enabled    :true,
            scaleFactor:0.5,
            type       :'circle',
          },
          from:{
            enabled    :true,
            scaleFactor:0.5,
            type       :'circle',
          }
        },
      },
      manipulation: {
        enabled: false,
        // Override addEdge function of vis by addEdge function from contextMenu factory
        addEdge: function (data, callback) {
          if (data.from == data.to) {
              callback(null);
              return;
          }
          contextMenu.addEdge($scope,data,callback);
        }
      },
    }

    // Watch changed in $scope.network
    // Mainly use in fire context menu
    $scope.$watchCollection('network', function (network) {
      if (network == null) {
          return;
      }

      // Fire if right click on topology area
      network.on('oncontext', function(params) {
        // Prevent default context menu of browser
        params.event.preventDefault();

        // Determine which menu will dropdown base on number of nodes and edges have selected
        var item;
        if (params.nodes.length > 0 && params.nodes.length < 2) {
          $scope.utils = contextMenu.NodeMenu;          // Only 1 node has selected
          item         = params.nodes[0];               // So user clicked on a node
        }                                               // Node menu will be used
        else if (params.edges.length > 0) {
          $scope.utils = contextMenu.EdgeMenu;          // 1 edge so 2 nodes have selected
          item         = params.edges[0];               // So user clicked on an edge
        }                                               // Edge menu will be used
        else $scope.utils = contextMenu.GeneralMenu; // Nothing has selected, general menu will be used
        $scope.$apply();  // Immediately apply to all variables of $scope

        // Show context menu
        contextNode               = document.getElementById('contextmenu-node'); 
        contextNode.style.display = "inline-block";
        contextNode.style.left    = params.event.pageX + "px";
        contextNode.style.top     = params.event.pageY + "px";

        // Fire corresponding function when user click on an option in context menu
        // Item is node, edge or nothing based on which menu was used
        contextNode.onclick = function(e) {
          $scope.utils.every(function(element,index) {
            if (element.name == e.target.innerText) {
              element.function($scope,item);
              return false;
            }
            return true;
          })
          // Keep context menu hiding after use
          contextNode.style.display = "none";
        }
        // Off menu when mouse leave
        contextNode.onmouseleave = function (e) {
            contextNode.style.display = "none";
        }
        // Prevent context menu when another is being on
        contextNode.oncontextmenu = function (e) {
            e.preventDefault();
        }
      })

    })

  }
]);


// Factory of main app 
// Mainly contain function of context menu
// Use $http service of angularJs, Data service of ngVis module and ngDialog service of ngDialog module 
viewer.factory('contextMenu',['$http','Data','ngDialog',
  function ($http,Data,ngDialog) {
    var contextMenu = {};
    var nodesDetail = {}; // Nodes cache
    var edgesDetail = {}; // Edges cache

    // General menu when right click fire with no node or edge has selected
    contextMenu.GeneralMenu = [
      {
        // Send signal to proxy to discover network using snmp protocol
        // This action will take a while approximately about 5 seconds
        name:'Discover Network',
        function: function(scope) { 
          // Open waiting dialog
          ngDialog.open({
            template:'<img src="map/img/waiting.gif">',
            plain: true,
            controller: ['$scope',function($scope) {
              Data.discover().then(function(res) {
                if (res.status == 'success') {
                  Data.getNetwork(scope); // Redraw topology using new data when discover successful
                  var nodesDetail = {};   // Refresh cache
                  var edgesDetail = {};   //
                } 
                else {
                  alert('Cannot discover network!');
                }
                $scope.closeThisDialog();
              });
            }]
          })
        }
      },
      {
        name: 'Synchronize',
        function: function(scope) {
          Data.sync().then(function(res) {
            if (res.status == 'success') {
              Data.getNetwork(scope); // Redraw when rollback success
              nodesDetail = {};       // Refresh cache
              edgesDetail = {};       //
            } else {
              alert('Cannot synchnorize data')
            }
          })
        }
      },
      {
        // Commit change in database
        // Any changing user made in topology are just temporary and can rollback before doing this action
        name:'Save change',
        function: function(scope) {
          Data.saveChange().then(function(data) {
            if (data.status="success") {
              Data.getNetwork(scope); // Redraw when save success
              nodesDetail = {};       // Refresh cache
              edgesDetail = {};       //
            } 
            else {
              alert("Cannot save data");
            }
          })
        }
      },
      {
        // Rollback changed that user have just done
        name:'Discard change',
        function: function(scope) {
          Data.discardChange().then(function(data) {
            if (data.status="success") {
              Data.getNetwork(scope); // Redraw when rollback success
              nodesDetail = {};       // Refresh cache
              edgesDetail = {};       //
            } 
            else {
              alert("Cannot save data");
            }
          })
        }
      }
    ]

    // Node menu when right click fire with one node has selected
    contextMenu.NodeMenu = [
      {
        // View full detail of node
        name:'View Detail',
        function: function(scope,node) {
          // Open dialog to show node detail
          ngDialog.open({
            template: 'map/template/detail_node.html',
            controller: ['$scope',function($scope) {
              // Check if data of this node already in cache
              // If not, query using Data service and save in cache to fast perform next time
              if (nodesDetail[node]) {
                $scope.detail = nodesDetail[node];
              } 
              else {
                Data.getNodeDetail(node).then(function(data) {
                  if (data) {
                    nodesDetail[node] = data;
                    $scope.detail = nodesDetail[node];
                  } 
                  else $scope.closeThisDialog();
                })
              }
            }]
          });
        }
      },
      {
        // Edit detail of node in database
        // Action can rollback 
        name:'Edit Node',
        function: function (scope,node) {
          // Open dialog
          ngDialog.open({
            template: 'map/template/edit_node.html',
            controller: ['$scope',function($scope) {

              // Get node detail first
              // Then make a copy to check whether detail has changed or not
              var detail;
              $scope.detail={};

              if(nodesDetail[node]) {
                detail = nodesDetail[node];
                if (detail.manual)
                  angular.copy(detail,$scope.detail);
                else {
                  setTimeout(function() {
                    alert("This node is fixed");
                    $scope.closeThisDialog();
                  }, 100);
                }
              } else {
                Data.getNodeDetail(node).then(function(data) {
                  if (data) {
                      nodesDetail[node] = data;
                      detail = nodesDetail[node];
                      if (detail.manual)
                        angular.copy(detail,$scope.detail);
                      else {
                        alert("This node is fixed");
                        $scope.closeThisDialog();
                      }
                  } else $scope.closeThisDialog();
                })
              }

              // Fire when user click confirm button
              $scope.confirm = function() {
                // Send to server new data if the origin and the copy are not the same
                if (!angular.equals($scope.detail,detail)) {
                  // Confirm alert
                  if (confirm('Do you want to change?')) {
                    Data.editNode(node,$scope.detail).then(function(res) {
                      console.log(res);
                      if (res.status == 'success') {
                        nodesDetail[node] = $scope.detail;
                        Data.getNetwork(scope);
                      } 
                      else 
                        alert('Cannot edit this node!');
                    });
                    $scope.closeThisDialog();
                  }
                } 
                else $scope.closeThisDialog();
              }
            }]
          });
          
        }
      },
      {
        // Delete node and edges directly connect to it
        // Action can rollback
        name:'Delete Node',
        function: function (scope,node) {
          Data.deleteNode(node).then(function(res) {
            if (res.status == 'success') 
              Data.getNetwork(scope);
            else if (res.status == 'fixed') 
              alert('This node is fixed');
            else if (res.status == 'error')
              alert('Cannot delete this node!');
          });
          
        }
      }
    ]


    // Edge menu when right click fire with 1 edge has selected
    contextMenu.EdgeMenu = [
      {
        // View edge detail 
        // All data are already in cache but need to transform
        name:'View Edge Detail',
        function: function(scope,edge) {
          // Open dialog
          ngDialog.open({
            template: 'map/template/detail_edge.html',
            controller: ['$scope',function($scope) {
              // Search in factory cache first
              // If don't exist, generate and push in
              if (edgesDetail[edge]) {
                $scope.detail = edgesDetail[edge];
              } else {
                $scope.detail = Data.getEdgeDetail(scope,edge);
                edgesDetail[edge]=$scope.detail;
              }
            }]
          });
        }
      },
      {
        // Delete connect between two node
        // Action can rollback
        name:'Delete Edge',
        function: function(scope,edge) {
          Data.deleteEdge(edge).then(function(res) {
            if (res.status == 'success') 
              Data.getNetwork(scope);
            else if (res.status == 'fixed')
              alert('This edge is fixed');
            else 
              alert("Error when delete this edge");
          }) 
        }
      },
      {
        // Turn off or turn on port status between two end point of edge
        name:'Edit Port Status',
        function: function(scope,edge) {
          // Open dialog
          ngDialog.open({
            template: 'map/template/edit_edge.html',
            controller: ['$scope',function($scope) {
              // Get edge detail first
              // Then make a copy to check whether detail has changed or not
              var detail;
              $scope.detail = {};

              if (edgesDetail[edge]) {
                detail = edgesDetail[edge];
              } 
              else { 
                detail = Data.getEdgeDetail(scope,edge);
                edgesDetail[edge] = detail;
              }

              angular.copy(detail,$scope.detail);
              
              // Fire when user click on confirm button
              $scope.confirm = function() {
                // Send to server new data if the origin and the copy are not the same
                if (!angular.equals($scope.detail,detail)) {
                  // Confirm alert
                  if (confirm('Do you want to change?')) {
                    Data.editEdge(edge,$scope.detail).then(function(res) {
                      if (res.status == 'success') {
                        edgesDetail[edge] = $scope.detail;
                        Data.getNetwork(scope);
                      } 
                      else 
                        alert('Cannot edit this edge');
                    });
                    $scope.closeThisDialog();
                  }
                } 
                else $scope.closeThisDialog();
              }
            }]
          });
        }
      }
    ]

    // Override original addEdge() function of visjs to take advantage of addEdge interaction of visjs
    // Network tranform to addEdgeMode when edge symbol in left side is dragged onto topology area
    // Drag from one node to another to connect two
    // Action can rollback
    contextMenu.addEdge = function(scope,data,callback) {
      // Open dialog
      ngDialog.open({
        template: 'map/template/add_edge.html',
        controller: ['$scope',function($scope) {

          // Get detail of two nodes are connected through this edge
          $scope.detail = {
            'Device A': {},
            'Device B': {}
          };

          var getDetail = function(device,node) {

            // Don't suggest ports of node that already connected to other
            var updateDetail = function(device,data) {
              var edges   = scope.data.edges._data;
              device.name = data.general.Name;
              device.IP   = data.general.IP;
              for (var key in data.ports) {
                port = data.ports[key];
                var exit = 0;

                for (edge in edges) {
                  if (edges[edge].fromMac == port.mac || edges[edge].toMac == port.mac) {
                    exit = 1;
                    break;
                  } 
                }
                if (exit == 1) continue;

                device.ports[key] = {
                  'MAC'   : port.mac,
                  'status':port.status?"On":"Off"
                };
              }
            }

            // Get detail of node first then analyze
            device.ports = {};
            if (nodesDetail[node]) {
              updateDetail(device,nodesDetail[node]);
            } else {
              Data.getNodeDetail(node).then(function(data) {
                if (!data) $scope.closeThisDialog();
                nodesDetail[node] = data;

                updateDetail(device,data);
              })
            }
          }

          getDetail($scope.detail['Device A'],data.from);
          getDetail($scope.detail['Device B'],data.to)

          // Confirm function when user click in confirm button
          $scope.confirm = function() {
            // Port of each node much be specified
            deviceA = $scope.detail['Device A'];
            deviceB = $scope.detail['Device B'];
            if (deviceA.port && deviceB.port) {
              deviceA.MAC = deviceA.ports[deviceA.port].MAC;
              deviceB.MAC = deviceB.ports[deviceB.port].MAC;
              delete deviceA.ports
              delete deviceB.ports
              Data.addEdge($scope.detail).then(function(res) {
                if (res.status == "success") 
                  Data.getNetwork(scope);
                else 
                  alert("Cannot add this edge");
              })
            } 
            else alert("Port must be specified");
            $scope.closeThisDialog();
          }
          scope.network.unselectAll();
          scope.network.disableEditMode();
        }]
      });
    }

    // Function fire when user drag one device in node type from left list to topology
    // Action can rollback
    contextMenu.addNode = function(scope,node,event) {
      // Open dialog
      ngDialog.open({
        template: 'map/template/add_node.html',
        controller: ['$scope',function($scope) {
          // Generate new example detail of node
          // Feel free to change it
          $scope.detail = {
            general: {
              'Name'       :'New Device',
              'IP'         :'0.0.0.0',
              'Location'   :'Unknown',
              'Description':'Unknown',
              'Up Time'    :'Unknown',
              'Note'       :''
            },
            type: node.name,
            portLen: 0,
            ports: {}
          };;

          // Mainly watch if user change portLen in $scope.detail to regenerate port option of node
          $scope.$watchCollection('detail',function(detail) {
            // Create new ports or delete existing ports
            var portKeys = Object.keys(detail.ports);
            var portLen = portKeys.length;

            // Create new ports if portLen was increased
            if (portLen < detail.portLen && Number.isInteger(parseInt(detail.portLen))) {
              for (var i=portLen;i<detail.portLen;i++) {
                detail.ports[i] = {
                  id    : 0,
                  des   : 'Unknown',
                  speed : 'Unknown',
                  mac   : 'Unknown',
                  status: false,
                  note  : 'Unknown'
                }
              }
            } 
            // Delete exist ports if portLen was decreased
            else if (portLen > detail.portLen && Number.isInteger(parseInt(detail.portLen))) {
              for (var i=detail.portLen;i<portLen;i++) {
                delete detail.ports[i];
              }
            }
          })

          // Confirm function
          $scope.confirm = function() {
            // Check if ip is in ip form
            var ipPattern = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
            if (ipPattern.test($scope.detail.general['IP']) && $scope.detail.general['IP'] != "0.0.0.0") {
              // Send to server and redraw topology
              Data.addNode($scope.detail).then(function(res) {
                if (res.status == 'success') {
                  Data.getNetwork(scope);
                } else 
                  alert('Cannot add node!');
              })
            } else {
              alert("Wrong IP!");
            }
            $scope.closeThisDialog();
          }
        }]
      });
    }

    return contextMenu;
  }
])

