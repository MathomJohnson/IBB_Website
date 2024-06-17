(function($) {

	"use strict";

	// Setup the calendar with the current date
$(document).ready(function(){
    var date = new Date();
    var today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({date: date}, next_year);
    $(".left-button").click({date: date}, prev_year);
    $(".month").click({date: date}, month_click);
    $("#add-button").click({date: date}, new_event);
    // Set current month as active
    $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
    var events = check_events(today, date.getMonth()+1, date.getFullYear());
    show_events(events, months[date.getMonth()], today, date.getFullYear());
});

// Initialize the calendar by appending the HTML dates
function init_calendar(date) {
    $(".tbody").empty();
    $(".events-container").empty();
    var calendar_days = $(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");
    var today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    var first_day = date.getDay();
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for(var i=0; i<35+first_day; i++) {
        // Since some of the elements will be blank, 
        // need to calculate actual date from index
        var day = i-first_day+1;
        // If it is a sunday, make a new row
        if(i%7===0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        // if current index isn't a day in this month, make it blank
        if(i < first_day || day > day_count) {
            var curr_date = $("<td class='table-date nil'>"+"</td>");
            row.append(curr_date);
        }   
        else {
            var curr_date = $("<td class='table-date'>"+day+"</td>");
            var events = check_events(day, month+1, year);
            if(today===day && $(".active-date").length===0) {
                curr_date.addClass("active-date");
                show_events(events, months[month], day, year);
            }
            // If this date has any events, style it with .event-date
            if(events.length!==0) {
                curr_date.addClass("event-date");
            }
            // Set onClick handler for clicking a date
            curr_date.click({events: events, month: months[month], day:day}, date_click);
            row.append(curr_date);
        }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
}

// Get the number of days in a given month/year
function days_in_month(month, year) {
    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);    
}

// Event handler for when a date is clicked
function date_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    show_events(event.data.events, event.data.month, event.data.day, event.data.year);
};

// Event handler for when a month is clicked
function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    var date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    var new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

// Event handler for when the year right-button is clicked
function next_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()+1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for when the year left-button is clicked
function prev_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()-1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for clicking the new event button
function new_event(event) {
    // if a date isn't selected then do nothing
    if($(".active-date").length===0)
        return;
    // remove red error input on click
    $("input").click(function(){
        $(this).removeClass("error-input");
    })
    // empty inputs and hide events
    $("#dialog input[type=text]").val('');
    $("#dialog input[type=number]").val('');
    $(".events-container").hide(250);
    $("#dialog").show(250);
    // Event handler for cancel button
    $("#cancel-button").click(function() {
        $("#name").removeClass("error-input");
        $("#start-time").removeClass("error-input");//used to be #time-slot
        $("#dialog").hide(250);
        $(".events-container").show(250);
    });
    // Event handler for ok button
    $("#ok-button").unbind().click({date: event.data.date}, function() {
        var date = event.data.date;
        var name = $("#name").val().trim();
        var start_time = $("#start-time").val();
        var day = parseInt($(".active-date").html());
        // Basic form validation
        if(name.length === 0) {
            $("#name").addClass("error-input");
        }
        else if(start_time.length === 0) {
            $("#start-time").addClass("error-input");
        }
        else {
            $("#dialog").hide(250);
            console.log("new event");
            new_event_json(name, start_time, date, day);
            date.setDate(day);
            init_calendar(date);
        }
    });
}

// Adds a json event to event_data
function new_event_json(name, start_time, date, day) {
    var event = {
        "occasion": name,
        "start_time": start_time,
        "year": date.getFullYear(),
        "month": date.getMonth()+1,
        "day": day
    };

    $.ajax({
        url: '/calendar/add-event/',
        method: 'POST',
        data: JSON.stringify(event),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token in the headers
        },
        success: function(response) {
            if (response.status === 'success') {
                //event_data["events"].push(event);  // Optionally, update local event_data to reflect the new event
                init_calendar(date);  // Reinitialize calendar with updated events
            } else {
                alert('Failed to add event');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred while adding the event');
        }
    });
    //event_data["events"].push(event);
}

// Function to get the CSRF token from the cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Display all events of the selected date in card views
function show_events(events, month, day, year) {
    // Clear the dates container
    $(".events-container").empty();
    $(".events-container").show(250);
    console.log(event_data["events"]);
    
    // If there are no events for this date, notify the user
    if(events.length===0) {
        var event_card = $("<div class='event-card'></div>");
        var event_name = $("<div class='event-name'>There are no events planned for "+month+" "+day+".</div>");
        $(event_card).css({ "border-left": "10px solid #FF1744" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);
    }
    else {
        // Go through and add each event as a card to the events container
        for(var i=0; i<events.length; i++) {
            console.log("event#: " + events[i].id)
            // Convert the 24 clock to the 12 hour clock time
            let time = events[i]["time"];
            let parts = time.split(':');
            let hour = parseInt(parts[0], 10);  // Convert hour part to integer
            let minute = parts[1];
            let period = "AM";
            if (hour >= 12) {
              period = "PM";
              if (hour > 12) {
                hour = hour - 12;
              }
            } else if (hour === 0) {
              hour = 12;
            }
            let newTime = hour + ":" + minute + " " + period;

            var event_card = $("<div class='event-card'></div>");
            var event_name = $("<div class='event-name' style='margin-right: 8px;'><b>Mentor:</b> "+events[i]["mentor"]+"</div>");
            var event_start = $("<div class='event-count'><b>Time:</b> "+newTime+"</div>");
            var meet_button = $("<button type='button' class='meet-button btn btn-primary' data-bs-toggle='modal' data-bs-target='#meetModal' data-mentor-name='"+events[i]["mentor"]+"' data-event-id='"+events[i].id+"'>Meet</button>");

            // Delete Event Handler only displays if user is staff
            if (auth === "True") {
                var event_delete_button = $("<button class='meet-button delete-event-button btn btn-danger' data-event-id='"+ events[i].id +"'>Delete</button>");
                // Add click event handler for the delete button
                event_delete_button.on("click", function() {
                    console.log("is authenticated: " + typeof auth)
                    var button = $(this);
                    console.log($(this));
                    var eventId = $(this).data('event-id');
                    console.log("event id is: " + eventId)
                    $.ajax({
                        url: "/calendar/delete-event/",  // URL to send the request to
                        method: "POST",
                        data: {
                            event_id: eventId,
                        },
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token in the headers
                        },
                        success: function(response) {
                            if (response.success) {

                                var date = new Date(events[0].year, months.indexOf(month), day);
                                
                                // Remove the event card from the DOM
                                button.closest('.event-card').remove();
                                console.log("date is:" + date)

                                init_calendar(date);
                                //event_card.remove();
                            } else {
                                alert("Failed to delete the event.");
                            }
                        },
                        error: function(xhr, status, error) {
                            alert("An error occurred while trying to delete the event.");
                        }
                    });
                });    
            }

            if(events[i]["cancelled"]===true) {
                $(event_card).css({
                    "border-left": "10px solid #FF1744"
                });
                event_count = $("<div class='event-cancelled'>Cancelled</div>");
            }
            if (auth === "True") {
                $(event_card).append(event_name).append(event_start).append(event_delete_button);
            } else {
                $(event_card).append(event_name).append(event_start).append(meet_button);
            }
            $(".events-container").append(event_card);
        }
    }
}

// Checks if a specific date has any events
function check_events(day, month, year) {
    var events = [];
    $.ajax({
        url: '/calendar/get-events/',
        method: 'GET',
        data: {
            year: year,
            month: month,
            day: day
        },
        async: false,  // Synchronous request to ensure events are loaded before continuing
        success: function(response) {
            if (response.status === 'success') {
                events = response.events;
            } else {
                alert('Failed to load events');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred while loading the events');
        }
    });
    return events;
}

// Given data for events in JSON format
var event_data = {
    "events": [
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
        {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10
    },
        {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10,
        "cancelled": true
    },
    {
        "occasion": " Repeated Test Event ",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 10
    },
    {
        "occasion": " Test Event",
        "start_time": " 2:20 - 2:50 ",
        "year": 2020,
        "month": 5,
        "day": 11
    }
    ]
};

const months = [ 
    "January", 
    "February", 
    "March", 
    "April", 
    "May", 
    "June", 
    "July", 
    "August", 
    "September", 
    "October", 
    "November", 
    "December" 
];

})(jQuery);
