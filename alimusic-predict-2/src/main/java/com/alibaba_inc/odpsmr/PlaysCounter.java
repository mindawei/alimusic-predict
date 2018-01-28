package com.alibaba_inc.odpsmr;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.Record;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.MapperBase;
import com.aliyun.odps.mapred.ReducerBase;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class PlaysCounter {

	public static class TestMapper extends MapperBase {
		private Record key;
		private Record value;

		@Override
		public void setup(TaskContext context) throws IOException {
			key = context.createMapOutputKeyRecord();
			value = context.createMapOutputValueRecord();
		}

		@Override
		public void map(long recordNum, Record record, TaskContext context)
				throws IOException {
			// artist_id,user_id,song_id,gmt_create,Ds
			key.set("artist_id", record.getString(0));
			key.set("Ds", record.getString(4));
			
			value.set("user_id", record.getString(1));
			value.set("song_id", record.getString(2));
			value.set("gmt_create", record.getString(3));
			

			context.write(key, value);
		}
		
	}

	public static class TestReducer extends ReducerBase {

		Record output;

		@Override
		public void setup(TaskContext context) throws IOException {
			output = context.createOutputRecord();
		}

		// key.set("artist_id", record.getString(0));
		// key.set("Ds", record.getString(4));
		// value.set("user_id", record.getString(1));
		// value.set("song_id", record.getString(2));
		// 歌曲名称不用考虑，只考虑一个小时内某个听众听某个艺人的歌曲数不多于16首的
		// value.set("gmt_create", record.getString(3));

		@Override
		public void reduce(Record key, Iterator<Record> values,
				TaskContext context) throws IOException {

			// user_id,gmt_create,num
			Map<String, Map<String, Integer>> playCounter = new HashMap<String, Map<String, Integer>>();

			
			
			while (values.hasNext()) {
				Record val = values.next();
				String user = val.getString("user_id");
				String hour = val.getString("gmt_create");

				if (!playCounter.containsKey(user)) {
					playCounter.put(user, new HashMap<String, Integer>());
				}
				// 获得已有的计数
				int num = playCounter.get(user).containsKey(hour) ? playCounter
						.get(user).get(hour) : 0;
				num += 1;
				playCounter.get(user).put(hour, num);

			}

			int max_num_per_hour = 20;
			long Plays = 0;
			for (String user : playCounter.keySet()) {
				for (String hour : playCounter.get(user).keySet()) {
					int num = playCounter.get(user).get(hour);
					num = Math.min(num, max_num_per_hour);
					Plays += num;
				}
			}

			output.set(0, key.getString("artist_id"));
			output.set(1, key.getString("Ds"));
			output.set(2, Plays);

			context.write(output);
		}
	}

	public static void main(String[] args) throws OdpsException {
	
		    if (args.length != 2) {
		      System.err.println("Usage: PlaysCount <user_actions_combine> <user_actions_count_filter>");
		      System.exit(2);
		    }

		    JobConf job = new JobConf();
			job.setMapperClass(TestMapper.class);
			job.setReducerClass(TestReducer.class);
			
			job.setMapOutputKeySchema(SchemaUtils.fromString("artist_id:string,Ds:string"));
			job.setMapOutputValueSchema(SchemaUtils.fromString("user_id:string,song_id:string,gmt_create:string"));
			
			

			
		    InputUtils.addTable(TableInfo.builder().tableName(args[0]).build(), job);
		    OutputUtils.addTable(TableInfo.builder().tableName(args[1]).build(), job);

		    JobClient.runJob(job);
	}

}
