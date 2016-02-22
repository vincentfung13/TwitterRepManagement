/**
 * Created by vincentfung13 on 22/02/2016.
 */
$(document).ready(function() {
    $('#id_date')
        .datepicker({
            format: 'yyyy-mm-dd'
        })
        .on('changeDate', function(e) {
            // Revalidate the date field
            $('#eventForm').formValidation('revalidateField', 'date');
        });

    //$('#eventForm').formValidation({
    //    framework: 'bootstrap',
    //    icon: {
    //        valid: 'glyphicon glyphicon-ok',
    //        invalid: 'glyphicon glyphicon-remove',
    //        validating: 'glyphicon glyphicon-refresh'
    //    },
    //    fields: {
    //        name: {
    //            validators: {
    //                notEmpty: {
    //                    message: 'The name is required'
    //                }
    //            }
    //        },
    //        date: {
    //            validators: {
    //                notEmpty: {
    //                    message: 'The date is required'
    //                },
    //                date: {
    //                    format: 'MM/DD/YYYY',
    //                    message: 'The date is not a valid'
    //                }
    //            }
    //        }
    //    }
    //});
});
