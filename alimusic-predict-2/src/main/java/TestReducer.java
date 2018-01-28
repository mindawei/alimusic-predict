
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

public class TestReducer extends ReducerBase{
	
  Record output;
  @Override
  public void setup(TaskContext context) throws IOException {
	output = context.createOutputRecord();
  }
  
//	key.set("artist_id", record.getString(0));
//	key.set("Ds", record.getString(4));  
//	value.set("user_id", record.getString(1));
//	value.set("song_id", record.getString(2));  歌曲名称不用考虑，只考虑一个小时内某个听众听某个艺人的歌曲数不多于16首的
//	value.set("gmt_create", record.getString(3));

  @Override
  public void reduce(Record key, Iterator<Record> values, TaskContext context)
	throws IOException {
	  
	// user_id,gmt_create,num
	Map<String,Map<String,Integer>> playCounter = new HashMap<String,Map<String,Integer>>();
	
	while (values.hasNext()) {
	  Record val = values.next();
	  String user = val.getString("user_id");
	  String hour = val.getString("gmt_create");
	  
	  if(!playCounter.containsKey(user)){
		  playCounter.put(user, new HashMap<String,Integer>());
	  }
	  // 获得已有的计数
	  int num = playCounter.get(user).containsKey(hour)?playCounter.get(user).get(hour):0;
	  num+=1;
	  playCounter.get(user).put(hour,num);

	}
	
	int max_num_per_hour = 16;
	long Plays = 0;
	for(String user : playCounter.keySet()){
		for(String hour:playCounter.get(user).keySet()){
			int num = playCounter.get(user).get(hour);
			num = Math.min(num, max_num_per_hour);
			Plays+=num;
		}
	}
	
//	output.set(0, key.getString("artist_id"));
//	output.set(1, key.getString("Ds"));
	output.set(0, Plays);
	
	context.write(key,output);
  }
}