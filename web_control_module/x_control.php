<?php
echo "X has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "x");
fclose($out);
echo "X has been sent!";
?>
