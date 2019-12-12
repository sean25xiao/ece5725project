<?php
echo "S has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "s");
fclose($out);
echo "S has been sent!";
?>
