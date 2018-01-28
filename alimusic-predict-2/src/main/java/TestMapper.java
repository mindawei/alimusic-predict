

import java.io.IOException;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

public class TestMapper extends MapperBase{
	  Record key;
	  Record value;
	  @Override
	  public void setup(TaskContext context) throws IOException {
		key = context.createMapOutputKeyRecord();
		value = context.createMapOutputValueRecord();
	  }
	  @Override
	  public void map(long recordNum, Record record, TaskContext context)
		throws IOException {
		  //artist_id,user_id,song_id,gmt_create,Ds
		key.set("artist_id", record.getString(0));
		value.set("user_id", record.getString(1));
		value.set("song_id", record.getString(2));
		value.set("gmt_create", record.getString(3));
		key.set("Ds", record.getString(4));
		context.write(key, value);
	  }
}