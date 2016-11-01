<?php

	$response = [];
	$response['threads'] = rand(0, 200);
	$response['crawled'] = rand(0, 20000);
	$response['tocrawl'] = rand(0, 20000);
	$response['keywords'] = rand(0, 20000);
	$response['images'] = rand(0, 20000);
	$response['success'] = true;

	echo json_encode($response);

?>