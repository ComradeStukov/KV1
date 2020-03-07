// Result code and message
var code_message = {
    0: "Success!",
    1: "Invalid Data!",
    100: "Restaurant not found!",
    101: "Restaurants with the same name and branch exist!",
    150: "Coordinate of the postcode not found!",
    200: "Tag not found!",
    201: "Tags with the same name exist!",
    300: "Cart is empty!",
};

/**
 * Handle an error
 * @param error The error object or result code
 */
function handle_error(error)
{
    // If it is a result code, show the code and the message
    // Else, show the status code
    if (typeof(error) === "number")
        show_message(true, "alert-danger", "Error!", code_message[error]);
    else
        show_message(true, "alert-danger", "Error!", "Server returned error code: " + error.status + "!");
}

/**
 * Go back to a particular position in the history
 * @param page
 */
function go_back(page=1)
{
    // Use window.history to find the page and go back
    window.history.length >= page ? window.history.go(-page) : window.location.href='find_restaurants';
}

/**
 * Invoke an ajax request
 * @param url The specified url
 * @param obj The object which will be encoded as JSON
 * @param success Callback function when the request succeeded
 */
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
            // Use the callback function when succeeded
            // Else use the error handling function
            if (!data["code"])
                success(data["res"]);
            else
                handle_error(data["code"]);
        },
        error: function (error) {handle_error(error);},
        xhrFields: {withCredentials: false},
        crossDomain: false
    });
}
