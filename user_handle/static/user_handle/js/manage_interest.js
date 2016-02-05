/**
 * Created by vincentfung13 on 04/02/2016.
 */
function tag_manager_setup(list, username) {
    var myApp = angular.module('myApp', [])
        .directive('tagManager', function () {
            return {
                restrict: 'E',

                scope: {
                    tags: '=',
                    autocomplete: '=autocomplete'
                },

                template: '<div class="tags">' +
                '<div ng-repeat="(idx, tag) in tags" class="tag label label-success">{{tag}} <a class="close" href ng-click="remove(idx)">×</a></div>' +
                '</div>' +
                '<div class="input-group"><input type="text" class="form-control" placeholder="add an entity..." ng-model="newValue" /> ' +
                '<span class="input-group-btn"><a class="btn btn-default" ng-click="add()">Add</a></span></div>',

                link: function ($scope, $element) {

                    var input = angular.element($element).find('input');

                    //// setup autocomplete
                    //if ($scope.autocomplete) {
                    //  $scope.autocompleteFocus = function(event, ui) {
                    //    input.val(ui.item.value);
                    //    return false;
                    //  };
                    //  $scope.autocompleteSelect = function(event, ui) {
                    //    $scope.newValue = ui.item.value;
                    //    $scope.$apply( $scope.add );
                    //
                    //    return false;
                    //  };
                    //  $($element).find('input').autocomplete({
                    //        minLength: 0,
                    //        source: function(request, response) {
                    //          var item;
                    //          return response((function() {
                    //            var _i, _len, _ref, _results;
                    //            _ref = $scope.autocomplete;
                    //            _results = [];
                    //            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                    //              item = _ref[_i];
                    //              if (item.toLowerCase().indexOf(request.term.toLowerCase()) !== -1) {
                    //                _results.push(item);
                    //              }
                    //            }
                    //            return _results;
                    //          })());
                    //        },
                    //        focus: (function(_this) {
                    //          return function(event, ui) {
                    //            return $scope.autocompleteFocus(event, ui);
                    //          };
                    //        })(this),
                    //        select: (function(_this) {
                    //          return function(event, ui) {
                    //            return $scope.autocompleteSelect(event, ui);
                    //          };
                    //        })(this)
                    //      });
                    //}


                    // adds the new tag to the array
                    $scope.add = function () {
                        // if not dupe, add it
                        if ($scope.tags.indexOf($scope.newValue) == -1) {
                            $scope.tags.push($scope.newValue);
                            post('/user_handle/interest/', {entity: $scope.newValue, username: username, action: 'add'});
                        }
                        $scope.newValue = "";
                    };

                    // remove an item
                    $scope.remove = function (idx) {
                        if ($.inArray($scope.tags[idx], $scope.allTags) == -1){
                            console.log($scope.tags[idx]);
                            post('/user_handle/interest/', {entity: $scope.tags[idx], username: username, action: 'remove'});
                        }
                        $scope.tags.splice(idx, 1);
                    };

                    // capture keypresses
                    input.bind('keypress', function (event) {
                        if (event.keyCode == 13) {
                            $scope.$apply($scope.add);
                        }
                    });
                }
            };
        })

        .controller('tagsCtrl', function ($scope) {
            $scope.tags = list;
            $scope.allTags = ['Apple', 'Amazon', 'Tesco', 'BMW', 'HSBC', 'Heineken'];
        });
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    var csrf_token = document.getElementById('csrf_token').value;
    var csrf_token_field = document.createElement('input');
    csrf_token_field.setAttribute('type', 'hidden');
    csrf_token_field.setAttribute('name', 'csrfmiddlewaretoken');
    csrf_token_field.setAttribute('value', csrf_token);
    form.appendChild(csrf_token_field);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}