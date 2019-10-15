var test = true;

var code_message = {
    0: "Success!",
    1: "Invalid Data",
    100: "Restaurant not found.",
    101: "Restaurants with the same name and branch exist.",
    200: "Tag not found",
    201: "Tags with the same name exist."
};

function show_message(show, type, title, content)
{
    message.$data["show"] = show;
    message.$data["type"] = type;
    message.$data["title"] = title;
    message.$data["content"] = content;
    if (show)
        $('html,body').animate({scrollTop: 0}, 500);
}

function handle_error(error)
{
    if (typeof(error) === "number")
        show_message(true, "alert-danger", "Erorr", code_message[error]);
    else
        show_message(true, "alert-danger", "Error", "Server returned " + error.status + ".");
}

function go_back()
{
    !window.history.length ? window.history.go(-1):window.location.href='/find_restaurant';
}

function ajax(url, obj, success)
{
    $.ajax({
        url: url,
        type: "POST",
        contentType: "application/json;charset=utf-8;",
        data: JSON.stringify(obj),
        dataType: "json",
        success: function (data)
        {
            if (!data["code"])
                success(data["res"]);
            else
                handle_error(data["code"]);
        },
        error: function (error) {handle_error(error);}
    });
}