<?php
require '../core/Manager.php';
$manager = Manager::getInstance();
$userService = $manager->getService("userService");
if (!$userService->isSessionOn()) {
    Utils::sendLogin();
    exit();
}
$userID = $userService->getUserID();
$jobService = $manager->getService("jobHandler");
$jobs = $jobService->getUserJobs($userID, 5);
$uiService = $manager->getService("ui");
$uiService->setCurrentActiveWindow("Home");
$totalJobs = $jobService->getTotalJobs($userID);
$totalParts = $jobService->getTotalParts($userID);
$totalDistance = $jobService->getTotalArea($userID);
require '../templates/header.php';
require '../templates/sidebar.php';

?>
<style>
    tr {
        cursor: pointer;
    }
</style>
<link rel="stylesheet" href="../assets/css/dataTables.bootstrap.css"/>
<div class="col-md-9 col-lg-10">

    <div class="row">
        <div class="col-xl-4 col-md-8 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Total Jobs
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?= $totalJobs ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-briefcase fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-xl-4 col-md-8 mb-4">
            <div class="card border-left-secondary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Total Parts
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?= $totalParts; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas  fa-building fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-xl-4 col-md-8 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Total Area
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?= $totalDistance; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="fas  fa-building fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="jobs">
        <hr>
        <div style="margin-bottom: 1.3rem">
            <a class="btn btn-success d-block d-sm-inline-block"
               href="newJob.php">
                <i class="fa fa-plus"></i>
                New Job
            </a>
        </div>
        <h2 class="display-4" style="margin-top:0.8rem;">Latest 5 Jobs</h2>
        <div class="col-sm-12 table-responsive">
            <table class="table table-striped w-100" id="jobs-list">
                <thead>
                <tr>
                    <th>Job Number</th>
                    <th>Date</th>
                    <th>Project</th>
                    <th>client</th>
                    <th>State</th>
                </tr>
                </thead>
                <tbody>
                <?php
                foreach ($jobs as $job) {
                    echo "<tr role=\"row\" dms='{$job['jobID']}'>";
                    echo "<td>{$job["JobNo"]}</td>";
                    echo "<td> {$job["date"]}</td>";
                    echo "<td>{$job["project"]} </td>";
                    echo "<td>{$job["client"]} </td>";
                    $state = $uiService->getStatueForJob((int)$job["state"]);
                    echo "<td> {$state}</td>";
                }
                ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php include '../templates/footer.php'; ?>
<script>
    $(document).ready(function () {
        let table = $('#jobs-list').DataTable({searching: false, paging: false, info: false});

        table.on('click', 'tbody tr', function () {
            let jobID = $(this).attr("dms");
            window.location.href = `viewJob.php?jobID=${jobID}`;
        })
    });

</script>

</body>
</html>

