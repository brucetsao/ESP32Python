
<?php
   	include("../comlib.php");		//使用資料庫的呼叫程式
	include("../Connections/iotcnn.php");		//使用資料庫的呼叫程式
		//	Connection() ;
  	$link=Connection();		//產生mySQL連線物件

//	if(is_array($_GET)&&count($_GET)>0)//先判断是否通过get传值了
//    {
		echo "GET DATA passed <br>" ;
        if(!isset($_GET["MAC"]))//是否存在"MAC"的参数
        {
            echo "MAC address lost <br>" ;
			die();
        }
        if(!isset($_GET["T"]))//是否存在"Temperature"的参数
        {
            echo "Temperature loss <br>" ;
			die();
        }
        if(!isset($_GET["H"]))//是否存在"humidity"的参数
        {
            echo "humidity loss <br>" ;
			die();
        }
	$temp0=$_GET["MAC"];		//取得POST參數 : MAC address
	$temp1=$_GET["T"];		//取得POST參數 : temperature
	$temp2=$_GET["H"];		//取得POST參數 : humidity		
 //  }



//	if empty(trim($temp0))//MAC 是否空白的参数
	echo "(".trim($temp0).")<br>";
	if (trim($temp0) == "")//MAC 是否空白的参数
	{
		echo "MAC Address is empty string <br>" ;
		die();
	}

//	$temp0=$_GET["MAC"];		//取得POST參數 : MAC address
//	$temp1=$_GET["T"];		//取得POST參數 : temperature
//	$temp2=$_GET["H"];		//取得POST參數 : humidity	
	$sysdt = getdataorder() ;
//	$ddt = getdataorder() ;
	//http://localhost:8888/iot/dhtdata/dhDatatadd.php?MAC=AABBCCDDEEFF&T=34&H=34
	//http://localhost:8888/bigdata/dhtdata/dhDatatadd.php?MAC=AABBCCDDEEFF&T=34&H=34
	// 主機：http://localhost:8888/
	//Http GET程式：dhtdata/dhDatatadd.php
	//傳遞的參數：MAC=AABBCCDDEEFF&T=34&H=34
		//MAC=網卡編號(需大寫)
		//T= 溫度
		//H=  濕度
		//INSERT INTO `dhtdata` (`id`, `MAC`, `crtdatetime`, `temperature`, `humidity`, `systime`) VALUES (NULL, 'AABBCCDDEEFF', current_timestamp(), '25.3', '88.9', '20221026085601');
	/*
	INSERT INTO `dhtdata` 
	(`MAC`,  `temperature`, `humidity`, `systime`) 
	VALUES 
	( 'AABBCCDDEEFF', 25.3, 88.9, '20221026085601');
	
	*/
	
	//$qrystr = "insert into big.dhtData (mac,systime,temperature,humidity) VALUES ('".$temp0."','".$sysdt."',".$temp1.",".$temp2.")"; 
	//組成新增到dhtdata資料表的SQL語法
	//          INSERT INTO `dhtData` (`id`, `MAC`, `crtdatetime`, `temperature`, `humidity`, `systime`) VALUES (NULL, '111111111111', CURRENT_TIMESTAMP, '26.8', '65', '20220318100901');
	//          INSERT INTO `dhtData` (MAC, temperature, humidity, systime) VALUES ('111111111111','26.8', '65', '20220318100901');

	//select * from dhtdata order by id desc;
//--------------
	$sqlstr = "insert into big.dhtData (MAC,temperature, humidity, systime) VALUES ( '%s', %f, %f, '%s');" ;
	$qrystr = sprintf($sqlstr ,$temp0,$temp1,$temp2,$sysdt) ;
	//使用sprintf 將 插入到dhtData 資料表的insert SQL 敘述產生出來，並回傳整個SQL敘述到變數$qrystr
	echo $qrystr ;		//印出$qrystr 內容
	echo "<br>" ;
	if (mysqli_query($link,$qrystr))		//連線的資料庫($link)，在該資料庫上執行變數$qrystr 的SQL 敘述(插入資料)
		{
				echo "Successful <br>" ;
		}
		else
		{
				echo "Fail <br>" ;
		}
			;			//執行SQL語法
	mysqli_close($link);		// 關閉連線

?>
