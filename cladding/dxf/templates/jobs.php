<?php
require '../core/Manager.php';
$manager = Manager::getInstance();
$userService = $manager->getService("userService");
$uiService = $manager->getService("ui");
$uiService->setCurrentActiveWindow("Jobs");
if (!$userService->isSessionOn()) {
    Utils::sendLogin();
}
$userID = $userService->getUserID();
$jobService = $manager->getService("jobHandler");
$jobs = $jobService->getUserJobs($userID);
$totalJobs = count($jobs);

require '../templates/header.php';
require '../templates/sidebar.php';
?>
<link rel="stylesheet" href="../assets/css/dataTables.bootstrap.css"/>
<style>
    tr{
        cursor:pointer;
    }
</style>
<div class="col-md-9 col-lg-10">

    <div style="margin-bottom: 1.3rem">
        <a class="btn btn-success d-block d-sm-inline-block"
           href="newJob.php">
            <i class="fa fa-plus"></i>
            New Job
        </a>
    </div>
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
<?php include '../templates/footer.php'; ?>
<script>
    $(document).ready(function () {
        let tableHTML = $('#jobs-list').DataTable();

        $('#jobs-list').on('click', 'tbody tr', function () {
            let jobID = $(this).attr("dms");
            window.location.href = `viewJob.php?jobID=${jobID}`;
        })
    });

</script>

</body>
</html>
