// ngVis module with Data service and visNetwork directive
var ngVis=angular.module('ngVis', []);

// Data service to do most action about communicating with server
ngVis.service('Data',['$http', function ($http) {

    var baseUrl = 'http://localhost:5000';
    var imgUrl  = "map/img/";
    var LENGTH  = 100;

    // Create 1 vis node 
    // Utility function, not service function
    var createNode = function(node) {
        var newNode = {};

        newNode.id    = node.id;
        newNode.shape = "image";
        newNode.group = node.group
        newNode.title = node.ip;
        newNode.label = node.name;
        newNode.image = imgUrl+node.type+".ico";

        return newNode;
    }

    // Create 1 vis edge
    // Utility function, not service function
    var createEdge = function(link) {
        if(link) {
            var newEdge = {};

            newEdge.id       = link.id;
            newEdge.from     = link.deviceA;
            newEdge.to       = link.deviceB;
            newEdge.fromPort = link.portA;
            newEdge.toPort   = link.portB;
            newEdge.fromMac  = link.macA;
            newEdge.toMac    = link.macB;
            newEdge.length   = LENGTH;

            newEdge.arrows = {
                from:{
                    status: link.statusA
                },
                to:{
                    status: link.statusB
                }
            }
            return newEdge;
        }
    }

    // Create set of vis nodes and edges by data was provided by server API
    // Utility function, not service function
    var genGraph = function(data) {

        var nodes = new vis.DataSet();
        var edges = new vis.DataSet();

        // Create set of nodes
        data.nodes.forEach(function(node) {
            var newNode = createNode(node);
            nodes.add(newNode);
        });
        // Create set of edges
        data.edges.forEach(function(link) {
            var newEdge = createEdge(link);
            edges.add(newEdge);
        })
        return {'nodes':nodes,'edges':edges};
    }

    // Get parameter on URL to retrive topoId
    var getUrlParameter = function(param, dummyPath) {
        var sPageURL = dummyPath || window.location.search.substring(1),
            sURLVariables = sPageURL.split(/[&||?]/),
            res;

        for (var i = 0; i < sURLVariables.length; i += 1) {
            var paramName = sURLVariables[i],
                sParameterName = (paramName || '').split('=');

            if (sParameterName[0] === param) {
                res = sParameterName[1];
            }
        }

        return res;
    }

    var topoId = getUrlParameter('topoId');

    // Rediscover network using IP list and community string provided before
    this.discover = function() {
        var promise = $http.get(baseUrl+'/general/discover/', {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Synchronize database between racks controller and server
    this.sync = function() {
        var promise = $http.get(baseUrl+'/general/synchronize/', {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Get network information in database (not realtime) to draw topology by topoId
    this.getNetwork = function(scope) {

        var promise = $http.get(baseUrl+'/general/detail/', {params:{'topoId':topoId}}).then(function(res) {
            if (res.data.status == 'error') {
                alert('Cannot show this topology');
            } else {
                scope.data = genGraph(res.data);
                if (scope.network) scope.network.redraw();
            }
        },function(error) {
            console.log(error);
        });
        return promise;
    };

    // Send commit database signal to server
    this.saveChange = function() {
        var promise = $http.get(baseUrl+'/general/save/').then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        });
        return promise;
    }

    // Send rollback database signal to server
    this.discardChange = function() {
        var promise = $http.get(baseUrl+'/general/discard/').then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        });
        return promise;
    }

    // Get detail about 1 node
    this.getNodeDetail = function(node) {
        var promise = $http.get(baseUrl+'/node/detail/',{params:{'node':node, 'topoId':topoId}}).then(function(res) {
            var data = res.data;
            if (data.status == 'Not found') {
                alert("Cannot find this node detail");
                return false;
            } else if (data.status == 'error') {
                alert("Error in server")
            }

            // Rearrange order of information 
            generalDetail = {
                'Name'       : data.general['Name'],
                'IP'         : data.general['IP'],
                'Location'   : data.general['Location'],
                'Description': data.general['Description'],
                'Note'       : data.general['Note'],
                'Up Time'    : data.general['Up Time'],
              }
            portDetail = data.portList;
            // Add few detail about port and type
            return {
                'general': generalDetail,
                'type'   : data['Type'],
                'manual' : !data['fixed'],
                'portLen': Object.keys(portDetail).length,
                'ports'  : portDetail
            };
        },function(error) {
            console.log(error);
        });  
        return promise;
    }

    // Post new data of node that user want to edit
    this.editNode = function(node,data) {

        var postData = {
            'node' : node,
            'data' : data
        }

        var promise = $http.post(baseUrl+'/node/edit/',JSON.stringify(postData), {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Delete node
    this.deleteNode = function(node) {
        var promise = $http.post(baseUrl+'/node/delete/',JSON.stringify({'node':node}), {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Post data of new node that user want to add to topology
    this.addNode = function(data) {
        var promise = $http.post(baseUrl+'/node/add/', JSON.stringify({'data':data}), {params:{'topoId':topoId}}).then(function(res) {
            retures.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Generate edge detail include detail about two endpoint nodes using existing data from vis data
    this.getEdgeDetail = function(scope,edge) {
        var detail = {DeviceA:{},DeviceB:{}};
        var edges  = scope.data.edges._data;
        var nodes  = scope.data.nodes._data;

        edgeDetail = edges[edge];

        detail.DeviceA.id     = nodes[edgeDetail.from].id;
        detail.DeviceA.name   = nodes[edgeDetail.from].label;
        detail.DeviceA.port   = edgeDetail.fromPort;
        detail.DeviceA.mac    = edgeDetail.fromMac;
        detail.DeviceA.status = (edgeDetail.arrows.from.status=="1")?true:false;

        detail.DeviceB.id     = nodes[edgeDetail.to].id;
        detail.DeviceB.name   = nodes[edgeDetail.to].label;
        detail.DeviceB.port   = edgeDetail.toPort;
        detail.DeviceB.mac    = edgeDetail.toMac;
        detail.DeviceB.status = (edgeDetail.arrows.to.status=="1")?true:false;

        return detail;
    }

    // Post new data of edge that user want to edit
    this.editEdge = function(edge,data) {

        var postData = {
            'edge' : edge,
            'data' : data
        }

        var promise = $http.post(baseUrl+'/edge/edit/', JSON.stringify(postData), {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Delete edge
    this.deleteEdge = function(edge) {
        var promise = $http.post(baseUrl+'/edge/delete/', JSON.stringify({'edge':edge}), {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

    // Post data of new edge that user want to add to topology
    this.addEdge = function(data) {
        var promise = $http.post(baseUrl+'/edge/add/', JSON.stringify({'data':data}), {params:{'topoId':topoId}}).then(function(res) {
            return res.data;
        },function(error) {
            console.log(error);
        })
        return promise;
    }

}]);


// Most important directive to draw topology
ngVis.directive('visNetwork', function () {
    return {
        restrict: 'EA',
        transclude: false,
        scope: {
            data   : '=',
            options: '=',
            utils  : '=',
            network: '='
        },
        link: function (scope, element, attr) {

            var network = null;

            scope.$watch('data', function () {
                // Sanity check
                if (scope.data == null) {
                    return;
                }
                // If we have actually changed the data set, then recreate the graph
                // We can always update the data by adding more data to the existing data set
                if (network != null) {
                    network.destroy();
                }

                // Create the graph2d object
                network = new vis.Network(element[0], scope.data, scope.options);
                scope.network = network;
            });

            // Update options whenever options variable has changed
            scope.$watchCollection('options', function (options) {
                if (network == null) {
                    return;
                }
                network.setOptions(options);
            });

        }
    };
});
