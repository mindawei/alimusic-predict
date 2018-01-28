

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class TestDriver {
	  public static void main (String[] args) throws OdpsException {
	    JobConf job = new JobConf();
		// TODO: specify map output types
	    //  key: artist_id,Ds
	    //  value: user_id,song_id,gmt_create
		job.setMapOutputKeySchema(SchemaUtils.fromString("artist_id:string,Ds:string"));
		job.setMapOutputValueSchema(SchemaUtils.fromString("user_id:string,song_id:string,gmt_create:string"));
		// TODO: specify input and output tables
		InputUtils.addTable(TableInfo.builder().tableName(args[0]).build(),job);
		OutputUtils.addTable(TableInfo.builder().tableName(args[1]).build(),job);
		// TODO: specify a mapper
		job.setMapperClass(TestMapper.class);
		job.setReducerClass(TestReducer.class);
		RunningJob rj = JobClient.runJob(job);
		rj.waitForCompletion();
	  }
}