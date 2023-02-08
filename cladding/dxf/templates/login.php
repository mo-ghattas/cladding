<?php
$msg = "";
require_once '../core/Manager.php';
$manager = Manager::getInstance();
$userService = $manager->getService("userService");
if ($userService->isSessionOn()) {
    header("Location: index.php");
    die();
}
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset($_POST['username']) || !isset($_POST["password"])) {
        header("Location: viewJob.php?jobID={$result}");
        die();
    }

    $result = $userService->login($_POST);
    if ($result) {
        header("Location: index.php");
    }
    $msg = "Wrong username or password";

}

$login = true;
require '../templates/header.php';

?>

<div class="navbar">
    <ul class="navbar-nav ml-auto">
        <li class="nav-item d-flex align-items-center mr-2 localization-icons">
        </li>
    </ul>
</div>


<div class="col-md-8 col-lg-6 col-xl-5 mx-auto" style="margin-top: 0; margin-bottom: 10%;">

    <h3 class="text-center">
        <img src="../assets/img/dome.png">
    </h3>

    <div class="card mt-5">
        <div class="card-body pt-4">

            <div class="px-4 pb-3">
                <!-- start: Login Form -->
                <div class="form-wrapper active" id="login">
                    <h6 class="text-uppercase mb-5 mt-3">
                        Login </h6>
                    <span class="text-danger"> <?= $msg ?></span>
                    <form class="form" method="post" action="#">
                        <!-- start: Username -->
                        <div class="form-group">
                            <label for="login-username">
                                Username </label>
                            <input type="text" name="username" class="form-control">
                        </div>
                        <!-- end: Username -->

                        <!-- start: Password -->
                        <div class="form-group">
                            <label>
                                Password </label>
                            <input type="password" name="password" class="form-control">
                        </div>
                        <!-- end: Password -->


                        <button type="submit" id="btn-login" class="btn btn-success mt-5 btn-block btn-lg"
                                data-loading-text="Logging in...">
                            Login
                        </button>
                    </form>
                </div>
                <!-- end: Login Form -->


            </div>
        </div>
    </div>


    <div class="text-center text-muted mt-3 sign-in-controls" style="display: none;">
        Already have an account? <a href="#login" class="form-change">Login</a>
    </div>
</div>

</div>
<!--Modal: Terms-->
<div class="modal fade" id="Terms" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">

        <!--Content-->
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title" id="myModalLabel"></h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <!--Body-->
            <div class="modal-body mb-0 p-0">

                <div class="d-flex justify-content-center align-items-center-center p-5">
                    <div class="embed-responsive embed-responsive-21by9 z-depth-1-half">

                    </div>
                </div>
            </div>

            <!--Footer-->
            <div class="modal-footer justify-content-end">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>

            </div>

        </div>
        <!--/.Content-->

    </div>

