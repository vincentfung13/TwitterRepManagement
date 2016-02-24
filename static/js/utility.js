/**
 * Created by vincentfung13 on 24/02/2016.
 */
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