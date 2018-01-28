

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class test {
	
	private static long millisPerDay = 24*3600*1000;
	private static SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");

	
	public static int getDays(String Ds){
	   
	    long days = 0;
		try {
			days = (sdf.parse(Ds).getTime() - sdf.parse("20150301").getTime())/ millisPerDay;
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return (int)days;

	}
	
	public static void main(String[] args) throws ParseException {
//		Map<Integer, Long> playCounter = new TreeMap<Integer, Long>();
//		playCounter.put(1, 3L);
//		playCounter.put(3, 9L);
//		playCounter.put(2, 6L);
//		playCounter.put(0, 0L);
//		for(Integer x:playCounter.keySet()){
//			System.out.println(x+" " +playCounter.get(x));
//		}
//		List<Long> Y = Arrays.asList(10L,21L,31L,41L,53L,64L,784L,83L,91L);
//		System.out.println(predict(Y));
//		
	System.out.println(""+16L);
	}
	
	public static Long predict(List<Long> Y){
		for(int i=0;i<5;++i)
			Y = weightSmooth(Y);
		for(int i=0;i<3;++i)
			Y = weightSmooth2(Y);
		return Y.get(Y.size()-1);
	}
	

	// 加权平均
	public static List<Long> weightSmooth(List<Long> Y){
		int size = Y.size();

	    List<Long> smoothedY = new ArrayList<Long>();
	    for(int i=0;i<size;++i)
	    	smoothedY.add(0L);

	    double[] weight = {0.07,0.13,0.18,0.24,0.18,0.13,0.07};
	   
	    int half_period = 3;
	    		
	    for(int i=0;i<size;++i){
	        
	    	int i_start = i - half_period;
	        i_start = Math.max(0,i_start);
	        
	        int i_end = i + half_period +1;
	        i_end = Math.min(size,i_end);
	        
	        if(i_end-i_start<7){
	        	smoothedY.set(i,Y.get(i));
	        }else{
	        	 double sum = 0;
	             int index = 0;
	        	 for(int j=i_start;j<i_end;++j){
	             	sum+=Y.get(j)*weight[index];
	             	index++;
	             }
	        	 smoothedY.set(i,(long)sum);
	        }
	    }
	    return smoothedY;
	}

// 加权平均
public static List<Long> weightSmooth2(List<Long> Y){
	int size = Y.size();

    List<Long> smoothedY = new ArrayList<Long>();
    for(int i=0;i<size;++i)
    	smoothedY.add(0L);

    double[] weight = {0.07,0.13,0.18,0.24,0.18,0.13,0.07};
   
    int half_period = 3;
    		
    for(int i=0;i<size;++i){
        
    	int i_start = i - half_period;
        i_start = Math.max(0,i_start);
        
        int i_end = i + half_period +1;
        i_end = Math.min(size,i_end);
        
        if(i_end-i_start<7){
        	 double sum = 0;
             int num = 0;
        	 for(int j=i_start;j<i_end;++j){
             	sum+=Y.get(j);
             	num++;
             }
        	 smoothedY.set(i,(long)(sum/num));
        }else{
        	 double sum = 0;
             int index = 0;
        	 for(int j=i_start;j<i_end;++j){
             	sum+=Y.get(j)*weight[index];
             	index++;
             }
        	 smoothedY.set(i,(long)sum);
        }
    }
    return smoothedY;
}



}
