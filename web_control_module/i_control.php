<?php
echo "I has been pressed! \n";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "i");
fclose($out);
echo "I has been sent!";
?>
