<?php
echo "A has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "a");
fclose($out);
echo "A has been sent!";
?>
