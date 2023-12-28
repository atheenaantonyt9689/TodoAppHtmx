window.onload = function () {
    bootlint.showLintReportForCurrentDocument([], {
        hasProblems: false,
        problemFree: false
    });

    $('[data-toggle="tooltip"]').tooltip()
    console.log("Hello World");

    /*function formatDate(date) {
        return (
            date.getDate() +
            "/" +
            (date.getMonth() + 1) +
            "/" +
            date.getFullYear()
        );
    }*/

    function formatDate(date) {
        return (
             date.getFullYear() +
            "-" +
            (date.getMonth() + 1) +
            "-" +
            date.getDate()

        );
    }

    var currentDate = formatDate(new Date());

    $(".due-date-button").datepicker({
        format: "YYYY-MM-DD",
        autoclose: true,
        todayHighlight: true,
        startDate: currentDate,
        orientation: "bottom right"
    });

    // var date = new Date();

    $(".due-date-button").on("click", function (event) {
        $(".due-date-button")
            .datepicker("show")
            .on("changeDate", function (dateChangeEvent) {
                $(".due-date-button").datepicker("hide");
                $(".due-date-label").text(formatDate(dateChangeEvent.date));
            //     set value of hidden_due_date to the date selected
                $("#due_date").val(formatDate(dateChangeEvent.date));
               //  show the due-date-label
               $('.due-date-label').removeClass('d-none');
            });
    });
};