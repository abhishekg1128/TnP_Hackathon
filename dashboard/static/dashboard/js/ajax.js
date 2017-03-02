/**
 * Created by sharvil on 22/1/17.
 */
$("a[data-target=#my-modal]").click(function (event) {
    event.preventDefault();
    var target = $(this).attr("href");
    $("#my-modal .modal-body").load(target, function () {
        $("#my-modal").modal("show");
    })
})