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
});
