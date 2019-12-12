<?php
echo "D has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "d");
fclose($out);
echo "D has been sent!";
?>
