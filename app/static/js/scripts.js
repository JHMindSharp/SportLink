$(document).ready(function() {
    var isConnected = {{ current_user.is_authenticated|tojson }};

    function updateUserButtons() {
        if (isConnected) {
            $("#signup-button, #login-button").hide();
            $("#logout-button, #profile-info").show();
        } else {
            $("#signup-button, #login-button").show();
            $("#logout-button, #profile-info").hide();
        }
    }

    updateUserButtons();

    $("#signup-button").click(function() {
        $('html, body').animate({
            scrollTop: $("#signup-section").offset().top
        }, 1000, function() {
            $("#signup-form").show();
            $("#login-form").hide();
            $("#signup-title").text("Inscrivez-vous maintenant !");
            $("#signup-button").addClass('active');
            $("#login-button").removeClass('active');
        });
    });

    $("#login-button").click(function() {
        $('html, body').animate({
            scrollTop: $("#signup-section").offset().top
        }, 1000, function() {
            $("#signup-form").hide();
            $("#login-form").show();
            $("#signup-title").text("Connecte-toi vite !");
            $("#signup-button").removeClass('active');
            $("#login-button").addClass('active');
        });
    });

    $("#logout-button").click(function() {
        window.location.href = '{{ url_for("logout") }}';
    });

    $("#signup-form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "{{ url_for('register') }}",
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    isConnected = true;
                    updateUserButtons();
                    alert("Registration successful! You are now logged in.");
                    window.location.href = "{{ url_for('profile') }}";
                } else {
                    alert("Registration failed: " + response.message);
                }
            },
            error: function() {
                alert("An error occurred while registering. Please try again.");
            }
        });
    });

    $("#login-form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "{{ url_for('login') }}",
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    isConnected = true;
                    updateUserButtons();
                    alert("Login successful!");
                    window.location.href = "{{ url_for('profile') }}";
                } else {
                    alert("Login failed: " + response.message);
                }
            },
            error: function() {
                alert("An error occurred while logging in. Please try again.");
            }
        });
    });

    $("#logo").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        $(".page-section").hide();
        $("#home").show();
    });

    $(".expandable").mouseenter(function() {
        var sectionId = $(this).data("section");
        var $infoBubble = $("#" + sectionId);
        $infoBubble.stop(true, true).fadeIn(500);
    }).mouseleave(function() {
        var sectionId = $(this).data("section");
        var $infoBubble = $("#" + sectionId);
        $infoBubble.stop(true, true).fadeOut(500);
    });

    $(".nav-link").click(function(e) {
        e.preventDefault();
        var targetSection = $(this).attr('href').substring(1);
        $(".page-section").hide();
        $("#" + targetSection).show();
    });

    $("#home").show();

    function loadUserProfile() {
        var user = {
            username: "{{ current_user.username }}",
            age: 25,
            region: "Île-de-France",
            profilePic: "{{ url_for('static', filename='images/default-profile.png') }}",
            posts: [
                "Publication 1: Lorem ipsum dolor sit amet.",
                "Publication 2: Consectetur adipiscing elit.",
                "Publication 3: Integer nec odio. Praesent libero."
            ]
        };

        $("#username").text(user.username);
        $("#user-age-region").text(user.age + ", " + user.region);
        $("#profile-pic").attr("src", user.profilePic);

        var postsContainer = $("#posts-container");
        postsContainer.empty();
        user.posts.forEach(function(post) {
            var postElement = $("<div class='post'></div>").text(post);
            postsContainer.append(postElement);
        });
    }

    $(".nav-link[href='#profile']").click(function() {
        loadUserProfile();
    });
});
