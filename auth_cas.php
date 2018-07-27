<?php
	
ini_set('display_errors', 1);
require_once 'CAS.php';

// Enable debugging
phpCAS::setDebug();
// Enable verbose error messages. Disable in production!
phpCAS::setVerbose(true);

$cas_host = "login.umd.edu";
$cas_port = 443;
$cas_context = "/cas";

phpCAS::client(CAS_VERSION_3_0, $cas_host, $cas_port, $cas_context);
// phpCAS::setFixedServiceURL("https://cmsc828t.cs.umd.edu");
phpCAS::setServerServiceValidateURL("https://login.umd.edu/cas/serviceValidate");
phpCAS::setNoCasServerValidation();
phpCAS::forceAuthentication();

if ( phpCAS::checkAuthentication() ) {
	$username = phpCAS::getUser();
}
else {
	$username = "No username";
}

if (isset($_REQUEST['logout'])) {
	phpCAS::logoutWithRedirectService('https://cmsc828t.cs.umd.edu');
}

?>