<?php
echo "J has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "j");
fclose($out);
echo "J has been sent!";
?>
