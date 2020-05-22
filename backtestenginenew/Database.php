<?php
class Database {

    protected $connection = null;
    private $debug = true;
    private $stmt = null;
    private $insertid = null;
    private $affectedrows = null;

    public function connection() {
        // we don't need to connect twice
        if ( $this->connection ) {
            return $this->connection;
        }

        //sqlsrv_configure('WarningsReturnAsErrors', 0);

        // data for making connection            
        $sqlsvr_details =   array(  'UID'   => 'sa',
                                    'PWD'           => 'f0r3z@786',
                                    'Database'      => 'FDS_Datafeeds',
                                    'CharacterSet'  => 'UTF-8'
                                );

        // try to connect                    
        $this->connection = sqlsrv_connect("INDXX", $sqlsvr_details);

        if($this->connection == false){
            $this->debug('Failed to connect to host: '.$this->errors(),true);
            return false;
        }else{
            return true;
        }
    }

    public function query($query) {
	$resultset = new resultset($query,$this->connection,$this->debug);		
    

	return $resultset->asObject();

	
    }

    private function debug ($message,$hard = false){
        if ($this->debug){
            if ($hard){
                die($message);
            }else{
                echo $message;
            }
        }

        return true;
    }

public function deleteInfo($query){
    return $this->update($query);   
}

public function updateInfo($query){
    //Not happy with this
    $this->affectedrows = null;
    $this->insertid = null;

    $this->stmt = sqlsrv_query($this->connection, $query);

    if (!$this->stmt){
        $this->debug('SQL Query Failed: '.$query.' '.$this->errors(),true);
        return false;
    }else{
        $this->affectedrows = @sqlsrv_rows_affected($this->stmt);
        return $this;   
    }
}

public function insertInfo($query){
    //Not happy with this
    $this->affectedrows = null;
    $this->insertid = null;

    $this->stmt = sqlsrv_query($this->connection, $query);

    if (!$this->stmt){
        $this->debug('SQL Query Failed: '.$query.' '.$this->errors(),true);
        return false;
    }else{
        //Get the last insert ID and store it on here
        $this->insertid = $this->query('select @@IDENTITY as insert_id')->asObject()->insert_id;
        return $this;   
    }
}

public function insert_id(){
    return $this->insertid;
}

public function affected_rows(){
    return $this->affectedrows; 
}

private function errors(){
    return print_r( sqlsrv_errors(SQLSRV_ERR_ERRORS), true);
}

}

class resultset implements Countable,Iterator {

    private $result = null;
    private $connection = null;
    private $debug = false;
    private $internal_pointer = 0;
    private $data = array();

    public function resultset($query,$link,$debug = false){ 
        $this->connection = $link;
        $this->debug = $debug;

        $this->result = sqlsrv_query($this->connection, $query, array(),  array('Scrollable' => SQLSRV_CURSOR_STATIC));

        if ($this->result == false){
            $this->debug('Query Failed: '.$query.' '.$this->errors(),true);
            return false;
        }else{
            return $this;
        }
    }

    public function asObject($step = true){
        $object = sqlsrv_fetch_object($this->result,NULL,NULL,SQLSRV_SCROLL_ABSOLUTE,$this->internal_pointer);
        if (! $object){
            return false;
        }else{
            if ($step) $this->internal_pointer++;
            return $object; 
        }

    }
	
	public function getAllData($step = true){
		$ReturnArr = array();
		$record = sqlsrv_fetch_array( $this->result, SQLSRV_FETCH_ASSOC);
		echo "ssssssssssssssss";die;
       // $object = sqlsrv_fetch_object($this->result,NULL,NULL,SQLSRV_SCROLL_ABSOLUTE,$this->internal_pointer);
        while( $record = sqlsrv_fetch_array( $this->result, SQLSRV_FETCH_ASSOC) ) {
			 $ReturnArr[] =  $record;
		}
		return  $ReturnArr;

    }

    public function num_rows() {
        return sqlsrv_num_rows($this->result);
    }

    public function free(){
        $this->internal_pointer = 0;

        if (is_resource($this->result)){
            sqlsrv_free_stmt($this->result);
        }   
    }

    public function __destory(){
        $this->free();
    }

        //Countable Function

    public function count(){
        return $this->num_rows();   
    }

    //Iteration Functions

    public function rewind(){
        $this->internal_pointer = 0;    
    }

    public function current(){
        return $this->asObject(false);
    }

    public function key(){
        return $this->internal_pointer;
    }

    public function next(){
        $this->internal_pointer++;
    }

    public function valid(){
        return $this->internal_pointer <= $this->num_rows();    
    }

    //============================================

    private function debug ($message,$hard = false){
        if ($this->debug){
            if ($hard){
                die($message);
            }else{
                echo $message;
            }
        }

        return true;
    }

    private function errors(){
        return print_r( sqlsrv_errors(SQLSRV_ERR_ERRORS), true);
    }
	function createDateRangeArray($strDateFrom,$strDateTo)
{
    // takes two dates formatted as YYYY-MM-DD and creates an
    // inclusive array of the dates between the from and to dates.

    // could test validity of dates here but I'm already doing
    // that in the main script

    $aryRange=array();

    $iDateFrom=mktime(1,0,0,substr($strDateFrom,5,2),     substr($strDateFrom,8,2),substr($strDateFrom,0,4));
    $iDateTo=mktime(1,0,0,substr($strDateTo,5,2),     substr($strDateTo,8,2),substr($strDateTo,0,4));

    if ($iDateTo>=$iDateFrom)
    {
        array_push($aryRange,date('Y-m-d',$iDateFrom)); // first entry
        while ($iDateFrom<$iDateTo)
        {
            $iDateFrom+=86400; // add 24 hours
            array_push($aryRange,date('Y-m-d',$iDateFrom));
        }
    }
    return $aryRange;
}
	
	
	
}
?>